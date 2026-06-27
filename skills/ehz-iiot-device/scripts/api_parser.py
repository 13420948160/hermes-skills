"""极联平台 API 文档解析器"""
import json
import re

from base.parser import BaseMarkdownParser, ApiEndpoint, ApiParam


class ApiDocsParser(BaseMarkdownParser):
    """解析极联平台 api_docs.md 格式的 API 文档"""

    def parse_file(self, path: str) -> list[ApiEndpoint]:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        return self.parse_string(content)

    def parse_string(self, content: str) -> list[ApiEndpoint]:
        # 按 ### N. 分割各接口章节
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
        # 提取序号
        idx_match = re.search(r"^###\s*(\d+)\.\s*(.+)$", text, re.MULTILINE)
        if not idx_match:
            return None
        index = int(idx_match.group(1))
        name = idx_match.group(2).strip()

        # 提取接口地址
        path_match = re.search(r"\*\*接口地址\*\*:\s*`?(POST|GET|PUT|DELETE)\s+([^`\n]+)`?", text)
        path = ""
        method = "POST"
        if path_match:
            method = path_match.group(1)
            path = path_match.group(2).strip()

        # 提取作用（描述）
        desc_match = re.search(r"\*\*作用\*\*:\s*(.+?)(?:\n|$)", text)
        description = desc_match.group(1).strip() if desc_match else ""

        # 提取请求参数表格
        params = self._parse_params_table(text)

        # 提取入参示例
        req_ex = self._parse_json_block(text, r"\*\*入参示例\*\*:")
        # 提取返回示例
        res_ex = self._parse_json_block(text, r"\*\*返回示例\*\*:")
        # 提取注意事项
        notes_match = re.search(r"\*\*注意事项\*\*:\s*([\s\S]+?)(?=^###\s|\n---|\Z)", text, re.MULTILINE)
        notes = notes_match.group(1).strip() if notes_match else ""

        # 用 request_example 补全参数默认值（JSON 中的值已是正确类型）
        if req_ex and isinstance(req_ex, dict):
            for p in params:
                if p.default in ("", "空", "无", None) and p.name in req_ex:
                    val = req_ex[p.name]
                    # JSON 中已是 Python 原生类型，直接使用
                    if isinstance(val, (bool, int, float)):
                        p.default = str(val)
                    elif isinstance(val, str):
                        p.default = val

        return ApiEndpoint(
            index=index,
            name=name,
            method=method,
            path=path,
            description=description,
            parameters=params,
            request_example=req_ex,
            response_example=res_ex,
            notes=notes,
        )

    def _parse_params_table(self, text: str) -> list[ApiParam]:
        """解析 Markdown 请求参数表格（仅解析 **请求参数** 下的表格）"""
        params = []

        # 提取 **请求参数** 标题到下一个 ** 标题 之间内容
        m = re.search(r"\*\*请求参数\*\*[:：]?\s*\n((?:.|\n)*?)(?=\*\*|$)", text)
        if not m:
            return params
        params_block = m.group(1)

        # 匹配参数表格行（支持 4 列和 5 列，第 5 列为默认值）
        rows = re.findall(
            r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|(?:\s*([^|]+?)\s*\|)?",
            params_block,
            re.MULTILINE,
        )
        for row in rows:
            col = [c.strip() for c in row]
            if len(col) < 4:
                continue
            name = col[0]
            # 跳过：表头行、分隔行、空行
            skip_patterns = (
                r"^-+$",          # 纯分隔行 |------|------|
                r"^(参数|字段|名称|name)$",
                r"^(类型|type)$",
                r"^(说明|描述|description)$",
                r"^(是否必填|required)$",
                r"^(默认值|default)$",
                r"^(错误码|errorCode)$",
                r"^$",             # 空单元格
            )
            if any(re.match(p, name, re.IGNORECASE) for p in skip_patterns):
                continue
            param_type = col[1]
            required_str = col[2]
            description = col[3] if len(col) > 3 else ""
            # 尝试从第5列获取默认值
            default = col[4].strip() if len(col) > 4 else ""
            required = required_str in ("是", "必填", "true", "True", "1")
            params.append(
                ApiParam(
                    name=name,
                    param_type=param_type,
                    required=required,
                    description=description,
                    default=default,
                )
            )
        return params

    def _parse_json_block(self, text: str, marker: str) -> dict | None:
        """从 markdown 中提取 JSON 代码块"""
        pattern = re.escape(marker) + r"\s*```(?:json)?\s*([\s\S]+?)\s*```"
        match = re.search(pattern, text)
        if not match:
            return None
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
