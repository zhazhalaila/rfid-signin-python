new Vue({
    el: '#app-6',
    data: {
        name: '',
        result: ''
    },

    methods : {
        open: function (data) {
            var name = this.name
			url = 'https://flask-serialshow.herokuapp.com/api/student_history?name=' + encodeURIComponent(name)
            this.$http.get(url, (data) => {
                this.result = data.history
            }).error(function (data, status, request) {
                //handler error
            })
        }
    }
})