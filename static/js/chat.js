
var chatarea = document.getElementById('chat_textarea');

var doc_url = document.URL;


function addFriend(friend_id){
    $.ajax({
    type: 'POST',
    url: '/chat/addFriend/' + friend_id,
    success: function(response){

        }
    }
    )
    }

function setScroll(){
    var $textarea = $('#chat_textarea');
    $textarea.scrollTop($textarea[0].scrollHeight);
}

function getMessages(){
    var doc_url = document.URL;
    if (doc_url.includes('chat/room')){
        var room_id = doc_url[doc_url.length-1];
        var url = '/api/room_messages/' + room_id;
    } else if (doc_url.includes('chat/chat')){
        var recipient_id = doc_url[doc_url.length-1];
        var url = '/api/messages/friend_id=' + recipient_id;
    } else {
        return;
    }
    $.ajax({
        type: 'GET',
        //  url: '/chat/getMessages/' + recipient_id,
          url: url,
        success: function(response){
            chatarea.value = '';
            for (let key in response){
                 let msg = '\n' + response[key].timestamp.replace('T', ' ').slice(0, 16) + '  ' + response[key].sender_id + ':   ' + response[key].content;
                if (response[key].destruct_timer != 0){
                    msg += '      ' + response[key].destruct_timer.toString() + ' s';
                }

                chatarea.value += msg;
                setScroll();
            }}
        ,
        error: function(response){
        //    alert('Error');
        }
    });
}



$(document).on('submit', '#msg_form', function(e){
    var doc_url = document.URL;
    var target_id = doc_url[doc_url.length-1]
    if (doc_url.contains('chat/chat')){
        var url = '/chat/send/friend_id=' + target_id;
    } else if (doc_url.contains('chat/room')){
        var url = '/chat/send/room_id=' + target_id;
    } else {
        return;
    };
    e.preventDefault();
    $.ajax({
    type: 'POST',
    url: url,
    data: {
        friend_id: target_id,
        msg_text: $('#msg_text').val(),
        destr_timer: $('#destruct_select').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(data){
        getMessages();
    }
    });
    document.getElementById('msg_text').value = ''
});


$(document).ready(function(){
console.log(recipient_id);
    if (recipient_id){
            getMessages();
    }
    setInterval(getMessages, 10000);
    }
);



