### 关于Redis

Redis在此项目中的功能类似于普通的数据库，主要就是用来存储在线课堂，以及对在线课堂的更新和删除，但是这样会有一个问题

假设我们第一次测试时，注册了三个账号并登录，那么Hash table中会存

ID | TOKEN
------------ | -------------
1 | RFID
2 | DATABASE

如果误删了migtations文件夹和app.db，那么数据库会重置，但是Redis不会！

第二次测试，注册一个账号，但是Hash table仍没有变，此时只有一个账号，获取在线课堂时会出错，因此最好在数据库初始化之前，清除Hash Table

[清除办法](https://stackoverflow.com/questions/16561379/remove-complete-hashset-at-once-in-redis)

### 关于CORS

在使用vue访问API来构建动态页面时，会遇到CORS错误

[什么是CORS](https://zh.wikipedia.org/zh-cn/%E8%B7%A8%E4%BE%86%E6%BA%90%E8%B3%87%E6%BA%90%E5%85%B1%E4%BA%AB)

[使用Flask-cors解决](https://flask-cors.readthedocs.io/en/latest/)

### 编码问题
使用Redis获取值，我们会得到二进制编码的字符，这样是不行的要把它转换成Python中的字符默认编码`utf-8`

### JSON格式构造问题
在构造JSON格式的字符时，不能直接返回对象，要使用字典来构造，示例代码

```python
for i in range(0, len(history)):
	dict_format = {}
	dict_format['class_name'] = history[i].time_class_name
	dict_format['time'] = history[i].time_time.strftime('%Y-%m-%d %H:%M:%S')
	dict_format['active'] = history[i].active
	json_list.append(dict_format)
return jsonify({'history': json_list})
```
