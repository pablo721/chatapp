
var chatarea = document.getElementById('chat_textarea');




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
    $.ajax({
        type: 'GET',
        //  url: '/chat/getMessages/' + recipient_id,
          url: '/api/messages?friend_id=' + recipient_id,
        success: function(response){
            chatarea.value = '';
            console.log('api_js_yo');
            console.log(response);
            console.log(response.length);
            console.log(typeof(response));

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
    e.preventDefault();
    $.ajax({
    type: 'POST',
    url: '/chat/send?' + recipient_id,
    data: {
        recipient_id: recipient_id,
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
    setInterval(getMessages, 2500);
    }
);



