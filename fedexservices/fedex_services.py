import os
import requests

rate_url = 'https://purplepromise.xyz/rate/%s/%s'


def get_rate_details(from_city, to_city):
    try:
        response = requests.get(rate_url % (from_city, to_city))
        rate = response.json()
        message = rate['message']
        return {'message': message}
    except:
        return {'message': 'There was a problem retrieving the shipping rate.'}


if __name__ == '__main__':
    rate= get_rate('New York City', 'Phoenix')
    print(str(rate))