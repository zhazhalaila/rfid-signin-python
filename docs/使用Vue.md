Vue与后台API交互很简单

我们希望当用户点击查询按钮后，不跳转界面，直接在下方显示签到记录

首先，传值

```html
<div id="app-6">
  <input id="search" type="text" placeholder="输入格式->课程名称+日期" v-model="message"/>
```

```javascript
new Vue({
    el: '#app-6',
    data: {
        message: '',
        result: ''
    },

    methods : {
        open: function (data) {
            var message = this.message
```

利用收到的值来构造URL

```javascript
url = 'http://127.0.0.1:5000/api/class_history?name=' + encodeURIComponent(name)
  + '&time=' + encodeURIComponent(time)
```

获取数据

```javascript
this.$http.get(url, (data) => {
  this.result = data.history
})
```

查询激活按钮

```html
<button class="btn-search" type="button" v-on:click="open">
```

循环显示信息

```html
<div class="row" v-for="i in result">
  <div class="cell" data-title="姓名">
    {% raw %}{{ i.name }}{% endraw %}
  </div>
  <div class="cell" data-title="签到时间/课程提交签到表时间">
    {% raw %}{{ i.time }}{% endraw %}
  </div>
  <div class="cell" data-title="签到状态">
    <button type="button" class="btn btn-primary " v-if="i.active">已到</button>
    <button type="button" class="btn btn-danger" v-else>未到</button>
  </div>
</div>
```

参考链接：

[List Rendering](https://vuejs.org/v2/guide/list.html)

[Event Handling](https://vuejs.org/v2/guide/events.html)

[Display message depend on v-on:click in vue](https://stackoverflow.com/questions/52939968/display-message-depend-on-v-onclick-in-vue)
