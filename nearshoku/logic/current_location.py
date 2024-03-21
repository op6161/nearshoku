from dotenv import load_dotenv
import os
import json
import requests


def get_location(url):
    r = requests.post(url)
    print (r)
    response = json.loads(requests.post(url).text)
    lat = round(response['location']['lat'], 2)
    lng = round(response['location']['lng'], 2)
    return lat, lng

load_dotenv()
geolocation_api = os.environ.get('GEOLOCATION_API_KEY')

API_KEY = geolocation_api
API_HOST = 'https://www.googleapis.com/geolocation/v1/'
url = f'{API_HOST}geolocate?key={API_KEY}'

lat, lng = get_location(url)