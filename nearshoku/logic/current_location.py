import json
import requests

def get_api(api_type):
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_key = os.environ.get(api_type)
    return api_key


def get_latlng(api_key):
    api_host = 'https://www.googleapis.com/geolocation/v1/'
    url = f'{api_host}geolocate?key={api_key}'

    response = json.loads(requests.post(url).text)

    lat = response['location']['lat']
    lng = response['location']['lng']

    return lat, lng


def get_location(lat, lng, api_key):
    api_host = 'https://maps.googleapis.com/maps/api/geocode/'
    url = f'{api_host}json?latlng={lat},{lng}&key={api_key}'
    response = json.loads(requests.post(url).text)
    return response


google_maps_api = get_api('GEOLOCATION_API_KEY')
lat, lng = get_latlng(google_maps_api)
print(lat,lng)
location = get_location(lat, lng, google_maps_api)