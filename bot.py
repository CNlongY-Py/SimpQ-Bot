# ------导入运行库-------
import logging
import time
import os
import importlib
import _thread
import libs
import requests
import re
import logging.handlers
# ------公共变量区-------
loglevel = logging.INFO  # 日志等级
debug = True  # debug模式
initHost = "127.0.0.1"  # 监听服务器HOST
initPort = 5701  # 监听服务器端口
version = "c0.1-RC1"  # 版本号
thread = True  # 多线程选项
botstatus = False # 检测Bot是否离线(Bug很多,强烈不建议使用)

# ------内置函数区-------
def replacestr(msg, uid=0, gid=0):  # 文字渲染模板
    msg = msg.replace("{{time}}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if gid:
        msg = msg.replace("{{gid}}", str(gid))
        msg = msg.replace("{{gname}}", libs.getGroupInfo(gid)["group_name"])
    if uid:
        msg = msg.replace("{{uid}}", str(uid))
        msg = msg.replace("{{uname}}", libs.getStargerInfo(uid)["nickname"])
    if uid and gid:
        msg = msg.replace("{{ucard}}", libs.getGroupUserInfo(gid, uid)["card"])
    return msg


def disloadLog(debug=True):  # 控制接收输出
    if debug:
        state = False
    else:
        state = True
    logging.getLogger('werkzeug').disabled = state
    logging.getLogger("apscheduler.executors.default").disabled = state
    logging.getLogger("urllib3.connectionpool").disabled = state
    logging.getLogger("apscheduler.scheduler").disabled = state


def getLog(name):  # 获取日志实例,初始化日志输出
    logger = logging.getLogger(name)  # 获得logging实例
    if debug:
        logger.setLevel(logging.DEBUG)  # DEBUG模式
    else:
        logger.setLevel(loglevel)  # 未开DEBUG模式下的日志等级
    formator = logging.Formatter(fmt="%(asctime)s[%(levelname)s][%(name)s]:%(message)s", datefmt="%Y-%m-%d-%X")
    sh = logging.StreamHandler()
    fh = logging.handlers.TimedRotatingFileHandler(filename="./logs/{}.log".format(time.strftime("%Y-%m-%d", time.localtime())), when='MIDNIGHT',
                                           interval=1, backupCount=3)
    fh.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")

    if not logger.handlers:
        sh.setFormatter(formator)
        logger.addHandler(sh)
        fh.setFormatter(formator)
    return logger


def checkUpdate():  # 检查更新(预计于下个版本发布)
    return "c0.1-RC1"


# ------核心函数区------
def createThread(name, data):  # 线程创建器
    return _thread.start_new_thread(name, data)

def getStatus():
    log=getLog("BotStatus")
    while True:
        try:
            requests.get(libs.ip+"/get_status")
        except:
            log.warning("Bot已离线,请检查是否IP配置错误")
        time.sleep(3)
def loadPlugLibs(list):
    log = getLog("loadLibs")
    libslist = {}
    pluglibs = os.listdir("./pluglibs")
    for i in list:
        if pluglibs.count(i + ".py") == 0:
            log.error("插件依赖加载失败,缺少依赖%s" % (i))
            exit(1)
        else:
            libslist[i] = importlib.import_module("pluglibs." + i)
    return libslist


def runPlugin(getPlugin, rjson, type, log):  # 为插件创建线程
    bot = importlib.import_module("libs")
    getPlugin.libs = loadPlugLibs(getPlugin.PLUGINFO["libs"])
    if type == "message":
        getPlugin.message(rjson, log, bot)
    elif type == "notice":
        try:
            getPlugin.notice(rjson, log, bot)
        except:
            log.debug("未找到notice响应函数,已跳过")
    elif type == "request":
        try:
            getPlugin.request(rjson, log, bot)
        except:
            log.debug("未找到request响应函数,已跳过")
    elif type == "init":
        getPlugin.main(log, bot)


def pluginLoad(name):  # 返回插件实例
    return importlib.import_module("plugins." + name)


def loadplugin(rjson, type):  # 载入插件
    pluginslist = os.listdir("./plugins")
    for i in pluginslist:
        name = i.split(".")[0]
        if i.find("disload") == -1 and i != "__pycache__":
            getPlugin = pluginLoad(name)
            log = getLog(getPlugin.PLUGINFO["name"])
            if thread:
                createThread(runPlugin, (getPlugin, rjson, type, log))
            else:
                runPlugin(getPlugin, rjson, type, log)


def initRun():  # 初始化运行
    logo = """
        ====================================================================

              /$$$$$$  /$$                                  /$$$$$$ 
             /$$__  $$|__/                                 /$$__  $$
            | $$  \__/ /$$ /$$$$$$/$$$$   /$$$$$$         | $$  \ $$
            |  $$$$$$ | $$| $$_  $$_  $$ /$$__  $$ /$$$$$$| $$  | $$
             \____  $$| $$| $$ \ $$ \ $$| $$  \ $$|______/| $$  | $$
             /$$  \ $$| $$| $$ | $$ | $$| $$  | $$        | $$/$$ $$
            |  $$$$$$/| $$| $$ | $$ | $$| $$$$$$$/        |  $$$$$$/
             \______/ |__/|__/ |__/ |__/| $$____/          \____ $$$
                                        | $$                    \__/
                                        | $$                        
                                        |__/                        

        ====================================================================
        """
    print(logo)
    log = getLog("init")
    log.info("当前版本 %s" % (version))
    log.info("正在自检")
    if checkUpdate() != version:
        log.warning("有新版本可用(%s),是否更新" % (checkUpdate()))
    getfile = os.listdir("./")
    if getfile.count("go-cqhttp") == 0:
        log.error("未找到go-cqhttp文件夹")
        exit(1)
    if getfile.count("plugins") == 0:
        log.error("未找到plugins文件夹")
        exit(1)
    log.info("自检完毕")
    if botstatus:
        log.info("Bot状态检测器已启动")
        createThread(getStatus,())
    log.info("初始化插件")
    loadplugin(0, "init")
    log.info("开始监听消息")


def initData(json):  # 处理消息数据
    time = json["time"]
    ptype = json["post_type"]
    if ptype == "message":
        msgtype = json["message_type"]
        if msgtype == "private":
            mid = json["message_id"]
            uid = json["user_id"]
            msg = json["message"]
            rjson = {"mid": mid, "uid": uid, "msg": msg, "time": time, "rawdata": json,
                     "msgtype": msgtype}
            loadplugin(rjson, ptype)
        elif msgtype == "group":
            subtype = json["sub_type"]
            mid = json["message_id"]
            uid = json["user_id"]
            msg = json["message"]
            gid = json["group_id"]
            rjson = {"subtype": subtype, "mid": mid, "uid": uid, "msg": msg, "gid": gid, "time": time, "rawdata": json,
                     "msgtype": msgtype}
            loadplugin(rjson, ptype)
    elif ptype == "notice":
        ntype = json["notice_type"]
        if ntype == "friend_recall":
            time = json["time"]
            uid = json["user_id"]
            mid = json["message_id"]
            rjson = {"time": time, "uid": uid, "mid": mid, "ntype": ntype, "rawdata": json}
        elif ntype == "group_recall":
            gid = json["group_id"]
            uid = json["user_id"]
            mid = json["message_id"]
            opid = json["operator_id"]
            rjson = {"time": time, "uid": uid, "mid": mid, "ntype": ntype, "gid": gid, "opid": opid, "rawdata": json}
        elif ntype == "group_increase":
            subtype = json["sub_type"]
            gid = json["group_id"]
            uid = json["user_id"]
            opid = json["operator_id"]
            rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "opid": opid, "rawdata": json,
                     "subtype": subtype}
        elif ntype == "group_decrease":
            subtype = json["sub_type"]
            gid = json["group_id"]
            uid = json["user_id"]
            opid = json["operator_id"]
            rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "opid": opid, "rawdata": json,
                     "subtype": subtype}
        elif ntype == "group_admin":
            subtype = json["sub_type"]
            gid = json["group_id"]
            uid = json["user_id"]
            rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "rawdata": json, "subtype": subtype}
        elif ntype == "group_upload":
            gid = json["group_id"]
            uid = json["user_id"]
            file = json["file"]
            rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "rawdata": json, "file": file}
        elif ntype == "group_ban":
            subtype = json["sub_type"]
            gid = json["group_id"]
            uid = json["user_id"]
            opid = json["operator_id"]
            bantime = json["duration"]
            rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "opid": opid, "rawdata": json,
                     "subtype": subtype, "bantime": bantime}
        elif ntype == "friend_add":
            uid = json["user_id"]
            rjson = {"time": time, "uid": uid, "ntype": ntype, "rawdata": json}
        elif ntype == "notify":
            subtype = json["sub_type"]
            if subtype == "lucky_king":
                tid = json["target_id"]
                gid = json["group_id"]
                uid = json["user_id"]
                subtype = json["sub_type"]
                rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "rawdata": json, "subtype": subtype,
                         "tid": tid}
            elif subtype == "honor":
                gid = json["group_id"]
                uid = json["user_id"]
                subtype = json["sub_type"]
                honortype = json["honor_type"]
                rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "rawdata": json, "subtype": subtype,
                         "honortype": honortype}
            elif subtype == "title":
                gid = json["group_id"]
                uid = json["user_id"]
                title = json["title"]
                rjson = {"time": time, "uid": uid, "ntype": ntype, "gid": gid, "rawdata": json, "subtype": subtype,
                         "title": title}
        elif ntype == "essence":
            subtype = json["sub_type"]
            gid = json["group_id"]
            opid = json["operator_id"]
            sid = json["sender_id"]
            rjson = {"time": time, "ntype": ntype, "gid": gid, "opid": opid, "rawdata": json,
                     "subtype": subtype, "sid": sid}
        if rjson:
            loadplugin(rjson, ptype)
    elif ptype == "request":
        rtype = json["request_type"]
        if rtype == "friend":
            uid = json["user_id"]
            comment = json["comment"]
            flag = json["flag"]
            rjson = {"time": time, "rawdata": json, "rtype": rtype, "uid": uid, "comment": comment, "flag": flag}
        elif rtype == "group":
            subtype = json["sub_type"]
            gid = json["group_id"]
            uid = json["user_id"]
            comment = json["comment"]
            flag = json["flag"]
            rjson = {"time": time, "rawdata": json, "rtype": rtype, "uid": uid, "comment": comment, "flag": flag,
                     "subtype": subtype, "gid": gid}
        loadplugin(rjson, ptype)
