#!/usr/bin/env python3
"""Audit published Expo manifests without installing packages or running lifecycle scripts."""

import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
import urllib.parse
import urllib.request

REGISTRY = "https://registry.npmjs.org/"
ROOT = Path(__file__).resolve().parents[1]


def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def metadata(name, version):
    url = REGISTRY + urllib.parse.quote(name, safe="@/") + "/" + version
    return get_json(url), url


def read_manifests(meta):
    """Read only named files in memory; never extract or execute package content."""
    url = meta["dist"]["tarball"]
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "registry.npmjs.org":
        raise ValueError("Expected an HTTPS npm registry tarball")
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    integrity = meta["dist"]["integrity"]
    algorithm, expected = integrity.split("-", 1)
    if algorithm != "sha512":
        raise ValueError("Expected npm sha512 integrity")
    actual = base64.b64encode(hashlib.sha512(data).digest()).decode()
    if actual != expected:
        raise ValueError("Tarball integrity mismatch")
    result = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for name in ("package/package.json", "package/bundledNativeModules.json"):
            try:
                member = archive.getmember(name)
            except KeyError:
                continue
            if not member.isfile():
                raise ValueError(f"Expected regular file: {name}")
            result[name.rsplit("/", 1)[-1]] = json.load(archive.extractfile(member))
    return result


def evidence(meta, url):
    return {"metadataUrl": url, "tarballUrl": meta["dist"]["tarball"],
            "integrity": meta["dist"]["integrity"]}


def sdk_snapshot(version):
    meta, url = metadata("expo", version)
    manifests = read_manifests(meta)
    package = manifests["package.json"]
    if package["version"] != version:
        raise ValueError("Expo package version mismatch")
    return {"expoVersion": version, "expoEngines": package.get("engines", {}),
            "bundledNativeModules": manifests["bundledNativeModules.json"],
            "toolingDependencies": package["dependencies"],
            "provenance": evidence(meta, url)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expo-version", default="58.0.8")
    parser.add_argument("--comparison-version", default="57.0.28")
    parser.add_argument("--template-version", default="58.0.17")
    parser.add_argument("--audited-at", required=True, help="YYYY-MM-DD, after reviewing release status")
    parser.add_argument("--release-status", choices=["beta", "stable"], required=True,
                        help="Human-reviewed status; do not infer from numeric npm versions")
    parser.add_argument("--release-status-url", help="Official release page used to verify status")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "expo-58/skills/expo-58/references/sdk-versions.json")
    args = parser.parse_args()
    for value, major in ((args.expo_version, 58), (args.comparison_version, 57),
                         (args.template_version, 58)):
        if not re.fullmatch(rf"{major}\.\d+\.\d+", value):
            parser.error(f"Expected an exact {major}.x.x version, got {value!r}")
    from datetime import date
    date.fromisoformat(args.audited_at)
    sdk58 = sdk_snapshot(args.expo_version)
    sdk57 = sdk_snapshot(args.comparison_version)
    template_meta, template_url = metadata("expo-template-default", args.template_version)
    template = read_manifests(template_meta)["package.json"]
    for name in ("react", "react-native", "react-native-reanimated", "react-native-worklets"):
        if template["dependencies"][name] != sdk58["bundledNativeModules"][name]:
            raise ValueError(f"Template and Expo bundled versions differ for {name}")
    sdk58["releaseStatus"] = args.release_status
    sdk58["featurePackages"] = {}
    for name in ("expo-hinge", "@expo/ui", "expo-router"):
        version = sdk58["bundledNativeModules"][name].lstrip("~^")
        meta, url = metadata(name, version)
        sdk58["featurePackages"][name] = {"version": version, "provenance": evidence(meta, url)}
    sdk58["template"] = {"packageName": "expo-template-default", "version": template["version"],
                         "dependencies": template["dependencies"],
                         "devDependencies": template.get("devDependencies", {}),
                         "engines": template.get("engines", {}),
                         "provenance": evidence(template_meta, template_url)}
    data = {"schemaVersion": 1, "auditedAt": args.audited_at,
            "sources": {"releaseStatus": args.release_status_url or
                        ("https://expo.dev/changelog/sdk-58-beta" if args.release_status == "beta"
                         else "https://expo.dev/changelog/sdk-58"),
                        "compatibility": "https://docs.expo.dev/versions/v58.0.0/",
                        "registry": REGISTRY,
                        "manifestNote": "Ranges are copied from published artifacts, not resolved lockfile versions."},
            "distTags": {name: get_json(REGISTRY + "-/package/" + name + "/dist-tags")
                         for name in ("expo", "expo-template-default", "create-expo-app")},
            "sdk58": sdk58, "sdk57": sdk57}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(args.output)
    print(f"Wrote {args.output}: Expo {args.expo_version}, {len(sdk58['bundledNativeModules'])} package ranges")


if __name__ == "__main__":
    main()
