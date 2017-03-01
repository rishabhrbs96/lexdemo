import os
from bottle import run, template, static_file, route, get, TEMPLATE_PATH

import coolwebservices


TEMPLATE_PATH.insert(0, os.environ.get('template_path','./views'))

HOST = '0.0.0.0'
PORT = port=int(os.environ.get("PORT", 5000))

pubnub = {
    'pubnub_publish_key': os.environ.get('pubnub_publish_key', None),
    'pubnub_subscribe_key': os.environ.get('pubnub_subscribe_key', None),
    'pubnub_chatroom_channel': os.environ.get('pubnub_chatroom_channel', None),
    'pubnub_chatbot_channel': os.environ.get('pubnub_chatbot_channel', None)
}


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.environ.get("static_path", "./static"))


@get('/')
def get_fredsez():
    return template('fredsez', **pubnub)


if __name__=='__main__':
    run(host=HOST, port=PORT)
