#!/usr/bin/env python3
"""Hermes Skills Hub Browser - 查看仓库中所有可用技能"""
import json
import sys
import urllib.request

CATALOG_URL = "https://raw.githubusercontent.com/13420948160/hermes-skills/main/skills-catalog.json"


def main():
    try:
        with urllib.request.urlopen(CATALOG_URL, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"错误: 无法获取 {CATALOG_URL}")
        print(f"      {e}")
        sys.exit(1)

    skills = data.get("skills", [])
    updated = data.get("updated", "?")

    print()
    print(f"   Hermes Skills Hub  —  共 {len(skills)} 个技能")
    print(f"   更新时间: {updated}")
    print()
    print(f"  {'序号':<4} {'技能名称':<20} {'说明'}")
    print(f"  {'-'*4} {'-'*20} {'-'*40}")

    for i, s in enumerate(skills, 1):
        name = s["name"][:18]
        desc = s["description"][:38]
        print(f"  {i:<4} {name:<20} {desc}")

    print()
    print("  安装命令:")
    for s in skills:
        cmd = f"hermes skills install 13420948160/hermes-skills/skills/{s['path']}"
        print(f"    {cmd}")
    print()


if __name__ == "__main__":
    main()
