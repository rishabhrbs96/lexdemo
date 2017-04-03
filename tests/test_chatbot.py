import os
from pprint import pprint

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)

pn_chatbot_channel = 'CHATBOT'
pn_chatbot_test_channel = 'CHATBOT_TEST'

pn = PubNub(pnconfig)


class TestChatbotSubscription(SubscribeCallback):
    def message(self, pubnub, message):
        try:
            pprint(vars(message))
        except Exception as e:
            print("Exception %s test chatbot" % str(e))

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

print("Test Chatbot Start")
pn.add_listener(TestChatbotSubscription())
pn.subscribe().channels([pn_chatbot_test_channel]).execute()

message = {
    'responseChannel': 'CHATBOT_TEST',
    'user': 'scott',
    'requestText': 'what is the forecast for memphis',
    'from': 'TEST_CHATBOT'
}
pprint(message)
pn.publish().channel(pn_chatbot_channel).message(message).async(my_publish_callback)