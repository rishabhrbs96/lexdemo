import os
from time import sleep

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

import gopigo_client

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)
pubnub = PubNub(pnconfig)

pn_chatbot_channel = os.environ.get('pubnub_chatbot_channel', None)
pn_robot_channel = os.environ.get('pubnub_robot_channel', None)


class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        try:
            action = message.message.lower()
            if 'forward' in action:
                gopigo_client.fwd()
                sleep(2)
                gopigo_client.stop()
            elif 'backward' in action:
                gopigo_client.bwd()
                sleep(2)
                gopigo_client.stop()
            elif 'left' in action:
                gopigo_client.left()
                sleep(2)
                gopigo_client.stop()
            elif 'right' in action:
                gopigo_client.right()
                sleep(2)
                gopigo_client.stop()
            elif 'rotate left' in action:
                gopigo_client.left_rot()
                sleep(2)
                gopigo_client.stop()
            elif 'rotate right' in action:
                gopigo_client.right_rot()
                sleep(2)
                gopigo_client.stop()
            elif 'stop' in action:
                gopigo_client.stop()
            elif 'blink' in action:
                pass
            else:
                pass
            self.log_it({'action': action})
        except IndexError:
            pass  # do nothing
        except Exception as e:
            print("problem: %s" % str(e))

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

    def log_it(self, content):
        print(str(content))
        # todo get stats - ultrasonic, voltage, last direction, image
        pubnub.publish().channel(pn_chatbot_channel).message(content).async(my_publish_callback)


def my_publish_callback(envelope, status):
    if not status.is_error():
        pass  # Message successfully published to specified chatroomChannel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue


print("starting gopi listenr...")
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels([pn_robot_channel]).execute()