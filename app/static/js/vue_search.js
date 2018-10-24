new Vue({
    el: '#app-6',
    data: {
        name: '',
        result: ''
    },

    methods : {
        open: function (data) {
            var name = this.name
			url = 'http://127.0.0.1:5000/api/student_history?name=' + encodeURIComponent(name)
            this.$http.get(url, (data) => {
                this.result = data.history
            }).error(function (data, status, request) {
                //handler error
            })
        }
    }
})