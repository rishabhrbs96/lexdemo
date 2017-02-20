import requests
import time
from requests.structures import CaseInsensitiveDict

FLIGHT_URL = "https://data-live.flightradar24.com/zones/fcgi/feed.js?airline=!%s&_=%d"
AIRPORT_URL = "http://services.faa.gov/airport/status/%s?format=application/json"

AIRLINE_CODE = CaseInsensitiveDict()
AIRLINE_CODE['American'] = 'AAL'
AIRLINE_CODE['FedEx'] = 'FDX'
AIRLINE_CODE['United'] = 'UAL'
AIRLINE_CODE['Alaska'] = 'ASA'
AIRLINE_CODE['Allegiant'] = 'AAY'
AIRLINE_CODE['Delta'] = 'DAL'
AIRLINE_CODE['Frontier'] = 'FFT'
AIRLINE_CODE['Hawaiian'] = 'HAL'
AIRLINE_CODE['JetBlue'] = 'JBU'
AIRLINE_CODE['Southwest'] = 'SWA'


def get_airline_details(airline):
    try:
        flights = get_active_flights(AIRLINE_CODE[airline])
        fastest = get_fastest_flight(flights)
        highest = get_highest_flight(flights)
        origination = get_most_originations(flights)
        destination = get_most_destinations(flights)

        data = {
            'airline': airline.capitalize(),
            'num_flights': len(flights),
            'fastest_flight': fastest['flight_number'],
            'fastest_speed': fastest['speed'],
            'highest_flight': highest['flight_number'],
            'highest_altitude': highest['altitude'],
            'origination_airport': get_airport(origination['airport']),
            'origination_count': origination['count'],
            'destination_airport': get_airport(destination['airport']),
            'destination_count': destination['count']
        }

        message = "%(airline)s has %(num_flights)d flights in the air. Flight %(fastest_flight)s is the fastest, travelling at %(fastest_speed)d knots. Flight %(highest_flight)s is the highest, travelling at %(highest_altitude)d feet. %(destination_airport)s has the most inbound flights for %(airline)s at %(destination_count)d. %(origination_airport)s has the most outbound flights for %(airline)s at %(origination_count)d."

        return {'message': message % data}
    except:
        return {'message': 'There was a problem retrieving the airline detail.'}



def get_active_flights(airline_code):
    url = FLIGHT_URL % (airline_code, int(time.time()))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }
    response = requests.get(url, headers=headers)
    response_obj = response.json()
    flights = [v for k, v in response_obj.items() if isinstance(v, list)]
    flights = [clean_flight_data(x) for x in flights]
    return flights


def get_fastest_flight(flights):
    fast_speed = 0
    fast_flight = {}
    for flight in flights:
        if flight['speed'] > fast_speed:
            fast_speed = flight['speed']
            fast_flight = flight
    return fast_flight


def get_highest_flight(flights):
    fast_speed = 0
    high_flight = {}
    for flight in flights:
        if flight['altitude'] > fast_speed:
            fast_speed = flight['altitude']
            high_flight = flight
    return high_flight


def get_most_destinations(flights):
    destinations = {}
    for flight in flights:
        try:
            destinations[flight['destination']] += 1
        except KeyError as e:
            destinations[flight['destination']] = 1
    key = max(destinations, key=destinations.get)
    return {'airport': key, 'count': destinations[key]}


def get_most_originations(flights):
    originations = {}
    for flight in flights:
        try:
            originations[flight['origination']] += 1
        except KeyError as e:
            originations[flight['origination']] = 1
    key = max(originations, key=originations.get)
    return {'airport': key, 'count': originations[key]}


def clean_flight_data(flight):
    result = {}
    try:
        result = {
            'flight_number': flight[16],
            'speed': flight[5],
            'altitude': flight[4],
            'origination': flight[11],
            'destination': flight[12],
            'type': flight[8],
            'registration': flight[9]
        }
    except:
        pass
    return result


def get_flight_count_to(airport_code, flights):
    count = len([x for x in flights if x['destination'] == airport_code])
    return count


def get_flight_count_from(airport_code, flights):
    count = len([x for x in flights if x['origination'] == airport_code])
    return count


def get_flight_detail(call_sign, flights):
    flights = [x for x in flights if x['flight_number'] == call_sign]
    return flights


def get_airport(airport_code):
    result = airport_code
    try:
        url = AIRPORT_URL % airport_code
        response = requests.get(url, timeout=0.5)
        if response.status_code in [200]:
            airport = response.json()
            result = airport['name']
    except Exception as e:
        pass
    return result


if __name__ == '__main__':

    al = 'fedex'#'AAL'#'FDX'
    result = get_airline_details(al)
    print(str(result))
    # f = get_active_flights(al)
    # o = get_flight_count_from(ap, f)
    # i = get_flight_count_to(ap, f)
    # print('Airline: %s, Airport: %s, Total: %d, In: %d, Out: %d' % (al, ap, len(f), i, o))
    # # print(str(get_flight_detail(cs, f)))
    # ff = get_fastest_flight(f)
    # print(str(ff))
    # hf = get_highest_flight(f)
    # print(str(hf))
    # print('airport %s, %s' % (ap, str(get_airport(ap))))
    # pass
