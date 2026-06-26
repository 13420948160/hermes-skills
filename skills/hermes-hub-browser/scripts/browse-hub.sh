#!/usr/bin/env bash
# 从 skills-catalog.json 获取技能列表，格式化输出
set -e

CATALOG_URL="https://raw.githubusercontent.com/13420948160/hermes-skills/main/skills-catalog.json"

data=$(curl -sf "$CATALOG_URL") || {
    echo "错误: 无法获取 $CATALOG_URL"
    exit 1
}

echo "$data" | python3 -c "
import sys, json

d = json.load(sys.stdin)
skills = d.get('skills', [])
updated = d.get('updated', '?')

print(f'🛠  Hermes Skills Hub  —  共 {len(skills)} 个技能')
print(f'   更新时间: {updated}')
print()
print(f'{\"序号\":<6} {\"技能名称\":<20} {\"说明\":<40}')
print('-' * 80)

for i, s in enumerate(skills, 1):
    name = s['name'][:18]
    desc = s['description'][:38]
    print(f'{i:<6} {name:<20} {desc}')

print()
print('安装命令:')
for s in skills:
    install_cmd = f'hermes skills install 13420948160/hermes-skills/skills/{s[\"path\"]}'
    print(f'  {install_cmd}')
print()
print('提示: 复制上面的安装命令即可安装对应技能')
"
