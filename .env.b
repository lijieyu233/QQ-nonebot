# NoneBot2 驱动器配置


# QQ 机器人配置
QQ_BOTS='[
  {
    "id": "102377271",
    "token": "pEaCP72G1CgXON0NlUjFOezUiGu7H9sN",
    "secret": "tuvwxyz13579BDFILORUXaeimquy26BG",
    "intent": {
      "c2c_group_at_messages": true
    }
  }
]'

QQ_IS_SANDBOX=true
DRIVER=~httpx+~websockets
HOST=0.0.0.0  # 配置 NoneBot 监听的 IP / 主机名
PORT=23333  # 配置 NoneBot 监听的端口
SUPERUSERS=["123456789","987654321"] # 配置超级用户
COMMAND_START=["/"]  # 配置命令起始字符
COMMAND_SEP=["."]  # 配置命令分割字符
