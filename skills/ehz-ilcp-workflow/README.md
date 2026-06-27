# ehz-ilcp-workflow

ILCP 审批流 CLI，支持发起审批流、查询审批状态、撤销审批、获取完成记录。

## 快速开始

```bash
cd skills/ehz-ilcp-workflow
cp .env.example .env   # 编辑 .env 填入实际值
python scripts/client.py --help
```

## 常用命令

| 操作 | 命令 |
|------|------|
| 发起审批流 | `python scripts/client.py initiate-flow` |
| 查询审批状态 | `python scripts/client.py get-flow-state --bid <实例ID>` |
| 撤销审批 | `python scripts/client.py repeal-flow --bid <实例ID>` |
| 获取完成记录 | `python scripts/client.py get-finish-record --initiator <用户ID> --start-time <开始时间> --end-time <结束时间>` |

## 环境变量

| 变量 | 说明 |
|------|------|
| API_URL | API 服务器地址 |
| ACCOUNT_ID | 极联平台账号 |
| SECRET_ID | 密钥ID |
| SECRET_KEY | 密钥KEY |
| TOKEN_VALID_SECONDS | token 有效期（秒），默认 900 |

详见 [SKILL.md](./SKILL.md)。
