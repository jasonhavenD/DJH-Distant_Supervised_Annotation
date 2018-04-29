# DJH-OpenRE
---
[CN-DBpedia](http://kw.fudan.edu.cn/cndbpedia/intro/)
---
[mongodb官网下载](https://www.mongodb.com/download-center?jmp=nav#community)
[mongodb3.4.1下载](http://oaq0p7t2g.bkt.clouddn.com/mongodb-win32-x86_64-2008plus-ssl-3.4.1-signed.msi?attname=)
windows mongodb 配置：
1.创建目录如下格式：
- bin
- data
- conf
	- mongodb.config
- logs
	- mongodb.log

2.环境变量：
将bin目录加入到path

3.启动 cmd
- 1.普通启动 ：mongod --config mongodb.config路径

- 2系统服务
	- 2.1 mongod --config mongodb.config路径 --install (管理者权限)
	- 2.2 net start mongodb
	- 2.3 net stop mongodb
