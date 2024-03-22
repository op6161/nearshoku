from django.shortcuts import render, redirect
from . import models
import json
import requests
# settings
# form_current = models.BycurrentModel()
# form_selected = models.BySelectedModel()
# form_current_data = {'form_current':form_current}
# form_selected_data = {'form_selected':form_selected}
def constant(func):
    '''
        decorator constant for _Const Class
    '''
    def func_set(self, value):
        raise TypeError

    def func_get(self):
        return func()
    return property(func_get, func_set)

class _Const(object):
    '''
        A Class saving constants.
    '''
    @constant
    def GOOGLE_API():
        return 'GEOLOCATION_API_KEY'

    @constant
    def RECRUIT_API():
        return 'HOTPEPPER_API_KEY'


CONST = _Const()

# use API
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

def get_current_latlng():
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    context = {'current_lat': current_lat, 'current_lng': current_lng}
    return context

def get_selected_latlng():
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    selected_lat, selected_lng = 1,1
    context = {
        'current_lat': current_lat, 'current_lng': current_lng,
        'selected_lat': selected_lat, 'selected_lng': selected_lng}
    return context


# views
def index(request):
    current_latlng = get_current_latlng()
    return render(request, 'result_index.html', current_latlng)

def result(request):
    if request.method == 'POST':
        print('감지는 됩니까?')
        try :
            if request.POST['selectCurrentLocationRange']:
                current_latlng = get_current_latlng()
                current_lat = current_latlng['current_lat']
                current_lng = current_latlng['current_lng']
                range = request.POST['selectCurrentLocationRange']
                contexts = {'current_lat':current_lat,
                            'current_lng':current_lng,
                            'current_range':range}
                return render(request, 'result.html', contexts)
        except:
            pass
        try:
            if request.POST['selectSelectedLocationRange']:
                print('이곳에 들어오고 있나요?')
                current_latlng = get_current_latlng()
                current_lat = current_latlng['current_lat']
                current_lng = current_latlng['current_lng']
                range = request.POST['selectSelectedLocationRange']
                selected_lat = 1
                selected_lng = 1
                contexts = {'current_lat': current_lat,
                            'current_lng': current_lng,
                            'current_range': range,
                            'selected_lat':selected_lat,
                            'selected_lng': selected_lng,}
                return render(request, 'result.html', contexts)
        except:
            pass