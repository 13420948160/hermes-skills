#!/usr/bin/env python3
"""Hermes Skills Hub Browser - 查看仓库中所有可用技能"""
import json
import sys
import urllib.request

# 直连 URL，国内慢时可切换镜像
CATALOG_URL = "https://raw.githubusercontent.com/13420948160/hermes-skills/main/skills-catalog.json"
# gh-proxy.com 镜像（国内 ≈450KB/s）
MIRROR_URL = "https://gh-proxy.com/https://raw.githubusercontent.com/13420948160/hermes-skills/main/skills-catalog.json"


def fetch_json(url: str, timeout: int = 10):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    data = None
    err = None

    # 先尝试直连
    try:
        data = fetch_json(CATALOG_URL)
    except Exception as e:
        err = e
        # 直连失败，尝试镜像
        try:
            print("直连超时，尝试 gh-proxy.com 镜像...", file=sys.stderr)
            data = fetch_json(MIRROR_URL, timeout=30)
        except Exception as e2:
            print(f"错误: 无法获取技能列表", file=sys.stderr)
            print(f"      直连: {err}", file=sys.stderr)
            print(f"      镜像: {e2}", file=sys.stderr)
            sys.exit(1)

    skills = data.get("skills", [])
    updated = data.get("updated", "?")

    print()
    print(f"## Hermes Skills Hub  —  共 {len(skills)} 个技能")
    print()
    print(f"更新时间: {updated}")
    print()
    print("| 序号 | 技能名称 | 说明 |")
    print("|------|---------|------|")

    for i, s in enumerate(skills, 1):
        print(f"| {i} | {s['name']} | {s['description']} |")

    print()
    print("### 安装命令")
    print()
    print("```bash")
    for s in skills:
        print(f"hermes skills install 13420948160/hermes-skills/skills/{s['path']}")
    print("```")
    print()


if __name__ == "__main__":
    main()
