import os

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from twilio.rest import TwilioRestClient

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)

pn_smsresponse_channel = os.environ.get('pubnub_smsresponse_channel', None)

pn = PubNub(pnconfig)

twilio_on = True
twilio_account_sid = os.environ.get('twilio_account_sid', None)
twilio_auth_token = os.environ.get('twilio_auth_token', None)
twilio_ani = os.environ.get('twilio_ani', None)

client = TwilioRestClient(account=twilio_account_sid, token=twilio_auth_token)


class SMSResponsePNCallback(SubscribeCallback):
    def message(self, pubnub, message):
        try:
            # pull ani and message from pubnub payload
            ani = message.message['user']
            text_to_send = message.message['responseText']

            # send sms response using twilio
            if twilio_on:
                message = client.messages.create(body=text_to_send, to=ani, from_=twilio_ani)
            print("Sent SMS to ani: %s, body: %s, sid: %s" % (
                ani, text_to_send, str(message.sid)
            ))
        except Exception as e:
            print("Exception %s sending SMS" % str(e))

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
