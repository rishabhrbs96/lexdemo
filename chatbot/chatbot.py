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
pn = PubNub(pnconfig)

pn_chatroom_channel = os.environ.get('pubnub_chatroom_channel', None)
pn_chatbot_channel = os.environ.get('pubnub_chatbot_channel', None)
pn_robot_channel = os.environ.get('pubnub_robot_channel', None)
pn_smsrequest_channel = os.environ.get('pubnub_smsrequest_channel', None)
pn_smsresponse_channel = os.environ.get('pubnub_smsresponse_channel', None)

coolservices_url = 'https://lex.purplepromise.xyz'

chatbot_handle = ['@fred', '!', 'fred']


class ChatbotPNCallback(SubscribeCallback):

    # inherited from PubNub's SubscribeCallback
    def message(self, pubnub, message):
        try:

            # message notification from chatroom
            if message.channel == pn_chatroom_channel:
                message_start = message.message.split()[1]
                from_handle = message.message.split()[0]
                if message_start in chatbot_handle and from_handle not in chatbot_handle:
                    self.log_it(pubnub, "relevant chatbot located...")
                    user = from_handle[1:]
                    utterance = ' '.join(message.message.split()[2:])
                    response_text = self.ask_lex(pubnub, user, utterance)
                    pubnub.publish().channel(pn_chatroom_channel).message(
                        chatbot_handle[0] + ' ' + from_handle + ' ' + response_text).async(my_publish_callback)

            # message notification from smsconnector
            elif message.channel == pn_smsrequest_channel:
                self.log_it(pubnub, "relevant sms request located...")
                response = {
                    'ani': message.message['ani'],
                    'message': self.ask_lex(pubnub, message.message['ani'], message.message['message'])
                }
                pubnub.publish().channel(pn_smsresponse_channel).message(response).async(my_publish_callback)

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
            pubnub.publish().channel(pn_chatroom_channel).message("%s says welcome" %
                                                                  chatbot_handle[0]).async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass

    # our additional methods not in SubscribeCallback
    def ask_lex(self, pubnub,  user, utterance):
        self.log_it(pubnub, "asking lex for %s, '%s'" % (user, utterance))
        intent = lex.ask_lex(utterance, user).json()

        self.log_it(pubnub, "intent type: %s" % intent['dialogState'])
        self.log_it(pubnub, intent)

        # Determine intent type  1. ready  2. need slot data  3. what?
        if intent['dialogState'] == 'ReadyForFulfillment':

            # Call third party service that matches intent passing slot data
            self.log_it(pubnub, "intent name: %s" % intent['intentName'])
            if intent['intentName'] == 'AirlineStatus':
                self.log_it(pubnub, "Calling airline service...")
                response = requests.get(coolservices_url + '/airline/' + intent['slots']['airline'], timeout=10)
                result = response.json()
                self.log_it(pubnub, result)
                return result['message']

            elif intent['intentName'] == 'WeatherForecast':
                self.log_it(pubnub, "Calling weather service...")
                response = requests.get(coolservices_url + '/weather/' + intent['slots']['city'], timeout=10)
                result = response.json()
                self.log_it(pubnub, result)
                return result['message']

            elif intent['intentName'] == 'FedExRate':
                self.log_it(pubnub, "Calling FedEx rate service...")
                response = requests.get(
                    coolservices_url + '/fedexrate/' + intent['slots']['fromCity'] + '/' + intent['slots'][
                        'toCity'], timeout=10)
                result = response.json()
                self.log_it(pubnub, result)
                return result['message']

            # Use pubnub robot channel to talk to the robot
            elif intent['intentName'] == 'RobotIntent':
                self.log_it(pubnub, "Publish to robot service...")
                direction = intent['slots']['direction'].lower()
                pubnub.publish().channel(pn_robot_channel).message(direction).async(my_publish_callback)
                result = {'message': direction}
                self.log_it(pubnub, result)
                return result['message']

        # deal with conversation, lex maintains state based on user
        elif intent['dialogState'] in ('ElicitIntent', 'ElicitSlot'):
            return intent['message']

        # return help
        elif intent['dialogState'] in ['HelpIntent']:
            help_text = "welcome to lex. Chat with your neighbor. To ask Amazon Lex a question select one of " \
                        "the questions below. To respond to a question from lex prefix your response with '!'. "
            return help_text

    def log_it(self, pubnub, content):
        print(str(content))
        pubnub.publish().channel(pn_chatbot_channel).message(content).async(my_publish_callback)


# callback specified when publishing to channel
def my_publish_callback(envelope, status):
    if not status.is_error():
        print("message published successfully")
        pass  # Message successfully published to specified chatroomChannel.
    else:
        print("message published failure")
        pass  # Handle message publish error. Check 'category' property to find out possible issue

'''
    def message_save(self, pubnub, message):
        try:
            message_start = message.message.split()[1]
            from_handle = message.message.split()[0]
            if message_start in chatbot_handle and from_handle not in chatbot_handle:
                self.log_it("relevant message located...")

                # Pull user and utterance from pubnub message
                user = from_handle[1:]
                utterance = ' '.join(message.message.split()[2:])

                # Call Amazon Lex passing utterance and using user to track session
                self.log_it("asking lex for %s, '%s'" % (user, utterance))
                intent = lex.ask_lex(utterance, user).json()

                self.log_it("intent type: %s" % intent['dialogState'])
                self.log_it(intent)

                # Determine intent type  1. ready  2. need slot data  3. what?
                if intent['dialogState'] == 'ReadyForFulfillment':

                    # Call third party service that matches intent passing slot data
                    self.log_it("intent name: %s" % intent['intentName'])
                    if intent['intentName'] == 'AirlineStatus':
                        self.log_it("Calling airline service...")
                        response = requests.get(coolservices_url + '/airline/' + intent['slots']['airline'], timeout=10)
                        result = response.json()
                        pubnub.publish().channel(pn_chatroom_channel).message(
                            chatbot_handle[0] + ' ' + from_handle + ' ' + result['message']).async(my_publish_callback)
                        self.log_it(result)

                    elif intent['intentName'] == 'WeatherForecast':
                        self.log_it("Calling weather service...")
                        response = requests.get(coolservices_url + '/weather/' + intent['slots']['city'], timeout=10)
                        result = response.json()
                        pubnub.publish().channel(pn_chatroom_channel).message(
                            chatbot_handle[0] + ' ' + from_handle + ' ' + result['message']).async(my_publish_callback)
                        self.log_it(result)

                    elif intent['intentName'] == 'FedExRate':
                        self.log_it("Calling FedEx rate service...")
                        response = requests.get(
                            coolservices_url + '/fedexrate/' + intent['slots']['fromCity'] + '/' + intent['slots'][
                                'toCity'], timeout=10)
                        result = response.json()
                        pubnub.publish().channel(pn_chatroom_channel).message(
                            chatbot_handle[0] + ' ' + from_handle + ' ' + result['message']).async(my_publish_callback)
                        self.log_it(result)

                    # Use pubnub robot channel to talk to the robot
                    elif intent['intentName'] == 'RobotIntent':
                        self.log_it("Publish to robot service...")
                        direction = intent['slots']['direction'].lower()
                        pubnub.publish().channel(pn_robot_channel).message(direction).async(my_publish_callback)
                        # message_action = direction if direction in (
                        #     'rotate left', 'rotate right', 'stop') else 'go %s' % direction
                        message_action = direction
                        pubnub.publish().channel(pn_chatroom_channel).message(
                            '%s %s is asking robot to %s.' % (chatbot_handle[0], from_handle, message_action)).async(
                            my_publish_callback)
                        self.log_it("%s - %s" % (intent['intentName'], direction))

                elif intent['dialogState'] in ('ElicitIntent', 'ElicitSlot'):
                    pubnub.publish().channel(pn_chatroom_channel).message(
                        chatbot_handle[0] + ' ' + from_handle + ' ' + intent['message']).async(my_publish_callback)
                elif intent['dialogState'] in ['HelpIntent']:
                    help_text = "welcome to lex. Chat with your neighbor. To ask Amazon Lex a question select one of " \
                                "the questions below. To respond to a question from lex prefix your response with '!'. "
                    pubnub.publish().channel(pn_chatroom_channel).message(
                        chatbot_handle[0] + ' ' + from_handle + ' ' + help_text).async(my_publish_callback)

        except IndexError:
            pass  # do nothing
        except Exception as e:
            print("problem: %s" % str(e))
'''

print("starting chatbot...")
pn.add_listener(ChatbotPNCallback())
pn.subscribe().channels([pn_chatroom_channel, pn_smsrequest_channel]).execute()
