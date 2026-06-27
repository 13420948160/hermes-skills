"""ILCP 审批流 API 文档解析器"""
import json
import re

from base.parser import BaseMarkdownParser, ApiEndpoint, ApiParam


class IlcpApiDocsParser(BaseMarkdownParser):
    """解析 ILCP 审批流 api_docs.md 格式的 API 文档"""

    def parse_file(self, path: str) -> list[ApiEndpoint]:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        return self.parse_string(content)

    def parse_string(self, content: str) -> list[ApiEndpoint]:
        sections = re.split(r"(?=^### \d+\.)", content, flags=re.MULTILINE)
        endpoints = []
        for sec in sections:
            if not sec.strip():
                continue
            ep = self._parse_section(sec)
            if ep:
                endpoints.append(ep)
        return endpoints

    def _parse_section(self, text: str) -> ApiEndpoint | None:
        idx_match = re.search(r"^###\s*(\d+)\.\s*(.+)$", text, re.MULTILINE)
        if not idx_match:
            return None
        index = int(idx_match.group(1))
        name = idx_match.group(2).strip()

        # 提取接口地址（支持带 / 前缀和不带前缀的格式）
        path_match = re.search(r"\*\*接口地址\*\*:\s*`?(POST|GET|PUT|DELETE)\s+(/[^\n`]+)`?", text)
        if path_match:
            method = path_match.group(1)
            path = path_match.group(2).strip().lstrip("/")
        else:
            path_match2 = re.search(r"\*\*接口地址\*\*:\s*/?([^\n`]+)", text)
            method = "POST"
            path = path_match2.group(1).strip() if path_match2 else ""

        # 提取接口说明
        desc_match = re.search(r"\*\*(?:作用|接口说明)\*\*:\s*(.+?)(?:\n|$)", text)
        description = desc_match.group(1).strip() if desc_match else ""

        params = self._parse_params_table(text)
        req_ex = self._parse_json_block(text, "**请求示例**")
        res_ex = self._parse_json_block(text, "**返回示例**")

        # 提取注意事项
        notes_parts = []
        notes_match = re.search(r"\*\*注意事项\*\*:\s*([\s\S]+?)(?=^###\s|^\-\-\-|\Z)", text, re.MULTILINE)
        if notes_match:
            notes_parts.append(notes_match.group(1).strip())

        # 提取接口级错误码
        err_match = re.search(r"\*\*错误码\*\*:\s*([\s\S]+?)(?=^###|\n---)", text, re.MULTILINE)
        if err_match:
            notes_parts.append("接口错误码:\n" + err_match.group(1).strip())

        notes = "\n".join(notes_parts)

        # 用 request_example 补全参数默认值
        if req_ex and isinstance(req_ex, dict):
            for p in params:
                if p.default in ("", "空", "无", None) and p.name in req_ex:
                    val = req_ex[p.name]
                    if isinstance(val, (bool, int, float)):
                        p.default = str(val)
                    elif isinstance(val, str):
                        p.default = val

        return ApiEndpoint(
            index=index,
            name=name,
            method=method,
            path="/" + path,
            description=description,
            parameters=params,
            request_example=req_ex,
            response_example=res_ex,
            notes=notes,
        )

    def _parse_params_table(self, text: str) -> list[ApiParam]:
        params = []
        # 定位请求参数表格区域（使用多行模式，^ 匹配行首）
        m = re.search(r"\*\*请求参数\*\*:?\s*\n\s*\n((?:.|\n)*?)(?=^\*\*|^\-\-\-|\Z)", text, re.MULTILINE)
        if not m:
            return params
        params_block = m.group(1)

        rows = re.findall(
            r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|(?:\s*([^|]+?)\s*\|)?",
            params_block, re.MULTILINE)
        for row in rows:
            col = [c.strip() for c in row]
            if len(col) < 4:
                continue
            name = col[0]
            skip_patterns = (
                r"^-+$",
                r"^(参数名|字段|名称|name|参数|字段名)$",
                r"^(类型|type)$",
                r"^(说明|描述|description)$",
                r"^(是否必填|required)$",
                r"^(默认值|default)$",
                r"^(错误码|errorCode)$",
                r"^$",
            )
            if any(re.match(p, name, re.IGNORECASE) for p in skip_patterns):
                continue
            param_type = col[1]
            required_str = col[2]
            description = col[3] if len(col) > 3 else ""
            default = col[4].strip() if len(col) > 4 else ""
            required = required_str in ("是", "必填", "true", "True", "1")
            params.append(ApiParam(
                name=name,
                param_type=param_type,
                required=required,
                description=description,
                default=default,
            ))
        return params

    def _parse_json_block(self, text: str, marker: str) -> dict | None:
        # marker 后支持: + 换行，然后是 ```json 代码块
        pattern = re.escape(marker) + r":?\s*\n\s*```(?:json)?\s*([\s\S]+?)\s*```"
        match = re.search(pattern, text)
        if not match:
            return None
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
