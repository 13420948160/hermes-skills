#!/usr/bin/env python3
"""一键生成 SKILL.md"""
import argparse
import os
import sys

# 将 skill 根目录加入 import 路径
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _SKILL_ROOT)

from skill_generator import generate_skill_md

ENV_VARS = [
    ("API_URL", "API 地址", "your_api_url_here"),
    ("ACCOUNT_ID", "用户ID（AccountId）", "your_account_id_here"),
    ("SECRET_ID", "密钥ID（SecretId）", "your_secret_id_here"),
    ("SECRET_KEY", "密钥KEY（SecretKey）", "your_secret_key_here"),
    ("TOKEN_VALID_SECONDS", "token 有效期（秒）", "900"),
]

DESCRIPTION = (
    "极联平台设备接入相关技能，用于查询设备列表、设备数据、设备反控及实时数据获取。"
)

PARAM_MAPPING = {
    "page_size": "page",
    "areaId": "areaId",
    "emodelid": "emodelid",
}

# CLI 别名（命令 -> 端点名）
CMD_ALIASES = {
    "get-devices": "获取设备列表",
    "list-devices": "获取设备列表",
    "get-real-time-data": "获取设备实时数据",
    "get-realtime": "获取设备实时数据",
    "set-data": "设备反控（写入数据）",
}

# 端点名 -> CLI 命令名的反向映射
EP_NAME_TO_CMD = {
    "获取设备列表": "get-devices",
    "设备反控（写入数据）": "set-data",
    "获取设备实时数据": "get-real-time-data",
}


def main():
    parser = argparse.ArgumentParser(description="生成 SKILL.md")
    parser.add_argument("--api-docs", default="references/api_docs.md", help="接口文档路径")
    parser.add_argument("--output", default="SKILL.md", help="SKILL.md 输出路径")
    parser.add_argument("--skill-name", default="ehz-iiot-device", help="skill 名称")
    parser.add_argument("--description", default=DESCRIPTION, help="skill 描述")
    args = parser.parse_args()

    generate_skill_md(
        api_docs_path=os.path.join(_SKILL_ROOT, args.api_docs),
        output_path=os.path.join(_SKILL_ROOT, args.output),
        skill_name=args.skill_name,
        description=args.description,
        env_vars=ENV_VARS,
        param_mapping=PARAM_MAPPING,
        ep_name_to_cmd=EP_NAME_TO_CMD,
    )


if __name__ == "__main__":
    main()
