from dotenv import load_dotenv
import os
import json
import requests


def get_latlng(API_KEY):
    API_HOST = 'https://www.googleapis.com/geolocation/v1/'
    url = f'{API_HOST}geolocate?key={API_KEY}'

    response = json.loads(requests.post(url).text)

    lat = response['location']['lat']
    lng = response['location']['lng']

    return lat, lng


def get_location(lat, lng, API_KEY):
    API_HOST = 'https://maps.googleapis.com/maps/api/geocode/'
    url = f'{API_HOST}json?latlng={lat},{lng}&key={API_KEY}'
    response = json.loads(requests.post(url).text)
    print(response)
    location=1
    return location

load_dotenv()
google_maps_api = os.environ.get('GEOLOCATION_API_KEY')

lat, lng = get_latlng(google_maps_api)
print(lat,lng)
location = get_location(lat, lng, google_maps_api)