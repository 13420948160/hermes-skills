#!/usr/bin/env python3
"""Scan skills/ directory and generate skills-catalog.json."""
import json
import os
import re
from datetime import datetime, timezone

SKILLS_DIR = "skills"
OUTPUT = "skills-catalog.json"


def parse_frontmatter(content: str) -> dict:
    result = {}
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return result
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key:
                result[key] = val
    return result


def main():
    skills = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" not in files:
            continue
        path = os.path.relpath(os.path.join(root, "SKILL.md"), SKILLS_DIR)
        skill_dir = os.path.dirname(path)
        name = os.path.basename(skill_dir)
        with open(os.path.join(root, "SKILL.md"), encoding="utf-8") as f:
            content = f.read()
        fm = parse_frontmatter(content)
        skill_path = os.path.join(root, "SKILL.md")
        mtime = datetime.fromtimestamp(os.path.getmtime(skill_path), tz=timezone.utc).strftime("%Y-%m-%d")
        skills.append({
            "name": name,
            "path": skill_dir,
            "description": fm.get("description", ""),
            "version": fm.get("version", ""),
            "updated": mtime,
        })
    catalog = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skills": skills,
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"Catalog: {len(skills)} skills -> {OUTPUT}")


if __name__ == "__main__":
    main()
