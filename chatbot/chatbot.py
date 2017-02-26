import os

import requests
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import lex

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)
pubnub = PubNub(pnconfig)

pn_chatroom_channel = os.environ.get('pubnub_chatroom_channel', None)
pn_chatbot_channel = os.environ.get('pubnub_chatbot_channel', None)

coolservices_url = 'https://fredsez.herokuapp.com'

chatbot_handle = '@fred'


class MySubscribeCallback(SubscribeCallback):

    def message(self, pubnub, message):
        try:
            message_start = message.message.split()[1]
            from_handle = message.message.split()[0]
            if message_start == chatbot_handle and from_handle != chatbot_handle:
                self.log_it("relevant message located...")

                user = from_handle[1:]
                utterance = ' '.join(message.message.split()[2:])

                self.log_it("asking lex...")
                intent = lex.ask_lex(utterance, user).json()

                self.log_it("intent type: %s"%intent['dialogState'])
                self.log_it(intent)
                if intent['dialogState'] == 'ReadyForFulfillment':

                    self.log_it("intent name: %s" % intent['intentName'])
                    if intent['intentName'] == 'AirlineStatus':
                        self.log_it("Calling airline service...")
                        response = requests.get(coolservices_url+'/airline/'+intent['slots']['airline'], timeout=10)
                        result = response.json()
                        pubnub.publish().channel(pn_chatroom_channel).message(chatbot_handle + ' ' + from_handle + ' ' + result['message']).async(my_publish_callback)
                        self.log_it(result)

                    elif intent['intentName'] == 'WeatherForecast':
                        self.log_it("Calling weather service...")
                        response = requests.get(coolservices_url+'/weather/'+intent['slots']['city'], timeout=10)
                        result = response.json()
                        pubnub.publish().channel(pn_chatroom_channel).message(chatbot_handle + ' ' + from_handle + ' ' + result['message']).async(my_publish_callback)
                        self.log_it(result)

                elif intent['dialogState'] in ('ElicitIntent', 'ElicitSlot'):
                    pubnub.publish().channel(pn_chatroom_channel).message(chatbot_handle + ' ' + from_handle + ' ' + intent['message']).async(my_publish_callback)

        except IndexError:
            pass # do nothing
        except Exception as e:
            print("problem: %s" % str(e))

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pubnub.publish().channel(pn_chatroom_channel).message("hello!!").async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass

    def log_it(self, content):
        print(str(content))
        pubnub.publish().channel(pn_chatbot_channel).message(content).async(my_publish_callback)

def my_publish_callback(envelope, status):
    if not status.is_error():
        pass  # Message successfully published to specified chatroomChannel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue

print("starting chatbot...")
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels([pn_chatroom_channel]).execute()