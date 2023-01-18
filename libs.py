# ------导入运行库------
import bot
import requests
import importlib

# ------内置变量------
botlib = importlib.import_module("bot")
ip = "http://127.0.0.1:5700"


# ------go-cqhttp函数------
def HTTP(url):
    http = requests.get(ip + url).json()["data"]
    return http


def sendMsg(msg, gid=0, uid=0):  # 发送消息(若gid未传入则默认私聊,uid相反)
    if gid:
        return HTTP("/send_group_msg?group_id=%s&message=%s" % (gid, bot.replacestr(msg, uid=uid, gid=gid)))
    elif uid:
        return HTTP("/send_private_msg?user_id=%s&message=%s" % (uid, bot.replacestr(msg, uid=uid, gid=gid)))
    else:
        return "[Error][201]错误的传入"


def sendForwardMsg(gid,
                   messages):  # 发送群聊自定义合并消息(详情请看https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9)
    return HTTP("/send_group_forward_msg?group_id=%s&message=%s" % (gid, messages))


def deleteMsg(mid):  # 撤回消息
    return HTTP("/delete_msg?message_id=%s" % (mid))


def getMsg(mid):  # 获取消息
    return HTTP("/get_msg?message_id=%s" % (mid))


def getForwardMsg(mid):  # 获取合并转发消息(字段 mid 对应合并转发中的 id 字段)
    return HTTP("/get_forward_msg?message_id=%s" % (mid))


def getImage(file):  # 获取图片信息
    return HTTP("/get_image?file=%s" % (file))


def makeMsgRead(mid):  # 设置消息已读
    HTTP("/mark_msg_as_read?message_id=%s" % (mid))


def groupKick(gid, uid, rkick="false"):  # 群组踢人(rkick默认为false)
    HTTP("/set_group_kick?group_id=%s&user_id=%s&reject_add_request=%s" % (gid, uid, rkick))


def groupBan(gid, uid, time=30 * 60):  # 设置群组禁言(时长默认30*60秒,传入0表示取消禁言)
    HTTP("/set_group_ban?group_id=%s&user_id=%s&duration=%s" % (gid, uid, time))


def groupBanAll(gid, type="true"):  # 群组全员禁言(默认为开始禁言)
    HTTP("/set_group_whole_ban?group_id=%s&enable=%s" % (gid, type))


def groupSetAdmin(gid, uid, type="true"):  # 群组设置管理员
    HTTP("/set_group_admin?group_id=%s&user_id=%s&enable=%s" % (gid, uid, type))


def groupSetName(gid, name):  # 设置群名
    HTTP("/set_group_name?group_id=%s&group_name=%s" % (gid, name))


def groupLeave(gid, type="false"):  # 退出群聊(type默认为false,如果登录号是群主, 则仅在此项为 true 时能够解散)
    HTTP("/set_group_leave?group_id=%s&is_dismiss=%s" % (gid, type))


def groupSetUserTitle(gid, uid, title):  # 设置群专属头衔
    HTTP("/set_group_special_title?group_id=%s&user_id=%s&special_title=%s" % (gid, uid, title))


def groupSign(gid):  # 群打卡
    HTTP("/send_group_sign?group_id=%s" % (gid))


def setFriendAdd(flag, approve="true"):  # 同意好友请求(approve是否同意,默认为true)(flag来自notice函数中的上报)
    HTTP("/set_friend_add_request?flag=%s&approve=%s" % (flag, approve))


def setGroupAdd(flag, type, approve="true",
                reason=""):  # 同意加群请求(approve是否同意,默认为true)(flag来自notice函数中的上报)(type内add 或 invite, 请求类型 需要和上报消息中的 sub_type 字段相符)(reason 拒绝理由 仅在拒绝时生效)
    HTTP("/set_group_add_request?flag=%s&type=%s&approve=%s&reason=%s" % (flag, type, approve, reason))


def getLoginInfo():  # 获取登录号信息
    return HTTP("/get_login_info")


def setLoginInfo(nickname, company, email, collage,
                 personal_note):  # 设置登录号信息(不懂看我https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%99%BB%E5%BD%95%E5%8F%B7%E8%B5%84%E6%96%99)
    HTTP("/set_qq_profile?nickname=%s&company=%s&email=%s&collage=%s&personal_note=%s" % (
    nickname, company, email, collage, personal_note))


def getStargerInfo(uid):  # 获取陌生人信息
    return HTTP("/get_stranger_info?user_id=%s" % (uid))


def getFriendList():  # 获取好友列表
    return HTTP("/get_friend_list")


def deleteFriend(uid):  # 删除好友
    HTTP("/delete_friend?user_id=%s" % (uid))


def getGroupInfo(gid):  # 获取群信息
    return HTTP("/get_group_info?group_id=%s" % (gid))


def getGroupList(gid):  # 获取群列表
    return HTTP("/get_group_list")


def getGroupUserInfo(gid, uid):  # 获取群成员信息
    return HTTP("/get_group_member_info?group_id=%s&user_id=%s" % (gid, uid))


def getGroupUserList(gid):  # 获取群成员列表
    return HTTP("/get_group_member_list?group_id=%s" % (gid))


def getGroupHonor(gid,
                  type="all"):  # 获取群荣誉信息(默认获取全部)(详细看https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E8%8D%A3%E8%AA%89%E4%BF%A1%E6%81%AF)
    return HTTP("/get_group_honor_info?group_id=%s&type=%s" % (gid, type))


def canSendImage():  # 检查是否可以发送图片
    return HTTP("/can_send_image")


def canSendRecord():  # 检查是否可以发送语音
    return HTTP("/can_send_record")


def getVersionInfo():  # 获取go-cqhttp版本信息
    return HTTP("/get_version_info")


def setGroupImage(gid,
                  file):  # 设置群头像(!!!注意!!! 目前这个API在登录一段时间后因cookie失效而失效, 请考虑后使用)(详细请看https://docs.go-cqhttp.org/api/#%E8%AE%BE%E7%BD%AE%E7%BE%A4%E5%A4%B4%E5%83%8F)
    return HTTP("/set_group_portrait?group_id=%s&file=%s" % (gid, file))


def ocrImage(imageid):  # 图片OCR(imageid为CQ码中的id)(详情请看https://docs.go-cqhttp.org/api/#%E5%9B%BE%E7%89%87-ocr)
    return HTTP("/ocr_image?image=%s" % (imageid))


def getGroupSysmsg():  # 获取群系统消息(返回规范https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E7%B3%BB%E7%BB%9F%E6%B6%88%E6%81%AF)
    return HTTP("/get_group_system_msg")


def uploadFile(file, name, uid=0, gid=0, folder=0):  # 上传群文件
    if uid and gid == 0 and folder == 0:  # 若uid不为0则上传私人文件
        return HTTP("/upload_private_file?user_id=%s&file=%s&name=%s" % (uid, file, name))
    elif gid and uid == 0 and folder:  # 若gid不为0则上传群文件
        return HTTP("/upload_group_file?group_id=%s&file=%s&name=%s&folder=%s" % (gid, file, name, folder))
    else:
        return "[Error][201]错误的传入"


# 群文件信息细节看我(!!!必看!!!)(https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%96%87%E4%BB%B6%E8%B5%84%E6%BA%90%E9%93%BE%E6%8E%A5)
def getGroupFileInfo(gid):  # 获取群文件系统信息
    return HTTP("/get_group_file_system_info?group_id=%s" % (gid))


def getGroupRootFile(gid):  # 获取群根目录文件列表
    return HTTP("/get_group_root_files?group_id=%s" % (gid))


def getGroupRootFolder(gid,
                       fid):  # 或群群根目录文件夹内列表(详情参考https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%A0%B9%E7%9B%AE%E5%BD%95%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8)
    return HTTP("/get_group_files_by_folder?group_id=%s&folder_id=%s" % (gid, fid))


def createGroupFolder(gid, name):  # 创建群根目录文件夹
    HTTP("/create_group_file_folder?group_id=%s&name=%s&parent_id=/" % (gid, name))


def destoryGroupFolder(gid, fid):  # 删除群根目录文件夹
    HTTP("/delete_group_folder?group_id=%s&folder_id=%s" % (gid, fid))


def destoryGroupFile(gid, fileid, bid):  # 删除群文件
    HTTP("/delete_group_file?group_id=%s&file_id=%s&busid=%s" % (gid, fileid, bid))


def getGroupFileUrl(gid, fileid, bid):  # 获取群文件链接
    return HTTP("/get_group_file_url?group_id=%s&file_id=%s&busid=%s" % (gid, fileid, bid))


def getStatus():  # 获取go-cqhttp状态信息(注意 所有统计信息都将在重启后重置)(详情https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%8A%B6%E6%80%81)
    return HTTP("/get_status")


def getAtAllTime(gid):  # 获取At全体成员的次数
    return HTTP("/get_group_at_all_remain?group_id=%s" % (gid))


def sendGroupNotice(gid, content, image=0):  # 发送群公告(image为可选)
    if image:
        HTTP("/_send_group_notice?group_id=%s&content=%s&image=%s" % (gid, content, image))
    else:
        HTTP("/_send_group_notice?group_id=%s&content=%s" % (gid, content))


def getGroupNotice(gid):  # 获取群公告
    return HTTP("/_get_group_notice?group_id=%s" % (gid))


def download(url, thread_count=8,
             header=""):  # go-cqhttp内置下载器(推荐使用默认参数)(详细请看https://docs.go-cqhttp.org/api/#%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6%E5%88%B0%E7%BC%93%E5%AD%98%E7%9B%AE%E5%BD%95)
    if header:
        return HTTP("/download_file?url=%s&thread_count=%s&header=%s" % (url, thread_count, header))
    else:
        header = "User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0[\r\n]Referer=" + url
        return HTTP("/download_file?url=%s&thread_count=%s&header=%s" % (url, thread_count, header))


def getOnlineClient(no_cache="true"):  # 获取当前在线客户端列表
    return HTTP("/get_online_clients?no_cache=%s" % (no_cache))


def getGroupMsgHistory(mid,
                       gid):  # 获取历史群消息(详情请看https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%B6%88%E6%81%AF%E5%8E%86%E5%8F%B2%E8%AE%B0%E5%BD%95)
    return HTTP("/get_group_msg_history?message_seq=%s&group_id=%s" % (mid, gid))


def setEssenceMsg(mid):  # 设置精华消息
    HTTP("/set_essence_msg?message_id=%s" % (mid))


def deleteEssenceMsg(mid):  # 移出精华消息
    HTTP("/delete_essence_msg?message_id=%s" % (mid))


def getEssenceMsgList(gid):  # 获取精华消息列表
    return HTTP("/get_essence_msg_list?group_id=%s" % (gid))


def checkUrlSafe(
        url):  # 检查链接安全性(详细请看https://docs.go-cqhttp.org/api/#%E6%A3%80%E6%9F%A5%E9%93%BE%E6%8E%A5%E5%AE%89%E5%85%A8%E6%80%A7)
    return HTTP("/check_url_safely?url=%s" % (url))


def sendPrivateForwordMsg(uid, msg):  # 发送合并转发自定义消息(好友)(上面跟群聊的详细教程一样)
    return HTTP("/send_private_forward_msg?user_id=%s&messages=%s" % (uid, msg))
