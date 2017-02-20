
var app = {
    'init': function(){
        this.channel = PUBNUB_CHANNEL;
        this.pubnub =  new PubNub({ publishKey : PUBNUB_PUBLISH_KEY, subscribeKey : PUBNUB_SUBSCRIBE_KEY});
        this.pubnub.addListener({message:this.channelListener});
        this.pubnub.subscribe({channels:[this.channel]});
        $('#message').keyup(this.publishMessage);
    },
    'channelListener': function(obj){
        $('#box').append('<br>'+(''+obj.message).replace( /[<>]/g, '' ));
        $('#box').scrollTop($('#box')[0].scrollHeight);
    },
    'publishMessage': function(e){
        if ((e.keyCode || e.charCode) === 13) {
            var name = $('#name').val();
            name = (name=='')?'some-dude':name;
            var sez = $('#message').val();
            sez = (sez=='')?'sez nothing':sez;
            var message = '@'+name+' - '+sez;
            app.pubnub.publish({channel: app.channel, message: message,x : ($('#message').val(''))});
        }
    }
};
$(document).ready(app.init());
