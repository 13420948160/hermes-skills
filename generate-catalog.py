#!/usr/bin/env python3
"""Scan skills/ directory and generate skills-catalog.json."""
import json
import os
import re
import subprocess
from datetime import datetime, timezone

SKILLS_DIR = "skills"
OUTPUT = "skills-catalog.json"
REPO_DIR = os.path.dirname(os.path.abspath(__file__))


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


def get_skill_updated(skill_path: str) -> str:
    """获取某文件最近一次 commit 的日期"""
    result = subprocess.run(
        ["git", "log", "--format=%ad", "--date=short", "-1", "--", skill_path],
        capture_output=True, text=True, cwd=REPO_DIR
    )
    return result.stdout.strip()


def bump_version(ver: str) -> str:
    """递增版本号最后一位，如 1.0.0 -> 1.0.1"""
    if not ver:
        return "1.0.0"
    parts = ver.split(".")
    try:
        parts[-1] = str(int(parts[-1]) + 1)
    except ValueError:
        return ver
    return ".".join(parts)


def main():
    catalog_path = os.path.join(REPO_DIR, OUTPUT)
    existing = {}
    if os.path.exists(catalog_path):
        with open(catalog_path, encoding="utf-8") as f:
            old = json.load(f)
        for s in old.get("skills", []):
            existing[s["name"]] = s

    skills = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" not in files:
            continue
        skill_path = os.path.join(root, "SKILL.md")
        path = os.path.relpath(skill_path, SKILLS_DIR)
        skill_dir = os.path.dirname(path)
        name = os.path.basename(skill_dir)
        with open(skill_path, encoding="utf-8") as f:
            content = f.read()
        fm = parse_frontmatter(content)

        # git commit 日期作为 updated
        git_updated = get_skill_updated(skill_path)

        old_skill = existing.get(name, {})
        old_updated = old_skill.get("updated", "")

        if old_updated == git_updated:
            # 未修改，沿用旧版本
            version = old_skill.get("version", fm.get("version", ""))
            updated = old_updated
        else:
            # 已修改，递增版本号
            version = bump_version(old_skill.get("version", fm.get("version", "")))
            updated = git_updated

        skills.append({
            "name": name,
            "path": skill_dir,
            "description": fm.get("description", ""),
            "version": version,
            "updated": updated,
        })

    catalog = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skills": skills,
    }
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"Catalog: {len(skills)} skills -> {catalog_path}")


if __name__ == "__main__":
    main()
