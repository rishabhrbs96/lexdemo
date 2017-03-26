
var app = {
    'chatroom' : {},
    'chatbot' : {},
    'init': function(){
        this.chatroomChannel = PUBNUB_CHATROOM_CHANNEL;
        this.chatroom =  new PubNub({ publishKey : PUBNUB_PUBLISH_KEY, subscribeKey : PUBNUB_SUBSCRIBE_KEY});
        // this.chatroom =  new PubNub({ publishKey : 'demo', subscribeKey : 'demo'});
        this.chatroom.addListener({message:this.chatroomListener});
        this.chatroom.subscribe({channels:[this.chatroomChannel]});

        this.chatbotChannel = PUBNUB_CHATBOT_CHANNEL;
        this.chatbot =  new PubNub({ subscribeKey : PUBNUB_SUBSCRIBE_KEY});
        this.chatbot.addListener({message:this.chatbotListener});
        this.chatbot.subscribe({channels:[this.chatbotChannel]});

        // $('#message').keyup(this.checkForEnter);
        $('#send-button').click(this.publishMessage);
    },
    'chatroomListener': function(obj){
        $('#box').append(''+app.formatMessage((''+obj.message).replace( /[<>]/g, '' )));
        $('#box').scrollTop($('#box')[0].scrollHeight);
    },
    'chatbotListener': function(obj){
        if($('#monitor-slider').val()=='1'){
            $('#bot').append('<pre>'+JSON.stringify(obj.message, null, ' ')+'</pre>');
            $('#bot').scrollTop($('#bot')[0].scrollHeight);
        }
    },
    'checkForEnter' : function(e){
        e.preventDefault();
        if ((e.keyCode || e.charCode) === 13) {
            app.publishMessage(e);
        }
    },
    'publishMessage': function(e){
        e.preventDefault();
        var name = $('#name').val().replace(/[^A-Z|a-z]/g,'').toLowerCase().slice(0,10);
        name = (name=='')?'some-dude':name;
        var sez = $('#message').val();
        sez = (sez=='')?'sez nothing':sez;
        var message = '@'+name+' '+sez;
        app.chatroom.publish({channel: app.chatroomChannel, message: message,x : ($('#message').val(''))});
        return false;
    },
    'formatMessage': function(message){
        var tokens = message.split(' ');
        var handle = tokens[0];
        var myHandle = '@'+$('#name').val().replace(/[^A-Z|a-z]/g,'').toLowerCase().slice(0,10);
        var alignment = handle==myHandle? 'text-right' : 'text-left';
        var today  = new Date();
        var messageTime = today.getHours()%12+':'+("0"+today.getMinutes()).slice(-2)+':'+("0"+today.getSeconds()).slice(-2)+" "+(today.getHours()>11?"PM":"AM");
        if(handle==myHandle){
            var bubble = 'me-bubble';
            var bottom = 'me-bottom';
        } else if(handle=='@fred') {
            bubble = 'fred-bubble';
            bottom = 'fred-bottom';
        } else {
            bubble = 'other-bubble';
            bottom = 'other-bottom'
        }
        tokens.splice(0,1);
        var remaining = tokens.join(' ');
        return "<div class='"+bubble+"'>"+remaining+"</div><div class='"+bottom+" clearfix'><div class='pointy-thing-left'></div><div class='pointy-thing-right'></div></div><div class='"+alignment+"'><strong>"+handle+"</strong>  "+messageTime.toLocaleString()+"</div>";
    }
};
$(document).ready(app.init());


















