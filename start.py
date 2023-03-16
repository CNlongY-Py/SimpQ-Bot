import os
import bot
import time
bot.initRun()  # 初始化运行
with open("./logs/{}.log".format(time.strftime("%Y-%m-%d", time.localtime())),"a")as f:
    for M in os.popen("python -m main"):  # 启动监听器
        print(M.replace("\n", ""))
        f.write(M)
