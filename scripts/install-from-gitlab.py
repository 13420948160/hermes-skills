#!/usr/bin/env python3
"""从私有 GitLab 仓库安装技能到本地。"""
import json
import os
import sys
import urllib.request

GITLAB_HOST = "http://10.10.11.4:30690"
PROJECT_ENCODED = "product%2Fiot%2Fiottool%2Fskills"
BRANCH = "develop"
SKILLS_DIR = os.path.expanduser("~/.hermes/skills")


def get_token():
    token = os.environ.get("GITLAB_TOKEN")
    if token:
        return token
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            marker = "GITLAB_TOKEN="
            if line.startswith(marker):
                return line[len(marker):]
    return None


def gitlab_get(path):
    token = get_token()
    if not token:
        print("Error: GITLAB_TOKEN not found")
        sys.exit(1)
    parts = [GITLAB_HOST, "api/v4/projects", PROJECT_ENCODED, path]
    url = "/".join(parts)
    req = urllib.request.Request(url)
    req.add_header("PRIVATE-TOKEN", token)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read().decode()


def list_skills():
    text = gitlab_get("repository/files/skills-catalog.json/raw?ref=" + BRANCH)
    data = json.loads(text)
    return data.get("skills", [])


def install(name):
    target_dir = os.path.join(SKILLS_DIR, name)
    os.makedirs(target_dir, exist_ok=True)
    file_path = "repository/files/skills%2F" + name + "%2FSKILL.md/raw?ref=" + BRANCH
    content = gitlab_get(file_path)
    with open(os.path.join(target_dir, "SKILL.md"), "w") as f:
        f.write(content)
    print("  OK " + name)


if __name__ == "__main__":
    token = get_token()
    if not token:
        print("Error: GITLAB_TOKEN not set")
        sys.exit(1)

    skills = list_skills()

    if len(sys.argv) > 1:
        name = sys.argv[1]
        for s in skills:
            if s["name"] == name:
                install(name)
                sys.exit(0)
        print("Not found: " + name)
        sys.exit(1)

    print()
    print("Skills Hub - " + str(len(skills)) + " skills")
    print()
    for i, s in enumerate(skills, 1):
        print("  " + str(i) + ". " + s["name"] + ": " + s["description"])
    print()
    print("Usage: python3 install-from-gitlab.py <skill-name>")
