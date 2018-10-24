var app = new Vue({
  el: '#app',
  data: {
    message: ''
  }
  ready: function() {

        // GET request
        this.$http.get('http://httpbin.org/ip', function (data, status, request) {

            // set data on vm
            this.$set('message', data)

        }).error(function (data, status, request) {
            // handle error
        })
      }
})
})
