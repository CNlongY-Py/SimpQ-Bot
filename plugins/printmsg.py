PLUGINFO = {
    "name": "PrintMsg",
    "version": "0.0.1",
    "author": "CNlongY",
    "libs": []
}


def main(log, bot):
    log.info("消息输出插件载入成功")


def message(json, log, bot):
    type = json["msgtype"]
    if type == "group":
        gid = json["gid"]
        uid = json["uid"]
        msg = json["msg"]
        log.info(bot.botlib.replacestr("[群聊消息]<{{gname}}>{{uname}}({{ucard}}):%s" % (msg), gid=gid, uid=uid))
    elif type == "private":
        uid = json["uid"]
        msg = json["msg"]
        log.info(bot.botlib.replacestr("[私聊消息]{{uname}}:%s" % (msg), uid=uid))
