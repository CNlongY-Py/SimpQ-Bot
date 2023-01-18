# SimpQ #
==================
## 安装操作使用指南 ##
SimpQ使用Python编写且基于[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)的QQBot框架
遵循GPL 3.0开源协议
**建议Python版本3.10.9**

---


SimpQ基础的文件目录
-----------------
- go-cqhttp
- logs
- plugins
- pluglibs
- bot.py
- libs.py
- main.py
- start.py

go-cqhttp 文件夹用来放置go-cqhttp的发行版
logs 用来存放Bot的日志文件
plugins 用来存放插件文件
pluglibs 用来存放插件的前置库
bot.py Bot的插件载入系统
libs.py go-cqhttp的API(截至目前已全部兼容可用API)
main.py Bot的监听器
start.py 启动Bot框架

### 懒人化安装请看下方SimpQ Toolkit ###
***
SimpQ版本
--------------
SimpQ及其小工具通常分为3个版本
a(alpha),b(beta),c(classic),RC(Release Candidate)
- a  为项目初期的工程版本,处于想法实现的过程,一般不会出现在Releases里
- b  为项目的测试版本,较为稳定
- c  为项目的正式版本,为b版本稳定运行一段时间后转为稳定版本
- RC 为项目正式版本的附加版本(类似于DLC?),会修复c版本的一些bug和增加一些新的特性
***
## 安装使用SimpQ ##
安装go-cqhttp
--------------
点击** [go-cqhttp版本列表](https://github.com/Mrs4s/go-cqhttp/releases) **来选择适合你系统的版本
放到go-cqhttp后启动会生成配置文件
请选择HTTP通信
配置文件生成后完成后打开config.yml
修改你的账号密码
```
account: # 账号相关
  uin: 1919810 # QQ账号
  password: '114514' # 密码为空时使用扫码登录
```
将servers:修改为以下内容
```
# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器

  - http: # HTTP 通信设置
      address: 0.0.0.0:5700 # HTTP监听地址
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling: # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post: # 反向HTTP POST地址列表
        #- url: ''                # 地址
        #  secret: ''             # 密钥
        #  max-retries: 3         # 最大重试，0 时禁用
        #  retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
        - url: http://127.0.0.1:5701/ # 地址
          secret: ''                  # 密钥
          max-retries: 10             # 最大重试，0 时禁用
          retries-interval: 1000      # 重试时间，单位毫秒，0 时立即

```
启动SimpQ和go-cqhttp
-------------------
**go-cqhttp和SimpQ必须同时运行,缺一不可!!!**
SimpQ点击start.py启动(推荐使用命令行python -m start.py启动)
go-cqhttp点击go-cqhttp.bat启动
***
## 插件的开发 ##
请阅读doc文件夹内**插件开发指南.md**

***
## SimpQ Toolkit 
*本工具箱为新手打造,不推荐老手使用*
>仍在开发,预计将于SimpQ b0.2发布时推出
- [ ] go-cqhttp一键安装并配置 
- [ ] 运行库一键部署(包含插件)
- [ ] 插件本体\前置 社区
- [ ] 下载SimpQ更新
- [ ] 小工具更新\下载
- [ ] 生成启动脚本
## 开发小工具 ##
- CNetSDK.py 需要搭配插件connectSDK.py一并使用 远程连接到机器人终端并输出日志信息打印到控制台
- SimpDebug.py 伪go-cqhttp,可以自定义命令,用来给插件Debug(目前仅有alpha版本)
- 加速开发中...
