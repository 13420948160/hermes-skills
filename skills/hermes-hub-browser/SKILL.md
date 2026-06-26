---
name: hermes-hub-browser
description: Use when browsing available skills in the custom hub. Lists all skills in a table with copyable install commands.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hub, browse, list, install]
    related_skills: [hello-hermes]
---

# Hermes Skills Hub Browser

## Overview

浏览内网 GitLab 仓库中的所有技能，以表格展示，附带安装命令。

## 使用方式

```bash
# 查看技能清单
source ~/.hermes/.env
python3 ~/.hermes/skills/hermes-hub-browser/scripts/browse-hub.py

# 安装技能
python3 ~/mycode/hermes-skills/scripts/install-from-gitlab.py hello-hermes
```

## 输出示例

```
## Hermes Skills Hub  —  共 2 个技能

| 序号 | 技能名称 | 说明 |
|------|---------|------|
| 1 | hello-hermes | Use when the user wants to test ... |
| 2 | hermes-hub-browser | Use when browsing available skills ... |

### 安装命令

python3 scripts/install-from-gitlab.py hello-hermes
python3 scripts/install-from-gitlab.py hermes-hub-browser
```
