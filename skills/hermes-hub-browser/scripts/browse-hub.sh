#!/usr/bin/env bash
# 从 skills-catalog.json 获取技能列表，格式化输出
set -e

CATALOG_URL="https://raw.githubusercontent.com/13420948160/hermes-skills/main/skills-catalog.json"

tmpfile=$(mktemp)
if ! curl -sf -o "$tmpfile" "$CATALOG_URL"; then
    rm -f "$tmpfile"
    echo "错误: 无法获取 $CATALOG_URL"
    exit 1
fi

python3 - "$tmpfile" << 'PYEOF'
import sys, json

with open(sys.argv[1]) as f:
    d = json.load(f)

skills = d.get('skills', [])
updated = d.get('updated', '?')

print()
print(f'   Hermes Skills Hub  —  共 {len(skills)} 个技能')
print(f'   更新时间: {updated}')
print()
print(f'  {"序号":<4} {"技能名称":<20} {"说明"}')
print(f'  {"-"*4} {"-"*20} {"-"*40}')

for i, s in enumerate(skills, 1):
    name = s['name'][:18]
    desc = s['description'][:38]
    print(f'  {i:<4} {name:<20} {desc}')

print()
print('  安装命令:')
for s in skills:
    cmd = 'hermes skills install 13420948160/hermes-skills/skills/' + s['path']
    print(f'    {cmd}')
print()
PYEOF

rm -f "$tmpfile"
