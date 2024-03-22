from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
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
        a Class saving constants.
    '''
    @constant
    def GOOGLE_API():
        return 'GEOLOCATION_API_KEY'

    @constant
    def RECRUIT_API():
        return 'HOTPEPPER_API_KEY'


def check_unicode(text):
  return text.replace('\u3000',' ')


def make_hash():
    import time
    key = time.time_ns()
    return hash(key)

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
    vals = param.values()

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
    return response

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


def load_shop_info(lat,lng,range,model_hash):
    '''

    '''
    shop_info = get_shop_info(lat,lng,range)
    shop_info = parsing_xml_to_json(shop_info)
    # print(shop_info)
    shop_info = shop_info['results']['shop'] #****
    # API의 한계로 일본 외의 나라에서는 사용할 수 없습니다
    # 일본 내에서도 주변에 등록된 식당이 없다면 사용할 수 없을 것 같습니다
    # >> keyError:'shop' 발생
    shop_list = []

    for shop in shop_info:
        temp = {
            'shop_id': shop['id'],
            'shop_name': check_unicode(shop['name']),
            'shop_kana': check_unicode(shop['name_kana']),
            'shop_access': check_unicode(shop['access']),
            'shop_thumbnail': shop['logo_image'],
            'shop_model_hash':model_hash
        }
        shop_list.append(temp)
    return shop_list

def shop_form_save(shop_list):
    object_bulk = [models.ShopInfoModel(**item) for item in shop_list]
    models.ShopInfoModel.objects.bulk_create(object_bulk)


def shop_show(request, cont1, model_hash):
    PAGING_POST_NUMBER = 4
    shop_list = models.ShopInfoModel.objects.filter(shop_model_hash=model_hash)
    # print(shop_list)
    # page = request.GET.get('page')
    # paginator = Paginator(shop_list, PAGING_POST_NUMBER)
    # try:
    #     page_object = paginator.page(page)
    # except:
    #     page=1
    #     page_object = paginator.page(page)
    # cont2 = {'shop_list': shop_list,
    #      'page_object': page_object,
    #      'paginator': paginator}
    cont2 = {'shop_list':shop_list}#paging test
    contexts = combine_dictionary(cont1,cont2)

    return render(request, 'result.html', contexts )

def combine_dictionary(dict1, dict2):
    '''
        combine two dictionaries but, *they should have different keys*
    '''
    dict1.update(dict2)
    return dict1

# views
def direction_error(request):
    return HttpResponse('direction error')

def index(request):
    current_latlng = get_current_latlng()
    return render(request, 'result_index.html', current_latlng)

def result(request):
    if request.method not in ['POST','GET']:
        return direction_error(request)

    current_latlng = get_current_latlng()
    current_lat = current_latlng['current_lat']
    current_lng = current_latlng['current_lng']
    #### test code ####
    current_lat = 34.67  # test value
    current_lng = 135.52  # test value
    range = 1  # test valeu
    contexts = {'current_lat': current_lat,
                'current_lng': current_lng,
                'range': range}

    if request.method == ['GET']:
        shop_show(request, contexts)
    ####################
    try :
        if request.POST['selectCurrentLocationRange']:
            range = request.POST['selectCurrentLocationRange']
            #### test code ####
            current_lat = 34.67 #test value
            current_lng = 135.52 #test value
            range = 1 # test valeu
            contexts = {'current_lat':current_lat,
                        'current_lng':current_lng,
                        'range':range}
            model_hash = make_hash()
            shop_list = load_shop_info(current_lat,current_lng,range,model_hash)
            shop_form_save(shop_list)
            shop_show(request, contexts, model_hash)

            #### test code ####
            # contexts = {'current_lat':current_lat,
            #             'current_lng':current_lng,
            #             'range':range}
            return render(request, 'result.html', contexts)
    except:
         pass

    try:
        if request.POST['selectSelectedLocationRange']:
            range = request.POST['selectSelectedLocationRange']
            selected_lat = 34.67 #temp value
            selected_lng = 135.52 #temlp value
            contexts = {'current_lat': current_lat,
                        'current_lng': current_lng,
                        'range': range,
                        'selected_lat':selected_lat,
                        'selected_lng': selected_lng,}
            #### test code ####




            #### test code ####
            return render(request, 'result.html', contexts)

    except:
        return direction_error(request)