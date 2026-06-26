# Hermes Skills Hub 管理指南

## 概述

Hermes 技能（Skills）是可复用的工作流程和规范，以 Markdown 文档形式存储，支持从 GitHub 仓库发布和安装。

## 核心概念

| | 技能 (Skills) | 插件 (Plugins) |
|---|---|---|
| 定位 | 可复用的事件处理流程和操作规范 | 系统功能扩展 |
| 存放位置 | `~/.hermes/skills/` | `~/.hermes/plugins/` |
| 内容形式 | Markdown + YAML frontmatter | Python 代码 |
| 用途 | 工作流、排查步骤、最佳实践 | 扩展工具能力 |
| 加载方式 | 运行时按需加载 | 启动时全局加载 |
| 管理命令 | `hermes skills *` | `hermes plugins *` |

**一句话总结：技能 = Agent 的"经验知识库"；插件 = Agent 的"工具箱"** 

## 目录结构

```
skills/
└── <category>/
    └── <skill-name>/
        └── SKILL.md           # 必需：技能定义
        └── references/        # 可选：附加文档
        └── scripts/           # 可选：辅助脚本
        └── templates/         # 可选：文件模板
```

## SKILL.md 格式规范

文件必须以 `---` 开头，包含以下 frontmatter：

```markdown
---
name: skill-name                # 小写，hyphen分隔，≤64字符
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

## When to Use
- 触发条件1
- 触发条件2

## 正文内容
具体步骤、最佳实践、命令示例等。

## Common Pitfalls
1. 常见错误及修复

## Verification Checklist
- [ ] 验证项1
- [ ] 验证项2
```

### 关键约束

- `description` ≤ 1024 字符
- 文件必须以 `---` 开头（无前导空白）
- 总文件大小 ≤ 100,000 字符
- `name` 字段全局唯一

## 自建 Skills Hub

### 方式一：GitHub 仓库（推荐）

**1. 接入 Hub（tap add）**

```bash
hermes skills tap add owner/repo
```

> 注意：`tap add` 仅支持 GitHub，不支持 GitLab

**2. 推送技能到 GitHub**

```bash
git clone https://github.com/owner/repo.git
# 创建技能文件
git add -A && git commit -m "feat: add <skill-name>"
git push origin main
```

## 查看仓库里的所有技能

### 方式一：skills-catalog.json（推荐）

每次推送新技能，GitHub Actions 自动更新：

```bash
curl -s "https://raw.githubusercontent.com/13420948160/hermes-skills/main/skills-catalog.json"
```

### 方式二：GitHub API

```bash
# 从 .env 文件读取 token 直接使用
GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=*** ~/.hermes/.env | cut -d= -f2) && \
curl -s -H "Authorization: token *** "https://api.github.com/repos/13420948160/hermes-skills/contents/skills"
```

### 方式三：脚本

```bash
bash scripts/list-skills.sh
```

## 安装技能

```bash
# 从 repo 安装（需要先 tap add）
hermes skills install owner/repo/skills/category/skill-name

# 强制重装（已安装时使用）
hermes skills install owner/repo/skills/category/skill-name --force

# 从 raw URL 直接安装（无需 tap）
hermes skills install "https://raw.githubusercontent.com/owner/repo/main/skills/category/skill-name/SKILL.md" --name skill-name
```

### 方式二：手动安装

```bash
mkdir -p ~/.hermes/skills/<category>/<skill-name>
# 下载或复制 SKILL.md 到该目录
cp SKILL.md ~/.hermes/skills/<category>/<skill-name>/
```

### 方式三：GitLab（有限支持）

GitLab 仓库不能使用 `tap add`，但可以通过 URL 安装：

```bash
# 需要获取 GitLab raw 文件的直接 URL
hermes skills install "<gitlab-raw-url>" --name skill-name
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `hermes skills list` | 列出所有已安装技能 |
| `hermes skills search <query>` | 搜索技能 |
| `hermes skills browse` | 浏览 Hub 上所有可用技能 |
| `hermes skills tap list` | 查看已配置的 taps |
| `hermes skills tap add owner/repo` | 添加 GitHub 仓库为技能源 |
| `hermes skills tap remove owner/repo` | 移除技能源 |
| `hermes skills install <identifier>` | 安装技能 |
| `hermes skills install <url>` | 从 URL 安装技能 |
| `hermes skills inspect <identifier>` | 预览技能内容 |
| `hermes skills uninstall <name>` | 卸载技能 |
| `/skill <name>` | 在会话中加载技能 |

## GITHUB_TOKEN 配置

`hermes skills install` 需要 GitHub API 认证才能正常使用。推荐配置方式：

### 1. 获取 Token

- 创建 **Classic token**（经典 PAT，`ghp_` 开头）：https://github.com/settings/tokens/new
- 权限选择：`Contents: Read`（仅读取仓库内容）
- 注意：**Fine-grained PAT**（`github_pat_` 开头）可能导致 Git Trees API 认证失败，推荐用经典 PAT

### 2. 写入配置文件

```bash
echo "GITHUB_TOKEN=ghp_your_token_here" >> ~/.hermes/.env
```

### 3. 安装前清理环境

当前 shell 会话可能继承了旧 token，安装前清除：

```bash
unset GITHUB_TOKEN
source ~/.hermes/.env
hermes skills install owner/repo/skills/category/skill-name
```

## 搜索不到刚上传的技能？

`hermes skills search` 和 `browse` 搜不到自定义 tap 的技能，这是 **Hermes 的设计限制**，不是配置问题。

### 根本原因

当中心化索引（Hermes Index）存在时，`search` 和 `browse` 会**跳过所有 GitHub 源**（包括自定义 tap），只用官方索引。源码中明确跳过：

```python
_api_source_ids = frozenset({"github", "skills-sh", "clawhub", ...})
if _index_available and sid in _api_source_ids:
    continue  # 自定义 tap 不在索引中，永远被跳过
```

所以无论 `skills/hello-hermes/SKILL.md` 还是 `skills/category/skill-name/SKILL.md`，自定义 tap 的技能都无法通过 `search` 或 `browse` 发现。

### 不影响使用

`install` 完全独立于索引，通过完整路径直接下载：

```bash
# 安装（路径格式：owner/repo/skills/category/skill-name）
hermes skills install 13420948160/hermes-skills/skills/hello-hermes

# 强制重装
hermes skills install 13420948160/hermes-skills/skills/hello-hermes --force
```

`hermes skills list` 也能看到已安装的技能。日常流程不受影响。

## 默认 Taps

Hermes 默认包含以下官方 taps：

| Repo | 说明 |
|------|------|
| `openai/skills` | OpenAI 精选技能 |
| `anthropics/skills` | Anthropic 技能 |
| `huggingface/skills` | HuggingFace 技能 |
| `NVIDIA/skills` | NVIDIA 官方技能 |

## 验证清单

新建技能后，确认以下事项：

- [ ] SKILL.md 文件以 `---` 开头（无前导空白）
- [ ] frontmatter 包含 `name`、`description`、`version`、`author`、`license`、`metadata`
- [ ] `description` 字段 ≤ 1024 字符
- [ ] 技能目录结构正确
- [ ] 已推送到 GitHub
- [ ] `hermes skills install` 安装成功
- [ ] `/skill <name>` 加载无报错