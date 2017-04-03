import os
from pprint import pprint

from bottle import get, post, request
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from twilio import twiml
from twilio.rest import TwilioRestClient

from smsconnector.smsconnector import my_publish_callback

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ.get('pubnub_publish_key', None)
pnconfig.subscribe_key = os.environ.get('pubnub_subscribe_key', None)

pn_smsrequest_channel = os.environ.get('pubnub_smsrequest_channel', None)
pn_smsresponse_channel = os.environ.get('pubnub_smsresponse_channel', None)

pn = PubNub(pnconfig)

twilio_on = True
twilio_account_sid = os.environ.get('twilio_account_sid', None)
twilio_auth_token = os.environ.get('twilio_auth_token', None)
twilio_ani = os.environ.get('twilio_ani', None)

client = TwilioRestClient(account=twilio_account_sid, token=twilio_auth_token)


@get('/sms')
def get_sms():
    return {'message': 'get smsconnector available'}


@post('/sms')
def post_sms():
    print("Processing sms request")
    print("Sending to channel: %s" % pn_smsrequest_channel)
    message = {
        'responseChannel': pn_smsresponse_channel,
        'user': request.forms.get('From'),
        'requestText': request.forms.get('Body'),
        'from': 'sms'
    }
    pprint(message)

    # publish to pubnub so the chatbot can handle it
    pn.publish().channel(pn_smsrequest_channel).message(message).async(my_publish_callback)

    # return an empty twiml response so as not to send message
    # we will handle this asynchronously using our pubnub listener below
    twiml_response = twiml.Response()
    return str(twiml_response)

