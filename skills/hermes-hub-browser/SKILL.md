---
name: hermes-hub-browser
description: Use when browsing available skills in the custom hub. Lists all skills from skills-catalog.json in a table with copyable install commands.
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

浏览自定义 Hermes Skills Hub（内网 GitLab `product/iot/iottool/skills`）中的所有技能。从 `skills-catalog.json` 读取数据，以表格形式展示，并附带可直接复制的安装命令。

## 使用方式

运行脚本（Windows / macOS / Linux 通用）：

```bash
python3 ~/.hermes/skills/hermes-hub-browser/scripts/browse-hub.py
```

输出示例：

```
## Hermes Skills Hub  —  共 2 个技能

更新时间: 2026-06-26T10:33:54Z

| 序号 | 技能名称 | 说明 |
|------|---------|------|
| 1 | hello-hermes | Use when the user wants to test the Hermes ... |
| 2 | hermes-hub-browser | Use when browsing available skills ... |

### 安装命令

hermes skills install "http://10.10.11.4:30690/product/iot/iottool/skills/-/raw/main/skills/hello-hermes/SKILL.md" --name hello-hermes
hermes skills install "http://10.10.11.4:30690/product/iot/iottool/skills/-/raw/main/skills/hermes-hub-browser/SKILL.md" --name hermes-hub-browser
```

## 添加新技能

1. 在 `skills/` 下创建 `<技能名>/SKILL.md`
2. 推送到 GitLab
3. GitHub Actions 自动更新 `skills-catalog.json`
4. 运行本技能查看最新列表

## 常见问题

**Q: skills-catalog.json 没有及时更新？**
A: 手动运行 `python3 scripts/generate-catalog.py` 生成，然后提交推送。
