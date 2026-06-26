#!/usr/bin/env bash
# 查看 GitLab 仓库中所有可用的技能
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== 可用技能 ==="
curl -sf "http://10.10.11.4:30690/product/iot/iottool/skills/-/raw/main/skills-catalog.json" | \
  python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    skills = data.get('skills', [])
    for s in skills:
        print(f\"  {s['name']}: {s['description']}\")
except Exception as e:
    print(f\"解析失败: {e}\")
"
