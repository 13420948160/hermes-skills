#!/usr/bin/env bash
# 通过 gh-proxy.com 镜像加速 git push（国内网络专用）
# 用法: bash scripts/push-via-proxy.sh
set -e

cd "$(dirname "$0")/.."

echo "=== 使用 gh-proxy.com 镜像推送 ==="
echo ""

# 添加镜像 remote
if ! git remote | grep -q "^ghproxy$"; then
    git remote add ghproxy https://gh-proxy.com/https://github.com/13420948160/hermes-skills.git
fi

git push ghproxy main

echo ""
echo "推送成功！"
echo ""
echo "注意: ghproxy remote 是镜像地址，推送后还需同步到官方 origin："
echo "  git push origin main"
