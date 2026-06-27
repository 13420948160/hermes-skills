# ehz-iiot-device

极联平台设备接入 CLI，支持设备列表查询、属性数据获取、设备反控、实时数据批量获取。

## 快速开始

```bash
cd skills/ehz-iiot-device
cp .env.example .env   # 编辑 .env 填入实际值
python scripts/client.py --help
```

## 常用命令

| 操作 | 命令 |
|------|------|
| 设备列表 | `python scripts/client.py get-devices` |
| 设备列表（在线） | `python scripts/client.py get-devices --online 1` |
| 关键字搜索 | `python scripts/client.py get-devices --keyword 温度` |
| 实时数据 | `python scripts/client.py get-real-time-data --attrs <设备编号>.<属性ID>` |
| 设备反控 | `python scripts/client.py set-data --attr <设备编号>.<属性ID> --value <值>` |
| 设备实时状态 | `python scripts/client.py get-equipment-rt-status --eids <eid1>,<eid2>` |
| 按标签查设备 | `python scripts/client.py get-devices-by-tag --tag-id <ID> --keyword "" --page-index 1 --page-size 20` |
| 告警历史 | `python scripts/client.py get-alarm-history --area-id <ID> --page-index 1 --page-size 20` |
| 历史数据 | `python scripts/client.py get-history-data --eid <EID> --oids <属性1>,<属性2> --start-time <ISO> --end-time <ISO> --interval 3600000 --page-index 1 --page-size 100` |

## 环境变量

| 变量 | 说明 |
|------|------|
| API_URL | API 服务器地址 |
| ACCOUNT_ID | 极联平台账号 |
| SECRET_ID | 密钥ID |
| SECRET_KEY | 密钥KEY |
| TOKEN_VALID_SECONDS | token 有效期（秒），默认 900 |

详见 [SKILL.md](./SKILL.md)。
