"""SKILL.md 生成器"""
import json
import os
import re

from api_parser import ApiDocsParser


def _to_cmd_name(name: str) -> str:
    """中文名称转 CLI 命令名"""
    name = re.sub(r"^[\d\.]+\s*", "", name)
    return re.sub(r"[\W_]+", "-", name).lower()


def _cli_param_name(name: str, param_mapping: dict) -> str:
    """API param name -> CLI param name"""
    mapped = param_mapping.get(name, name)
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", mapped)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


def _deduplicate_params(params: list, param_mapping: dict) -> list:
    """去除重复的 CLI 参数"""
    seen = set()
    result = []
    for p in params:
        cli_name = _cli_param_name(p.name, param_mapping)
        if cli_name in seen:
            continue
        seen.add(cli_name)
        result.append(p)
    return result


def _format_notes(notes: str) -> str:
    """将注意事项转换为 Markdown 列表格式"""
    lines = notes.strip().splitlines()
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("-"):
            result.append(line)
        elif re.match(r"^\d+\.", line):
            result.append(line)
        else:
            result.append(f"- {line}")
    return "\n".join(result)


def generate_skill_md(
    api_docs_path: str,
    output_path: str,
    skill_name: str,
    description: str,
    env_vars: list[tuple[str, str, str]] = None,
    param_mapping: dict = None,
    ep_name_to_cmd: dict = None,
    cli_script_path: str = "scripts/client.py",
):
    """
    从 api_docs.md 动态生成 SKILL.md

    Args:
        api_docs_path: api_docs.md 文件路径
        output_path: SKILL.md 输出路径
        skill_name: skill 名称
        description: skill 描述
        env_vars: 环境变量列表 [(变量名, 说明, 示例), ...]
        param_mapping: 参数映射表 {API名: CLI名}
    """
    parser = ApiDocsParser()
    endpoints = parser.parse_file(api_docs_path)
    param_mapping = param_mapping or {}
    ep_name_to_cmd = ep_name_to_cmd or {}

    lines = []
    lines.append("---")
    lines.append(f"name: {skill_name}")
    lines.append(f"description: {description}")
    lines.append("license: MIT")
    lines.append("metadata:")
    lines.append('  author: "ehz"')
    lines.append('  version: "1.0.0"')
    lines.append("---")
    lines.append("")
    lines.append(f"# {skill_name} Tool")
    lines.append("")
    lines.append(description)
    lines.append("")
    lines.append("## When to Use")
    lines.append("")
    for ep in endpoints:
        lines.append(f"- {ep.description}")
    lines.append("")
    lines.append("## 环境配置")
    lines.append("")
    lines.append("使用前需要配置以下环境变量（参考 `.env.example` 模板）：")
    lines.append("")
    lines.append("| 环境变量 | 说明 | 示例 |")
    lines.append("|--------|------|------|")
    if env_vars:
        for var_name, var_desc, var_example in env_vars:
            lines.append(f"| {var_name} | {var_desc} | {var_example} |")
    else:
        lines.append("| API_URL | API 地址 | your_api_url_here |")
        lines.append("| ACCOUNT_ID | 用户ID（AccountId） | your_account_id_here |")
        lines.append("| SECRET_ID | 密钥ID（SecretId） | your_secret_id_here |")
        lines.append("| SECRET_KEY | 密钥KEY（SecretKey） | your_secret_key_here |")
        lines.append("| TOKEN_VALID_SECONDS | token 有效期（秒） | 900 |")
    lines.append("")
    lines.append("**认证说明**：`TOKEN` 无需手动配置，客户端启动时会自动调用 `/ESBREST/faas/code/getAccessToken` 接口换取，token 有效期 15 分钟，客户端会自动刷新。")
    lines.append("")
    lines.append("**快速开始**：复制 `.env.example` 为 `.env` 并填入实际值即可。")
    lines.append("")
    lines.append("## 能力清单")
    lines.append("")

    for ep in endpoints:
        cmd = ep_name_to_cmd.get(ep.name, _to_cmd_name(ep.name))
        lines.append(f"### {ep.index}. {ep.name}")
        lines.append("")
        lines.append(ep.description)
        lines.append("")
        lines.append("```bash")
        lines.append(f"python {cli_script_path} {cmd}")
        # 列出所有别名（反向查找）
        aliases = [a for a, n in (ep_name_to_cmd or {}).items() if n == cmd and a != cmd]
        if aliases:
            for alias in aliases:
                lines.append(f"python {cli_script_path} {alias}  # 别名")
        lines.append("```")
        lines.append("")

        # 去重后的参数
        unique_params = _deduplicate_params(ep.parameters, param_mapping)
        if unique_params:
            lines.append("**请求参数**:")
            lines.append("| 参数 | 类型 | 必填 | 说明 |")
            lines.append("|------|------|------|------|")
            for p in unique_params:
                req = "是" if p.required else "否"
                lines.append(f"| {p.name} | {p.param_type} | {req} | {p.description} |")
            lines.append("")

        if ep.request_example:
            lines.append("**入参示例**:")
            lines.append("```json")
            lines.append(json.dumps(ep.request_example, ensure_ascii=False, indent=4))
            lines.append("```")
            lines.append("")

        if ep.response_example:
            lines.append("**返回示例**:")
            lines.append("```json")
            lines.append(json.dumps(ep.response_example, ensure_ascii=False, indent=4))
            lines.append("```")
            lines.append("")

        if ep.notes:
            lines.append("**注意事项**:")
            lines.append(_format_notes(ep.notes))
            lines.append("")

        lines.append("---")
        lines.append("")

    lines.append("## Output Format")
    lines.append("")
    lines.append("脚本统一输出 JSON 格式：")
    lines.append("```json")
    lines.append('{ "errorCode": 0, "errorMsg": "success", "return": { ... } }')
    lines.append("```")
    lines.append("")
    lines.append("## 错误码")
    lines.append("")
    lines.append("| 错误码 | 说明 |")
    lines.append("|--------|------|")
    lines.append("| 0 | 成功 |")
    lines.append("| 400 | 请求参数错误 |")
    lines.append("| 401 | 认证失败 |")
    lines.append("| 404 | 设备不存在 |")
    lines.append("| 408 | 请求超时 |")
    lines.append("| 500 | 服务器内部错误 |")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"SKILL.md 已生成: {output_path}")
