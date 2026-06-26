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

浏览自定义 Hermes Skills Hub（`13420948160/hermes-skills`）中的所有技能。从 GitHub 的 `skills-catalog.json` 读取数据，以表格形式展示，并附带可直接复制的安装命令。

## 使用方式

运行脚本（Windows / macOS / Linux 通用）：

```bash
python3 ~/.hermes/skills/hermes-hub-browser/scripts/browse-hub.py
```

输出示例：

```
   Hermes Skills Hub  —  共 2 个技能
   更新时间: 2026-06-26T09:44:42Z

  序号  技能名称                说明
  ----  --------------------  ----------------------------------------
  1     hello-hermes          Use when the user wants to test the Hermes
  2     hermes-hub-browser    Use when browsing available skills in the custom hub

  安装命令:
    hermes skills install 13420948160/hermes-skills/skills/hello-hermes
    hermes skills install 13420948160/hermes-skills/skills/hermes-hub-browser
```

复制需要的安装命令粘贴到终端即可。

## 添加新技能

1. 在 `skills/` 下创建 `<技能名>/SKILL.md`
2. 推送到 GitHub
3. GitHub Actions 自动更新 `skills-catalog.json`
4. 运行本技能查看最新列表

## 常见问题

**Q: 安装命令中的 `skills/skills/` 是不是重复了？**
A: 不是。第一个 `skills/` 是仓库中的目录名，第二个是技能路径。`hermes skills install` 需要仓库内的完整路径。

**Q: skills-catalog.json 没有及时更新？**
A: 检查 `.github/workflows/sync-catalog.yml` 是否正常运行。也可手动触发：GitHub → Actions → Generate Skills Catalog → Run workflow。
