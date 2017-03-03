from bottle import get

from fedexservices.fedex_services import get_rate_details
from flightservices.flight_services import get_airline_details
from weatherservices.weather_services import get_forecast


@get('/chatbot')
def get_bot():
    return {'message': 'All your chatbots are belong to us!'}


@get('/airline/<airline>')
def get_airline(airline):
    return get_airline_details(airline)


@get('/weather/<city_name>')
def get_weather(city_name):
    return get_forecast(city_name)

@get('/fedexrate/<from_city>/<to_city>')
def get_rate(from_city, to_city):
    return get_rate_details(from_city, to_city)