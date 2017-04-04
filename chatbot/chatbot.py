import os
from pprint import pprint

import requests
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import lex

import re

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)
pn = PubNub(pnconfig)

pn_chatbot_channel = os.environ.get('pubnub_chatbot_channel', None)
pn_chatbotlog_channel = os.environ.get('pubnub_chatbotlog_channel', None)
pn_robot_channel = os.environ.get('pubnub_robot_channel', None)

coolservices_url = 'https://lex.purplepromise.xyz'

chatbot_handle = ['fred']


class ChatbotPNCallback(SubscribeCallback):
    # inherited from PubNub's SubscribeCallback
    def message(self, pubnub, message):
        try:
            pprint(vars(message))

            chatbot_request = message.message
            if chatbot_request['from'] not in chatbot_handle:
                log_it('Processing chatbot request')
                chatbot_request['from'] = chatbot_handle[0]
                user = re.sub(r'\W+', '', chatbot_request['user'])
                chatbot_request['responseText'] = ask_lex(user, chatbot_request['requestText'])
                pubnub.publish().channel(chatbot_request['responseChannel']).message(chatbot_request).async(
                    chatbot_publish_callback)

            else:
                log_it("Message ignored")
        except IndexError as e:
            print("IndexError: %s" % str(e))
        except Exception as e:
            print("problem: %s" % str(e))

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
            log_it("chatbot online")
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass


# callback specified when publishing to channel
def chatbot_publish_callback(envelope, status):
    if not status.is_error():
        print("message published successfully")
        pass  # Message successfully published to specified chatroomChannel.
    else:
        print("message published failure")
        pass  # Handle message publish error. Check 'category' property to find out possible issue


def log_it(content):
    print(str(content))
    pn.publish().channel(pn_chatbotlog_channel).message(content).async(my_publish_callback)


def ask_lex(user, utterance):
    try:
        log_it("asking lex for %s, '%s'" % (user, utterance))
        intent = lex.ask_lex(utterance, user).json()

        log_it("intent type: %s" % intent['dialogState'])
        log_it(intent)

        # Determine intent type  1. ready  2. need slot data  3. what?
        if intent['dialogState'] == 'ReadyForFulfillment':

            # Call third party service that matches intent passing slot data
            log_it("intent name: %s" % intent['intentName'])
            if intent['intentName'] == 'AirlineStatus':
                log_it("Calling airline service...")
                response = requests.get(coolservices_url + '/airline/' + intent['slots']['airline'], timeout=10)
                result = response.json()
                log_it(result)
                return result['message']

            elif intent['intentName'] == 'WeatherForecast':
                log_it("Calling weather service...")
                response = requests.get(coolservices_url + '/weather/' + intent['slots']['city'], timeout=10)
                result = response.json()
                log_it(result)
                return result['message']

            elif intent['intentName'] == 'FedExRate':
                log_it("Calling FedEx rate service...")
                response = requests.get(
                    coolservices_url + '/fedexrate/' + intent['slots']['fromCity'] + '/' + intent['slots'][
                        'toCity'], timeout=10)
                result = response.json()
                log_it(result)
                return result['message']

            # Use pubnub robot channel to talk to the robot
            elif intent['intentName'] == 'RobotIntent':
                log_it("Publish to robot service...")
                direction = intent['slots']['direction'].lower()
                pn.publish().channel(pn_robot_channel).message(direction).async(my_publish_callback)
                result = {'message': direction}
                log_it(result)
                return result['message']

        # deal with conversation, lex maintains state based on user
        elif intent['dialogState'] in ('ElicitIntent', 'ElicitSlot'):
            return intent['message']

        # return help
        elif intent['dialogState'] in ['HelpIntent']:
            help_text = "Welcome to lex. Chat with your neighbor. To ask Amazon Lex a question select one of " \
                        "the questions below. To respond to a question from lex prefix your response with '!'. "
            return help_text

    except Exception as e:
        print("Exception: %s" % str(e))
        return "Sorry, I didn't understand your question."


print("starting chatbot...")
pn.add_listener(ChatbotPNCallback())
pn.subscribe().channels([pn_chatbot_channel]).execute()
