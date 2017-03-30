import os
import requests

ll_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s'
weather_url = 'https://api.darksky.net/forecast/%s/%f,%f'
darksky_key = os.environ.get('darksky_key', None)

def get_forecast(city_name):
    try:
        ll = get_lat_lon(city_name)
        response = requests.get(weather_url % ((darksky_key,)+ll), timeout=10)
        weather = response.json()
        current = "Currently in %s it is %d degrees and %s." % (city_name, int(weather['currently']['temperature']),
                                                               weather['currently']['summary'].lower())
        hourly = "The forecast for %s is %s with a high of %d and a low of %d." % (city_name, weather['daily']['data'][0]['summary'].split()[0].lower() + ' ' +
                                                ' '.join(weather['daily']['data'][0]['summary'].split()[1:])[:-1],
                                                int(weather['daily']['data'][0]['temperatureMax']),
                                                int(weather['daily']['data'][0]['temperatureMin'])
                                                )
        return {'message': "%s %s" % (current, hourly)}
    except Exception as e:
        return {'message': 'There was a problem retrieving the forecast.'}


def get_lat_lon(city_name):
    response = requests.get(ll_url%city_name, timeout=5)
    ll = response.json()
    return ll['results'][0]['geometry']['location']['lat'], ll['results'][0]['geometry']['location']['lng']

if __name__ == '__main__':
    forecast = get_forecast('New York City')
    print(str(forecast))
    forecast = get_forecast('Memphis, TN')
    print(str(forecast))
    forecast = get_forecast('France')
    print(str(forecast))