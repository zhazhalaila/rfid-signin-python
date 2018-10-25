new Vue({
    el: '#app-6',
    data: {
        message: '',
        result: ''
    },

    methods : {
        open: function (data) {
            var message = this.message
            var name = message.split(':')[0]
            var time = message.split(':')[1]
			url = 'http://127.0.0.1:5000/api/class_history?name=' + encodeURIComponent(name)
                + '&time=' + encodeURIComponent(time)
            this.$http.get(url, (data) => {
                this.result = data.history
            }).error(function (data, status, request) {
                //handler error
            })
        }
    }
})