$(document).ready(function () {
  var pusher = new Pusher('b5b7012005f41774f901', {
      cluster: 'ap1',
      forceTLS: true
  });
  messageChannel = pusher.subscribe('message');
  // Listen to 'message sent' event
  messageChannel.bind('send', function(data) {
    var toAppend = document.createElement('div')
    toAppend.classList.add('lmedia', 'text-muted', 'pt-3')
    document.getElementById('message-box').appendChild(toAppend)
    toAppend.innerHTML ='<p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">'+
                    `<strong class="d-block text-gray-dark">${data}</strong>`+
                    '加入了课堂' + 
					'</p>' + 
				'</div>'
  });
});