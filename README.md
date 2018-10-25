# rfid-signin-python
RFID+Flask构造一个打卡系统

redis存储在线课堂已完成

10.22日

构造一个在线课堂首页

查询资料， 看vue怎么与后端进行交互

10.24日 已完成vue与后端交互并且创建了查询界面

已知BUG：

查询到的永远是True

解决办法：

每一天都创建一个数据表初始化值为False， 检测到RFID信息设置值为False.
