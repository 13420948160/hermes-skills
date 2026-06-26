# Hermes Skills Hub

内网 GitLab 仓库，托管自定义 Hermes 技能。

**仓库地址:** `http://10.10.11.4:30690/product/iot/iottool/skills.git`  
**当前分支:** `develop`（待合并到 `main`）  
**同步推送:** GitHub `https://github.com/13420948160/hermes-skills.git`

---

## 目录结构

```
skills/
├── hello-hermes/
│   └── SKILL.md
└── hermes-skills/
    ├── SKILL.md
    └── scripts/
        └── hermes-skills           # CLI 主程序（browse/install/uninstall）

generate-catalog.py                 # 本地生成 skills-catalog.json
skills-catalog.json                 # 技能清单（供 CLI 读取）
```

## 前提：配置 GITLAB_TOKEN

本仓库为私有仓库，需配置访问 token。

**1. 创建 Token**

打开 GitLab → User Settings → Access Tokens → 创建 `read_api` 权限的 token。

**2. 写入配置文件**

```bash
echo "GITLAB_TOKEN=你的Token" >> ~/.hermes/.env
```

## 使用 hermes-skills CLI

CLI 命令已安装到 `~/.local/bin/hermes-skills`，支持三个操作：

### 查看所有可用技能

```bash
hermes-skills browse
```

输出示例：

```
  #   Name                 Description
  --- -------------------- ----------------------------------------
  1   hello-hermes         Use when the user wants to test the ...
  2   hermes-skills        Manage skills from private GitLab hub ...
```

### 安装技能

```bash
hermes-skills install hello-hermes
```

从 GitLab develop 分支下载 SKILL.md 到 `~/.hermes/skills/<name>/`。

### 卸载技能

```bash
hermes-skills uninstall hello-hermes
```

删除 `~/.hermes/skills/<name>/` 目录。

## 添加新技能

1. 在 `skills/` 下创建 `<技能名>/SKILL.md`
2. 本地生成 catalog：`python3 generate-catalog.py`
3. 提交并推送
4. 其他人执行 `hermes-skills browse` 即可看到新技能

## 常用 Hermes 命令

| 命令 | 说明 |
|------|------|
| `hermes skills list` | 列出所有已安装技能 |
| `hermes skills install <url>` | 从 URL 安装技能 |
| `/skill <name>` | 在会话中加载技能 |

## SKILL.md 格式规范

```markdown
---
name: skill-name
description: Use when <触发条件>. <一句话行为描述>.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tag1, tag2]
    related_skills: [other-skill]
---

# 技能标题

## Overview
说明做什么、为什么。

## 正文内容
具体步骤、最佳实践、命令示例等。
```

关键约束：
- `description` ≤ 1024 字符
- 文件以 `---` 开头（无前导空白）
- `name` 字段全局唯一

## 验证清单

- [ ] SKILL.md 文件以 `---` 开头
- [ ] frontmatter 完整
- [ ] `description` ≤ 1024 字符
- [ ] 已推送并更新 `skills-catalog.json`
- [ ] `hermes-skills browse` 能查到
- [ ] `hermes-skills install` 安装成功
