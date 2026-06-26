---
name: hermes-skills
description: Manage skills from private GitLab hub. Browse, install, and uninstall skills using the hermes-skills CLI command.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hub, install, uninstall, browse, gitlab]
    related_skills: [hello-hermes]
---

# Hermes Skills Manager

## Overview

管理私有 GitLab 仓库中的 Hermes 技能。支持浏览、安装、卸载。

## 使用方式

```bash
# 查看所有可用技能
hermes-skills browse

# 安装技能
hermes-skills install hello-hermes

# 卸载技能
hermes-skills uninstall hello-hermes
```

## 前提

需在 `~/.hermes/.env` 中配置 `GITLAB_TOKEN=你的Token`

## 输出示例

```
## Hermes Skills Hub -- 2 skills

| # | Name | Description |
|---|------|-------------|
| 1 | hello-hermes | Use when the user wants to test ... |
| 2 | hermes-hub-browser | Use when browsing available skills ... |

Install:
  hermes-skills install hello-hermes
  hermes-skills install hermes-hub-browser
```
