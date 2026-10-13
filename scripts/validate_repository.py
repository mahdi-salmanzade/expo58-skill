#!/usr/bin/env python3
"""Validate this skill repository's packaging and offline navigation (stdlib only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def read_json(path: Path) -> dict:
        try:
            value = json.loads(path.read_text())
            if not isinstance(value, dict):
                raise ValueError("expected a JSON object")
            return value
        except (OSError, ValueError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            return {}

    market = read_json(root / ".claude-plugin/marketplace.json")
    plugin_root = root / "expo-58"
    plugin = read_json(plugin_root / ".claude-plugin/plugin.json")
    skill = plugin_root / "skills/expo-58"
    entry_path = skill / "SKILL.md"
    entry = entry_path.read_text() if entry_path.is_file() else ""
    require(bool(entry), "Missing SKILL.md")
    require(entry.startswith("---\nname: expo-58\n"), "Incorrect skill name/frontmatter")
    require(bool(re.search(r"^description:\s*\S+", entry, re.M)), "Missing skill description")
    require(plugin.get("name") == "expo-58", "Incorrect plugin name")
    require(market.get("name") == "expo58-skill", "Incorrect marketplace name")
    catalog = market.get("plugins", [])
    require(len(catalog) == 1, "Expected one marketplace plugin")
    if len(catalog) == 1:
        item = catalog[0]
        require(item.get("source") == "./expo-58", "Incorrect plugin source path")
        for key in ("name", "version", "description"):
            require(item.get(key) == plugin.get(key), f"Plugin/catalog {key} mismatch")
    require((skill / "agents/openai.yaml").is_file(), "Missing Codex UI metadata")

    # Resolve local Markdown links relative to each file, including links to code.
    # Strip fenced code first so illustrative links aren't mistaken for navigation.
    for doc in root.rglob("*.md"):
        if any(part in {".git", "node_modules", ".venv"} for part in doc.parts):
            continue
        body = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", doc.read_text(), flags=re.M | re.S)
        for target in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", body):
            target = target.strip().split(' "', 1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("#", "//")):
                continue
            relative = unquote(parsed.path)
            if not relative:
                continue
            resolved = (doc.parent / relative).resolve()
            require(resolved.is_relative_to(root), f"{doc.relative_to(root)}: nonportable link {target}")
            require(resolved.exists(), f"{doc.relative_to(root)}: missing local target {target}")

    references = sorted((skill / "references").glob("[0-9][0-9]-*.md"))
    require(len(references) == 23, f"Expected 23 topic references; found {len(references)}")
    for reference in references:
        require(f"references/{reference.name}" in entry, f"Unrouted reference: {reference.name}")

    snapshot = read_json(skill / "references/sdk-versions.json")
    require(snapshot.get("schemaVersion") == 1, "Unsupported package snapshot schema")
    require(bool(snapshot.get("auditedAt")), "Snapshot has no audit date")
    require(bool(snapshot.get("sources")), "Snapshot has no source provenance")
    sdk = snapshot.get("sdk58", {})
    require(bool(re.fullmatch(r"58\.\d+\.\d+", sdk.get("expoVersion", ""))), "Snapshot is not Expo 58")
    bundled = sdk.get("bundledNativeModules", {})
    for name in ("react", "react-native", "expo-router", "@expo/ui", "expo-hinge"):
        require(bool(bundled.get(name)), f"Snapshot lacks bundled package: {name}")
    require(bool(sdk.get("provenance", {}).get("integrity")), "Expo tarball integrity missing")
    require(bool(sdk.get("template", {}).get("dependencies")), "Template dependencies missing")

    evaluations = read_json(skill / "evals/evals.json")
    ids: set[str] = set()
    for case in evaluations.get("evals", []):
        case_id = case.get("id", "")
        require(bool(case_id) and case_id not in ids, f"Missing or duplicate eval id: {case_id}")
        ids.add(case_id)
        require(bool(case.get("prompt")), f"Eval {case_id} has no prompt")
        require(bool(case.get("assertions")), f"Eval {case_id} has no observable assertions")
    require(len(ids) >= 10, "Expected SDK and Duo evaluation scenarios")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Valid: plugin packaging, 23 references, local links, package snapshot, and evaluation scenarios.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
