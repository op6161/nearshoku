from django.shortcuts import render, redirect
from django.http import HttpResponse
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
    '''
        a function for get protected key with python-dotenv

        Args:
            api_type(str): a .env key for using API
        Raises:
            -
        Returns:
            api_key(str)
    '''
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_key = os.environ.get(api_type)
    return api_key


def get_latlng(api_key):
    '''
        get user's current lat/lng from google-geolocation

        Args:
            api_key(str): googlemaps API key
        Raises:
            -
        Returns:
            lat, lng(float)
    '''
    API_HOST = 'https://www.googleapis.com/geolocation/v1/'
    url = f'{API_HOST}geolocate?key={api_key}'

    response = json.loads(requests.post(url).text)

    lat = response['location']['lat']
    lng = response['location']['lng']

    return lat, lng


def get_location(lat, lng, api_key):
    '''
        get user's location for lat/lng from google-geocode API

        Args:
            api_key(str): googlemaps API key
        Raises:
            -
        Returns:
            -
    '''
    API_HOST = 'https://maps.googleapis.com/maps/api/geocode/'
    url = f'{API_HOST}json?latlng={lat},{lng}&key={api_key}'
    response = json.loads(requests.post(url).text)
    return response


def get_current_latlng():
    '''

    '''
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    context = {'current_lat': current_lat, 'current_lng': current_lng}
    return context


def get_selected_latlng():
    '''

    '''
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    selected_lat, selected_lng = 1,1
    context = {
        'current_lat': current_lat, 'current_lng': current_lng,
        'selected_lat': selected_lat, 'selected_lng': selected_lng}
    return context


def get_shop_info(lat,lng,range):
    '''

    '''
    api_key = get_api(CONST.RECRUIT_API)
    API_HOST = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'Accept': '*/*'
    }
    param = {
        'key':f'{api_key}',
        'lat':lat,
        'lng':lng,
        'range':range,
    }

    query = '?'
    keys = param.keys()
    vals = params.values()

    for key,val in zip(keys,vals):
        if val:
            query += f'{key}={val}&'
        else:
            query += f'{key}&'
    url = API_HOST+query

    try:
        response = requests.get(url, headers=headers)
    except Exception:
        print(Exception)
    return shop_info

def parsing_xml_to_json(xml_data):
    '''
        Parse the xml data into json format

        Args:
             xml_data(requests.get():xml format)
        Raises:
            -
        Returns:
            json_data(requests.get().txt:json format)
    '''
    import xmltodict
    xml_pars = xmltodict.parse(xml_data.text)
    json_dump = json.dumps(xml_pars)
    json_data = json.loads(json_dump)
    return json_data


def load_shop_list(lat,lng,range):
    '''

    '''
    shop_info = get_shop_info(lat,lng,range)
    shop_info = parsing_xml_to_json(shop_info)
    shop_info = shop_info['result']['shop']
    shop_list = []
    for shop in shop_info:
        temp = {
            'shop_id': shop['id'],
            'shop_name': check_unicode(shop['name']),
            'shop_kana': check_unicode(shop['name_kana']),
            'shop_access': check_unicode(shop['access']),
            'shop_thumbnail': shop['logo_image'],
        }
        shop_list.append(temp)
    return shop_list

def shop_form_save(shop_list):
    form = models.ShopInfoModel()
    for idx, shop in enumerate(shop_list):
        form.shop_list_number = idx
        form.shop_id = shop['shop_id']
        form.shop_name = shop['shop_name']
        form.shop_kana = shop['shop_kana']
        form.shop_access = shop['shop_access']
        form.shop_thumbnail = shop['shop_thumbnail']
        form.save(commit=False) # save to memory

# views
def direction_error(request):
    return HttpResponse('direction error')

def index(request):
    current_latlng = get_current_latlng()
    return render(request, 'result_index.html', current_latlng)

def result(request):
    if request.method != 'POST':
        return direction_error

    current_latlng = get_current_latlng()
    current_lat = current_latlng['current_lat']
    current_lng = current_latlng['current_lng']

    try :
        if request.POST['selectCurrentLocationRange']:
            range = request.POST['selectCurrentLocationRange']
            contexts = {'current_lat':current_lat,
                        'current_lng':current_lng,
                        'current_range':range}



            return render(request, 'result.html', contexts)
    except:
        pass

    try:
        if request.POST['selectSelectedLocationRange']:
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
        return direction_error