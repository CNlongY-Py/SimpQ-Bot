import os
import bot

bot.initRun()  # 初始化运行
for M in os.popen("python -m main"):  # 启动监听器
    print(M.replace("\n", ""))
