#!/usr/bin/env bash
# 查看 GitHub 仓库中所有可用的技能
# 用法: ./scripts/list-skills.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# 从 .env 读取 token
if [ -f "$HOME/.hermes/.env" ]; then
    TOKEN=$(grep "^GITHUB_TOKEN=" "$HOME/.hermes/.env" | cut -d= -f2)
fi

if [ -z "$TOKEN" ] && [ -f "$REPO_DIR/.env" ]; then
    TOKEN=$(grep "^GITHUB_TOKEN=" "$REPO_DIR/.env" | cut -d= -f2)
fi

if [ -z "$TOKEN" ]; then
    echo "错误: 未找到 GITHUB_TOKEN，请先配置 ~/.hermes/.env"
    exit 1
fi

echo "=== 可用技能 ==="
curl -sf -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/13420948160/hermes-skills/contents/skills" | \
  python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, list):
        for d in data:
            if d.get('type') == 'dir':
                print(f\"  {d['name']}\")
    elif isinstance(data, dict) and 'message' in data:
        print(f\"错误: {data['message']}\")
except Exception as e:
    print(f\"解析失败: {e}\")
"
