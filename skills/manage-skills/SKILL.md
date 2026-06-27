---
name: manage-skills
description: 从私有 GitLab 仓库管理 Hermes 技能。使用 manage-skills CLI 命令浏览、安装和卸载技能。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hub, install, uninstall, browse, gitlab]
    related_skills: [hello-hermes]
---

# Hermes 技能管理器

## 概述

从私有 GitLab 仓库管理 Hermes 技能，支持浏览、安装和卸载操作。

## 使用方式

```bash
# 浏览所有可用技能
manage-skills browse

# 安装技能
manage-skills install hello-hermes

# 卸载技能
manage-skills uninstall hello-hermes
```

## 前提条件

需在 `~/.hermes/.env` 中配置 `GITLAB_TOKEN=你的Token`

## 输出示例

```
## Hermes Skills Hub -- 2 skills

| # | Name | Description |
|---|------|-------------|
| 1 | hello-hermes | Use when the user wants to test ... |
| 2 | manage-skills | Manage skills from private GitLab hub ... |

安装方式：
  manage-skills install hello-hermes
  manage-skills install manage-skills
```
