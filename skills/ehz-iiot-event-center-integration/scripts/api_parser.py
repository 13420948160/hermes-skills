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
        sections = re.split(r"(?=^(?:###\s*|#{1,2}\s*)?\d+\.)", content, flags=re.MULTILINE)
        endpoints = []
        for sec in sections:
            if not sec.strip():
                continue
            ep = self._parse_section(sec)
            if ep:
                endpoints.append(ep)
        return endpoints

    def _infer_type_from_value(self, val: any) -> str:
        if isinstance(val, bool):
            return "boolean"
        if isinstance(val, int):
            return "integer"
        if isinstance(val, float):
            return "number"
        if isinstance(val, list):
            return "array"
        if isinstance(val, dict):
            return "object"
        return "string"

    def _parse_json_to_params(self, req_ex: dict) -> list[ApiParam]:
        """从入参 JSON 示例中提取参数"""
        params = []
        for k, v in req_ex.items():
            if k in ("apikey",):
                continue
            params.append(
                ApiParam(
                    name=k,
                    param_type=self._infer_type_from_value(v),
                    required=False,
                    description="",
                    default=str(v) if v is not None else "",
                )
            )
        return params

    def _parse_section(self, text: str) -> ApiEndpoint | None:
        idx_match = re.search(r"^(?:###\s*|#{1,2}\s*)?(\d+)\.\s*(.+)$", text, re.MULTILINE)
        if not idx_match:
            return None
        index = int(idx_match.group(1))
        name = idx_match.group(2).strip()

        path_match = re.search(
            r"\*\*接口地址\*\*:\s*`?(POST|GET|PUT|DELETE)\s+([^`\n]+)`?", text, re.IGNORECASE
        )
        path = ""
        method = "POST"
        if path_match:
            method = path_match.group(1).upper()
            path = path_match.group(2).strip()

        desc_match = re.search(r"\*\*作用\*\*:\s*(.+?)(?:\n|$)", text)
        description = desc_match.group(1).strip() if desc_match else ""

        # 解析接口类型（iiot 或 faas），默认为 iiot
        api_type_match = re.search(r"\*\*接口类型\*\*:\s*(iiot|faas)", text)
        api_type = api_type_match.group(1) if api_type_match else "iiot"

        params = self._parse_params_table(text)
        req_ex = self._parse_json_block(text, r"\*\*入参示例\*\*:")

        if not params and req_ex and isinstance(req_ex, dict):
            params = self._parse_json_to_params(req_ex)

        res_ex = self._parse_json_block(text, r"\*\*返回示例\*\*:")
        notes_match = re.search(
            r"\*\*注意事项\*\*:\s*([\s\S]+?)(?=^###\s|\n---|\Z)", text, re.MULTILINE
        )
        notes = notes_match.group(1).strip() if notes_match else ""

        if req_ex and isinstance(req_ex, dict):
            for p in params:
                if p.default in ("", "空", "无", None) and p.name in req_ex:
                    val = req_ex[p.name]
                    if val is not None:
                        if isinstance(val, bool):
                            p.default = str(val).lower()
                        elif isinstance(val, (int, float)):
                            p.default = str(val)
                        elif isinstance(val, str):
                            p.default = val

        return ApiEndpoint(
            index=index, name=name, method=method, path=path,
            description=description, parameters=params,
            request_example=req_ex, response_example=res_ex, notes=notes,
            api_type=api_type,
        )

    def _parse_params_table(self, text: str) -> list[ApiParam]:
        """解析 Markdown 请求参数表格，逐行纯字符串解析，支持任意列数"""
        params = []

        m = re.search(r"\*\*请求参数\*\*[:：]?\s*\n((?:.|\n)*?)(?=\*\*|$)", text)
        if not m:
            return params
        block = m.group(1)

        # 第一步：找到所有表格行
        table_lines = []
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("|"):
                table_lines.append(line)

        # 判断是否为中文表头标签行
        def is_header_row(cells: list) -> bool:
            if not cells:
                return False
            first = cells[0]
            # 跳过中文表头标签（如 "参数名"）
            header_labels = {
                "参数", "字段", "名称", "类型", "说明", "描述",
                "是否必填", "必填", "默认值", "错误码", ""
            }
            if first in header_labels:
                return True
            # 跳过英文表头标签（首字母小写的单词）
            en_headers = {
                "name", "field", "type", "description", "required", "default", "param"
            }
            if first.lower() in en_headers and len(cells) <= 3:
                return True
            # 跳过：第二列为中文说明（如 "类型"、"说明"）的行（header 行特征）
            if len(cells) >= 2 and re.match(r"^[\u4e00-\u9fff]", cells[1]):
                return True
            return False

        # 第二步：逐行遍历，跳过表头行和分隔行
        for line in table_lines:
            cells = [c.strip() for c in line.split("|")[1:-1]]  # 去掉首尾空串
            valid = [c for c in cells if c]
            if not valid:
                continue
            # 跳过表头行
            if is_header_row(valid):
                continue
            # 跳过纯分隔行
            if all(re.match(r"^[\s|-]+$", c) for c in cells):
                continue
            # 剩余的视为数据行
            params.append(self._make_param_from_cells(cells))

        return [p for p in params if p is not None]

    def _make_param_from_cells(self, cells: list) -> ApiParam | None:
        """从单元格列表构建 ApiParam"""
        # 过滤空单元格，保留有效列
        # 列布局：
        #   [参数名, 类型, 必填, 说明, 默认值]  (5列)
        #   [参数名, 类型, 必填, 说明]           (4列)
        #   [参数名, 类型, 必填]                 (3列)
        #   [参数名, 类型]                       (2列)
        valid = [c for c in cells if c]
        if not valid:
            return None
        name = valid[0]
        if not name:
            return None

        # 已知的中文表头标签（用于排除）
        header_labels = {
            "参数", "字段", "名称", "类型", "说明", "描述",
            "是否必填", "必填", "默认值", "错误码", ""
        }
        if name in header_labels:
            return None

        if len(valid) >= 2:
            param_type = valid[1]
        else:
            param_type = "string"

        required_str = ""
        description = ""
        default = ""

        if len(valid) >= 3:
            required_str = valid[2]
        if len(valid) >= 4:
            description = valid[3]
        if len(valid) >= 5:
            default = valid[4]

        required = required_str in ("是", "必填", "true", "True", "1")

        return ApiParam(
            name=name,
            param_type=param_type,
            required=required,
            description=description,
            default=default,
        )

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
