import os
import bot
import time
with open("./logs/%s.log" % time.strftime("%Y-%m-%d", time.localtime()), "a", encoding="utf-8") as f:
    f.write("==============================\n")
bot.initRun()  # 初始化运行
for M in os.popen("python -m main"):  # 启动监听器
    print(M.replace("\n", ""))
