#!/usr/bin/env python3
"""Hermes Skills Hub Browser - 查看仓库中所有可用技能"""
import json
import os
import sys
import urllib.request
import urllib.error

# GitLab 项目编码
GITLAB_HOST = "http://10.10.11.4:30690"
PROJECT_PATH = "product/iot/iottool/skills"
PROJECT_ENCODED = "product%2Fiot%2Fiottool%2Fskills"
BRANCH = "develop"  # 当前在 develop 分支，合并到 main 后改为 main

# GitLab API 地址（需配置 private_token）
API_URL = f"{GITLAB_HOST}/api/v4/projects/{PROJECT_ENCODED}/repository/files/skills-catalog.json/raw?ref={BRANCH}"


def get_token():
    """从环境变量或 .env 文件读取 GITLAB_TOKEN"""
    token = os.environ.get("GITLAB_TOKEN") or os.environ.get("GITLAB_PRIVATE_TOKEN")
    if token:
        return token
    # 尝试从 ~/.hermes/.env 读取
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("GITLAB_TOKEN=") or line.startswith("GITLAB_PRIVATE_TOKEN="):
                    return line.strip().split("=", 1)[1]
    return None


def fetch_json(url: str, token: str, timeout: int = 10):
    req = urllib.request.Request(url)
    if token:
        req.add_header("PRIVATE-TOKEN", token)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    token = get_token()
    if not token:
        print("错误: 未找到 GITLAB_TOKEN", file=sys.stderr)
        print("请配置 ~/.hermes/.env 或设置环境变量:", file=sys.stderr)
        print("  echo \"GITLAB_TOKEN=你的token\" >> ~/.hermes/.env", file=sys.stderr)
        sys.exit(1)

    try:
        data = fetch_json(API_URL, token)
    except urllib.error.HTTPError as e:
        print(f"错误: GitLab API 返回 {e.code}", file=sys.stderr)
        if e.code == 401:
            print("      Token 无效，请检查 GITLAB_TOKEN 是否正确", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: 无法获取技能列表", file=sys.stderr)
        print(f"      {e}", file=sys.stderr)
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
        print(f"python3 ~/.hermes/skills/hermes-hub-browser/scripts/install-from-gitlab.py {s['name']}")
    print("```")
    print()


if __name__ == "__main__":
    main()
