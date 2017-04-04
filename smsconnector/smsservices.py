import os
from pprint import pprint

from bottle import get, post, request
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from twilio import twiml


pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)
pn = PubNub(pnconfig)

pn_chatbot_channel = os.environ.get('pubnub_chatbot_channel', None)
pn_smsresponse_channel = os.environ.get('pubnub_smsresponse_channel', None)


@get('/')
def get_index():
    return 'smsservices'


@get('/sms')
def get_sms():
    return {'message': 'get smsconnector available'}


@post('/sms')
def post_sms():
    print("Processing sms request")
    print("Sending to channel: %s" % pn_chatbot_channel)
    message = {
        'responseChannel': pn_smsresponse_channel,
        'user': request.forms.get('From'),
        'requestText': request.forms.get('Body'),
        'from': 'sms'
    }
    pprint(message)

    # publish to pubnub so the chatbot can handle it
    pn.publish().channel(pn_chatbot_channel).message(message).sync()

    # return an empty twiml response so as not to send message
    # we will handle this asynchronously using our pubnub listener below
    twiml_response = twiml.Response()
    return str(twiml_response)
