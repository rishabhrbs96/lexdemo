import os

from bottle import get, post, request
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)
pn = PubNub(pnconfig)

pn_smsrequest_channel = os.environ.get('pubnub_smsrequest_channel', None)
pn_smsresponse_channel = os.environ.get('pubnub_smsresponse_channel', None)

twilio_account_sid = os.environ.get('twilio_account_sid', None)
twilio_auth_token = os.environ.get('twilio_auth_token', None)
twilio_ani = os.environ.get('twilio_ani', None)


@get('/sms')
def get_sms():
    return {'message': 'get smsconnector available'}


@post('/sms')
def post_sms():
    # receive sms
    twilio_request = request.json()

    # post to pubnub so the chatbot can handle it
    pn.publish().channel(pn_smsrequest_channel).message({'ani': '', 'message': ''}).async(my_publish_callback)

    # return an empty twiml response so as not to send message
    # we will handle this asynchronously using our pubnub listener below
    twiml_response = None #twiml.Response()
    return twiml_response


class SMSResponsePNCallback(SubscribeCallback):
    def message(self, pubnub, message):
        ani = message.message.ani
        text_to_send = message.message.message
        # call sms send

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass


# callback specified when publishing to channel
def my_publish_callback(envelope, status):
    if not status.is_error():
        print("message published successfully")
        pass  # Message successfully published to specified chatroomChannel.
    else:
        print("message published failure")
        pass  # Handle message publish error. Check 'category' property to find out possible issue


print("starting sms pn listener...")
pn.add_listener(SMSResponsePNCallback())
pn.subscribe().channels([pn_smsresponse_channel]).execute()
