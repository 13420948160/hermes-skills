---
name: skills-manage
description: 从私有 GitLab 仓库管理 Hermes 技能。使用 skills-manage CLI 命令浏览、安装和卸载技能。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hub, install, uninstall, browse, gitlab]
    related_skills: [hello-skill]
---

# Hermes 技能管理器

## 概述

从私有 GitLab 仓库管理 Hermes 技能，支持浏览、安装和卸载操作。

## 使用方式

```bash
# 浏览所有可用技能
skills-manage browse

# 安装技能
skills-manage install hello-skill

# 卸载技能
skills-manage uninstall hello-skill
```

## 前提条件

需在 `~/.hermes/.env` 中配置 `GITLAB_TOKEN=你的Token`

## 输出示例

```
## Hermes Skills Hub -- 2 skills

| # | Name | Description |
|---|------|-------------|
| 1 | hello-skill | Use when the user wants to test ... |
| 2 | skills-manage | Manage skills from private GitLab hub ... |

安装方式：
  skills-manage install hello-skill
  skills-manage install skills-manage
```
