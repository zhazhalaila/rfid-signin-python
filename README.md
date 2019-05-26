## Rfid-signin-python
RFID+Flask+Vue+Redis构造一个签到系统

项目已部署在Heroku上

[演示地址](https://flask-serialshow.herokuapp.com/index)

[演示视频](https://www.bilibili.com/video/av34612101)

测试账号名称: TEST 密码: password

项目功能 | 完成情况 | 满意度
------------ | ---------- | -----------
动态显示签到情况|     :smiley: | 80%
构造在线用户（课堂）池 | :smiley: | 95%
查询签到记录 | :smiley: | 70%
用户注册 | :smiley: | 80%
课堂绑定学生 | :smiley: | 80%
学生分群 | :smiley: | 90%
URL加密 | :smiley: | 90%
解除课堂与学生关系 | :worried: | 0%
异常处理 | :worried: | 0%
页面优化 | :worried: | 0%

部署的是国外的服务器因此日期显示为国外的日期

### Getting Started
在本地的部署
### 准备工作
1. [硬件准备](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E7%A1%AC%E4%BB%B6%E5%87%86%E5%A4%87.md)
1. [软件准备](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E8%BD%AF%E4%BB%B6%E5%87%86%E5%A4%87.md)

### 使用Docker

创建容器

```bash
git clone https://github.com/zhazhalaila/rfid-signin-python.git
cd rfid-signin-python
docker build -t serialshow:latest .
```

运行容器

```bash
docker run --name serialshow -d -p 8000:5000 --rm serialshow:latest
```

查看日志

```python
docker logs container
```

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
flask db upgrade
flask run
```
[数据库设计](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E6%95%B0%E6%8D%AE%E5%BA%93%E8%AE%BE%E8%AE%A1.md)

测试数据库是否正确
```
python tests.py
```

[几个大坑](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E6%B5%8B%E8%AF%95%E6%97%B6%E7%9A%84BUG.md)

### Built With
* [Redis](https://redis.io/) 主要用来构造在线用户（课堂）池
* [Flask](http://flask.pocoo.org/) Web框架
* [Vue](https://cn.vuejs.org/index.html) 动态查询

### API示例

查询学生签到情况，URL格式`http://127.0.0.1:5000/api/student_history?name=parameter`

返回数据格式
```
{"history":[{"active":true,"class_name":"RFID\u4f20\u611f\u5668","time":"2018-10-27 09:06:10"}]}
```

注意返回数据格式会出现`utf`编码的信息，我们可以不用管，JS会自动解析

查询当前签到情况，URL格式`http://127.0.0.1:5000/api/class_history?name=parameter&time=parameter`

返回数据格式
```
{"history":[{"active":true,"name":"\u6d4b\u8bd5\u8d26\u53f7","time":"2018-10-27 09:06:10"}]}
```

### Redis存储所有在线课堂
[原理](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E4%BD%BF%E7%94%A8Redis.md)

### Vue与API的交互

现在很流行前后端分离，后端提供API，前端只负责显示页面

[原理](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E4%BD%BF%E7%94%A8Vue.md)

### 与硬件交互

使用的COM3/4接口，Python已经有库可以帮我们完成读取USB接口的功能

启动`spider.py`，就可以看到结果了

[原理](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/%E7%AD%BE%E5%88%B0%E5%8E%9F%E7%90%86.md)

### URL加密

使用[Vigenère cipher算法加密](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)

[加密操作](https://github.com/zhazhalaila/rfid-signin-python/blob/master/docs/URL%E5%8A%A0%E5%AF%86.md)

### kmean算法

参考链接:
  
[集体智慧编程 第三章P42-P44](https://book.douban.com/subject/3288908/)

[K-Means Algorithm](https://www.coursera.org/lecture/machine-learning/k-means-algorithm-93VPG)

### 贡献代码
没有什么要求，只要能跑就行了，可以增加一些丰富的功能

### License
MIT
