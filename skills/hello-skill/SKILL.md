---
name: hello-skill
description: Use when the user wants to test the Hermes skills hub connection. A simple test skill that demonstrates skill structure and verifies your custom hub is reachable.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [test, demo, hello-world]
    related_skills: []
---

# Hello Skill

## Overview

A test skill to verify your custom Hermes Skills Hub is properly configured and reachable. This skill demonstrates the standard skill structure and can be used as a template for creating new skills.

## When to Use

- User asks to test the skills hub connection
- User wants a starting template for a new skill
- Verifying `hermes skills tap add` worked correctly

## What This Skill Does

When loaded, it prints a test confirmation message. The skill structure follows the standard Hermes SKILL.md format with proper frontmatter.

## Skill Structure

```
skills/
└── <category>/
    └── <skill-name>/
        └── SKILL.md       # Required: skill definition
        └── references/    # Optional: additional docs
        └── scripts/       # Optional: helper scripts
        └── templates/     # Optional: file templates
```

## Creating Your Own Skill

1. Create the directory structure under `skills/<category>/<skill-name>/`
2. Add a `SKILL.md` with proper frontmatter (name, description ≤1024 chars, version, author, license, metadata)
3. Commit and push to your GitHub repo
4. Run `hermes skills install owner/repo:category/skill-name`

## Common Pitfalls

1. **Description too long** — must be ≤ 1024 characters
2. **Missing frontmatter** — file must start with `---` at byte 0
3. **Wrong category** — use existing categories or ask before creating new ones
4. **skills/ tap not refreshed** — new skills may take a few minutes to appear in browse

## Verification Checklist

- [ ] SKILL.md has proper YAML frontmatter
- [ ] `description` field is ≤ 1024 characters
- [ ] File starts with `---` (no leading whitespace)
- [ ] `name`, `version`, `author`, `license`, `metadata` fields all present
- [ ] Committed and pushed to GitHub
- [ ] `hermes skills install` succeeds
- [ ] `/skill hello-skill` loads without error