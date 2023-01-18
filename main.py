from flask import *
import bot

app = Flask(__name__)
# 测试阶段关闭输出接口
# --------------
bot.disloadLog(False)


# bot.disloadLog(debug)
# --------------
@app.route('/', methods=["POST"])
def main():
    bot.initData(request.get_json())
    return ""


app.debug = bot.debug
app.run(host=bot.initHost, port=bot.initPort)
