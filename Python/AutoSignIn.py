"""
使用MPL2.0公开代码
雨云官方文档：https://apifox.com/apidoc/shared-a4595cc8-44c5-4678-a2a3-eed7738dab03/api-69942942
"""
import random
from datetime import datetime, timedelta, timezone

import sys
from textwrap import dedent

import requests
import json
import os

config = {}

# 生成配置文件
if not os.path.exists("/config.txt"):
    lines = ["api_key="]
    f = open("/config.txt", "w")
    f.writelines(line + '\n' for line in lines)
    f.close()
    input("配置文件已创建！现在，你需要前往项目文件夹或者程序文件夹找到config.txt并按照要求编辑（按回车键退出）")
    sys.exit(1)
else:
    f = open('/config.txt')
    for line in f.readlines():
        split = line.split("=")
        config[split[0]] = split[1].strip()

# API的Headers
url = "https://api.v2.rainyun.com/user/"
payload = {}
headers = {
    'x-api-key': f"{config['api_key']}",
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

response = requests.request("GET", url, headers=headers)
print(dedent(f"""请确认你的账户信息：
昵称：{json.loads(response.text)['data']['Name']}
邮箱：{json.loads(response.text)['data']['Email']}
上次登录地点：{json.loads(response.text)['data']['LastLoginArea']}
若准确无误请输入y
"""))
yes = ["yes", "y", "是"]
answer = input("上述信息是否准确无误？")
if answer in yes:
    print("您已确认信息匹配，计划任务将在每天8:00~12:00执行！（以北京时间（GMT+8）时间为准）")
    # API头部
    url = "https://api.v2.rainyun.com/user/reward/tasks"
    payload = json.dumps({
        "task_name": "每日签到"
    })
    headers = {
        'x-api-key': f"{config['api_key']}",
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    hour = 0
    minute = 0
    second = 0
    while True:
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        beijing_now = utc_now.astimezone(SHA_TZ)
        if hour == 0 or (beijing_now.hour == hour
                         and beijing_now.minute == minute
                         and beijing_now.second == second):
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            hour = random.randint(8, 12)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            print(f"执行完毕！下次执行时间为今日或次日{hour:02d}:{minute:02d}:{second:02d}！")
else:
    print("由于信息不匹配，计划任务将不执行！")
    sys.exit(1)
