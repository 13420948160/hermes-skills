#!/usr/bin/env python3
"""一键生成 SKILL.md"""
import argparse
import os
import sys

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

DESCRIPTION = "ILCP 审批流技能，支持发起审批流、查询审批状态、撤销审批、获取完成记录。"

PARAM_MAPPING = {}

CMD_ALIASES = {
    "get-flow-state": "获取审批流实例状态",
    "repeal-flow": "撤销审批流",
    "get-finish-record": "获取审批流完成记录",
}

EP_NAME_TO_CMD = {
    "发起审批流": "initiate-flow",
    "获取审批流实例状态": "get-flow-state",
    "撤销审批流": "repeal-flow",
    "获取审批流完成记录": "get-finish-record",
}



def main():
    parser = argparse.ArgumentParser(description="生成 SKILL.md")
    parser.add_argument("--api-docs", default="references/api_docs.md", help="接口文档路径")
    parser.add_argument("--output", default="SKILL.md", help="SKILL.md 输出路径")
    parser.add_argument("--skill-name", default="ehz-ilcp-workflow", help="skill 名称")
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
