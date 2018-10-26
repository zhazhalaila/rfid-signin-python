## Rfid-signin-python
RFID+Flask+Vue构造一个打卡系统

[项目演示地址](https://flask-serialshow.herokuapp.com/)部署在了Heroku上

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
Arduino开发板 + RFID-RC522传感器模组，
接线方式


Python 3.6.0

注册[Pusher](https://pusher.com/) 来完成动态显示签到情况功能

注册完成后会得到下面这样的连接脚本

```python
pusher_client = pusher.Pusher(
  app_id='621177',
  key='b5b7012005f41774f901',
  secret='b996e0df93996214b5ae',
  cluster='ap1',
  ssl=True
)
```
