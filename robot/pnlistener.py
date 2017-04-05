import os
import time

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

import gopigo_client

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)
pubnub = PubNub(pnconfig)

pn_chatbotlog_channel = os.environ.get('pubnub_chatbotlog_channel', None)
pn_robot_channel = os.environ.get('pubnub_robot_channel', None)


class MySubscribeCallback(SubscribeCallback):
    CRAB_DURATION = 3
    TURN_DURATION = 1
    BLINK_DURATION = .25
    FAST_SPEED = 200
    SLOW_SPEED = 150

    def message(self, pubnub, message):
        try:
            action = message.message.lower()
            if 'forward' in action:
                gopigo_client.fwd()
                time.sleep(self.CRAB_DURATION)
                gopigo_client.stop()
            elif 'backward' in action:
                gopigo_client.bwd()
                time.sleep(self.CRAB_DURATION)
                gopigo_client.stop()
            elif 'rotate' in action:
                if 'left' in action:
                    gopigo_client.left_rot()
                    time.sleep(self.TURN_DURATION)
                    gopigo_client.stop()
                elif 'right in action':
                    gopigo_client.right_rot()
                    time.sleep(self.TURN_DURATION)
                    gopigo_client.stop()
            elif 'left' in action:
                gopigo_client.left()
                time.sleep(self.TURN_DURATION)
                gopigo_client.stop()
            elif 'right' in action:
                gopigo_client.right()
                time.sleep(self.TURN_DURATION)
                gopigo_client.stop()
            elif 'dance' in action:
                gopigo_client.right()
                time.sleep(self.TURN_DURATION)
                gopigo_client.left_rot()
                time.sleep(self.TURN_DURATION)
                gopigo_client.right_rot()
                time.sleep(self.TURN_DURATION)
                gopigo_client.fwd()
                time.sleep(self.TURN_DURATION)
                gopigo_client.right()
                time.sleep(self.TURN_DURATION)
                gopigo_client.bwd()
                time.sleep(self.TURN_DURATION)
                gopigo_client.stop()
            elif 'stop' in action:
                gopigo_client.stop()
            elif 'blink' in action:
                for i in range(5):
                    gopigo_client.led_on(0)
                    gopigo_client.led_off(1)
                    time.sleep(self.BLINK_DURATION)
                    gopigo_client.led_off(0)
                    gopigo_client.led_on(1)
                    time.sleep(self.BLINK_DURATION)
                gopigo_client.led_off(0)
                gopigo_client.led_off(1)
            elif 'faster' in action:
                gopigo_client.set_speed(self.FAST_SPEED)
            elif 'slower' in action:
                gopigo_client.set_speed(self.SLOW_SPEED)
            else:
                pass
            self.log_it(self.get_status(action))
        except IndexError:
            pass  # do nothing
        except Exception as e:
            print("problem: %s" % str(e))

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print("Connectivity lost...")
            pass  # This event happens when radio / connectivity is lost
            pubnub.reconnect()
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            print("PN Timeout...")
            pass
            pubnub.reconnect()
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
        else:
            print("some other status: %d" % status)  # some other status


    @staticmethod
    def get_status(action):
        result = {}
        result['voltage'] = gopigo_client.volt()
        result['distance'] = gopigo_client.us_dist(0)
        result['action'] = action
        return result


def my_publish_callback(envelope, status):
    if not status.is_error():
        pass  # Message successfully published to specified chatroomChannel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue

def log_it(content):
    print(str(content))
    # todo get stats - ultrasonic, voltage, last direction, image
    pubnub.publish().channel(pn_chatbotlog_channel).message(content).async(my_publish_callback)

if __name__ == '__main__':
    print("waiting 30 seconds for network connectivity...")
    time.sleep(30)
    print("initialize robot...")
    gopigo_client.servo(90)
    gopigo_client.set_speed(MySubscribeCallback.SLOW_SPEED)
    print("starting pnlistener...")
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels([pn_robot_channel]).execute()
    print('end')