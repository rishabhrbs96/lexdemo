import os
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

aws_access_key = os.environ['aws_access_key']
aws_secret_access_key = os.environ['aws_secret_access_key']


def ask_lex(utterance, user):
    url = 'https://runtime.lex.us-east-1.amazonaws.com/bot/First/alias/firstone/user/'+user+'/text'
    auth = AWSRequestsAuth(aws_access_key=aws_access_key,
                           aws_secret_access_key=aws_secret_access_key,
                           aws_host='runtime.lex.us-east-1.amazonaws.com',
                           aws_region='us-east-1',
                           aws_service='lex')
    data = {
        "inputText": utterance,
        "sessionAttributes": {
            "string": "string"
        }
    }
    return requests.post(url=url, json=data, auth=auth)


if __name__ == '__main__':
    response = ask_lex('Gunter blieben glästen globen', 'some-dude')
    print(str(response.json()))
    response = ask_lex('how is goat', 'some-dude')
    print(str(response.json()))
    response = ask_lex('bob', 'some-dude')
    print(str(response.json()))
    response = ask_lex('what is the flight status for fedex', 'some-dude')
    print(str(response.json()))
