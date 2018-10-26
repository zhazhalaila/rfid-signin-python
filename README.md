## Rfid-signin-python
RFID+Flask+Vue构造一个打卡系统

[项目演示地址](https://flask-serialshow.herokuapp.com/)部署在了Heroku上

[演示视频](https://www.bilibili.com/video/av34612101)

项目功能 | 完成情况 | 满意度
------------ | ---------- | -----------
动态显示签到情况|     :smiley: | 80%
构造在线用户（课堂）池 | :smiley: | 95%
查询签到记录 | :smiley: | 70%
用户注册 | :smiley: | 80%
课堂绑定学生 | :smiley: | 80%
URL加密 | :worried: | 0%
解除课堂与学生关系 | :worried: | 0%
页面优化 | :worried: | 0%

### Getting Started
在本地的部署
### 准备工作
1. [硬件准备](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E7%A1%AC%E4%BB%B6%E5%87%86%E5%A4%87.md)
1. [软件准备](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E8%BD%AF%E4%BB%B6%E5%87%86%E5%A4%87.md)

### 安装
```
git clone https://github.com/zhazhalaila/rfid-signin-python.git
cd rfid-signin-python
pip install -r requirements.txt
```

### 运行与测试
运行
```
set FLASK_APP=serialshow.py
flask db init
flask db migrate -m "first"
flask db upgrade
flask run
```
测试数据库是否正确
```
python tests.py
```

### Built With
* [Redis](https://redis.io/) 主要用来构造在线用户（课堂）池
* [Flask](http://flask.pocoo.org/) Web框架
* [Vue](https://cn.vuejs.org/index.html) 动态查询
