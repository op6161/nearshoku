from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.cache import cache
from . import models
import json
import requests


# settings, tools
def constant(func):
    """
    A decorator function for _Const Class
    """
    def func_set(self, value):
        """
        you can't edit constant
        """
        raise TypeError

    def func_get(self):
        """
        you can use constant
        """
        return func()
    return property(func_get, func_set)

class _Const(object):
    """
    This Class is saving constants
    """
    @constant
    def GOOGLE_API(): # is not err
        return 'GEOLOCATION_API_KEY'

    @constant
    def RECRUIT_API():
        return 'HOTPEPPER_API_KEY'

def check_unicode(text):
    """
    Replace the str has unicode u3000 -> ' ' (space)

    Args:
        text(str): the string that has unicode u3000
    Returns:
        text(str): the string that changed from u3000 to space
    """
    return text.replace('\u3000',' ')

def make_hash():
    """
    Make hash key from current time

    Returns: hash key (int)
    """
    import time
    key = time.time_ns()
    return hash(key)

def parsing_xml_to_json(xml_data):
    """
    Parse the xml data into json format

    Args:
         xml_data(requests.get():xml format)
    Returns:
        json_data(requests.get().txt:json format)
    """
    import xmltodict
    xml_pars = xmltodict.parse(xml_data.text)
    json_dump = json.dumps(xml_pars)
    json_data = json.loads(json_dump)
    return json_data

def model_form_save(item_list, form_model):
    """
    Save the items into the modelform(db)

    Args:
        item_list(list): list of dict items
        form_model(models.Model): model form in models.py
    """
    object_bulk = [form_model(**item) for item in item_list]
    form_model.objects.bulk_create(object_bulk)

def combine_dictionary(dict1, dict2):
    """
    Combine two dictionaries. but they should have different keys
    * if dicts have same keys, it can update dict1's value without combining

    Args:
        dict1(dict)
        dict2(dict)
    Returns dictionary: dict1 + dict2
    """
    dict1.update(dict2)
    return dict1

CONST = _Const() # const class using set

# use API function
def get_api(api_type):
    """
    Get protected key with python-dotenv
    Args:
        api_type(str): a .env key for using API
    Returns:
        api_key(str)
    """
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_key = os.environ.get(api_type)
    return api_key


def get_latlng(api_key):
    """
    Get user's current lat/lng from google-geolocation
    Args:
        api_key(str): googlemaps API key
    Returns:
        lat(float): user's current Latitude
        lng(float): user's current Longitude
    """
    API_HOST = 'https://www.googleapis.com/geolocation/v1/'
    url = f'{API_HOST}geolocate?key={api_key}'

    response_geolocate = json.loads(requests.post(url).text)

    lat = response_geolocate['location']['lat']
    lng = response_geolocate['location']['lng']

    return lat, lng

# # # 구글맵과 연동 필요함
def get_location(lat, lng, api_key):
    '''
        Get user's location for lat/lng from google-geocode API

        Args:
            api_key(str): googlemaps API key
        Raises:
            -
        Returns:
            -
    '''
    API_HOST = 'https://maps.googleapis.com/maps/api/geocode/'
    url = f'{API_HOST}json?latlng={lat},{lng}&key={api_key}'
    response_geocode = json.loads(requests.post(url).text)
    return response_geocode


def get_current_latlng():
    '''

    '''
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    context = {'current_lat': current_lat, 'current_lng': current_lng}
    return context
# # 이 두 함수는 조건부로 합치면 좋을 것 같다 get latlng까지, view.result 같이 수정 필요함 주의
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


def load_shop_info(lat,lng,range,model_hash):
    '''
        Load shop info from hotpepper API

        Args:
            lat(float): latitude
            lng(float): longitude
            range(int): range option
            model_hash(int): a hash key made by make_hash()
        Raises:
            KeyError: There is no search result
        Returns:
            shop_info(list): list of dicts shop information
    '''
    api_key = get_api(CONST.RECRUIT_API)
    API_HOST = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'Accept': '*/*'
    }
    param = {
        """
        API parameters
        
        Params :
            key : api_key
            lat : latitude
            lng : longitude
            range : 1~5 : Search range from location(lat,lng)
            order : 4 or other : Search base from recommendation/range
                in this project, POST 'order' in True, False
                so it must be translate True: 4 False: 0
            count : 1~100 : result shop count (default 10)
            format : 'json','xml' : data format (default xml)
                in this project, parse xml to json has already been developed
                so I use 'xml' format. But it is no better than using json format 
        """
        'key': f'{api_key}',
        'lat': lat,
        'lng': lng,
        'range': range,
        #'order':order,
        'count':100,
        'format':'xml',
    }

    query = '?'
    keys = param.keys()
    vals = param.values()

    for key, val in zip(keys, vals):
        query += f'{key}={val}&'

    url = API_HOST + query

    try:
        hot_pepper_response = requests.get(url, headers=headers)
    except Exception:
        raise Exception

    shop_info_json = parsing_xml_to_json(hot_pepper_response)
    try:
        shop_info_json = shop_info_json['results']['shop'] #****
    except KeyError:
        # API의 한계로 일본 외의 나라에서는 사용할 수 없다
        # 일본 내에서도 주변에 등록된 식당이 없다면 사용할 수 없을 것 같다
        # >> keyError:'shop' 발생함
        # 검색 결과가 없습니다 출력하면 좋을 듯 하다
        raise 404

    shop_info = []

    for shop in shop_info_json:
        temp = {
            'shop_id': shop['id'],
            'shop_name': check_unicode(shop['name']),
            'shop_kana': check_unicode(shop['name_kana']),
            'shop_access': check_unicode(shop['access']),
            'shop_thumbnail': shop['logo_image'],
            'shop_model_hash':model_hash
        }
        shop_info.append(temp)
    return shop_info
# 두 함수는 return은 다르지만 args가 중복되니 기능을 합칠 수 잇어보인다
# API 호출을 분리시키면 될 듯
def load_user_info(range,order,model_hash,current_lat,
                   current_lng,selected_lat=None,selected_lng=None):
    '''

    '''
    user_info_json = [True] # default
    user_info = []
    for user in user_info_json: #template for modularize
        temp = {
            'user_model_hash':model_hash,
            'current_lat':current_lat,
            'current_lng':current_lng,
            'selected_lat':selected_lat,
            'selected_lng':selected_lng,
            'range':range,
            'order':order,
        }
        user_info.append(temp)
    return user_info

# # # using
# if selected_lat:
#     load_user_info(range,order,model_hash,current_lat,current_lng,selected_lat,selected_lng)
# else:
#     load_user_info(range, order, model_hash, current_lat, current_lng)

# views
# # # 페이징 구현 이후 views.result 합치기
def shop_show(request, model_hash):
    '''

    '''
    try:
        shop_list = models.ShopInfoModel.objects.filter(shop_model_hash=model_hash)
        user_info = models.UserInfoModel.objects.get(user_model_hash=model_hash) # add code test num a1a1
    except:
        raise "Cache Lost Error"

    # # # # paging code
    # PAGING_POST_NUMBER = 4
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
    cont1 = user_info.__dict__ # add code test num a1a1
    cont2 = {'shop_list':shop_list} # temp value for no paging
    contexts = combine_dictionary(cont1,cont2)
    return render(request, 'result.html', contexts )

def direction_error(request):
    '''

    '''
    return HttpResponse('direction error')

def index(request):
    '''

    '''
    current_latlng = get_current_latlng()
    return render(request, 'result_index.html', current_latlng)


def result(request): # for test code # add code test num a1a1
    model_hash = cache.get('model_hash')

    if request.POST.get('selectCurrentLocationRange') \
    or request.POST.get('selectSelectedLocationRange'):
        # 새로운 검색 요청을 받았을 때
        print('result() debug: get POST')
        model_hash = update_database(request)
        return shop_show(request, model_hash)

    if model_hash is None:
        print('result() debug: is model hash none')
        # 새로운 검색 요청을 받았을 때, 분기 수정 후 발생하지 않고 있음
        model_hash = update_database(request)
        return shop_show(request, model_hash)
    else:
        # 페이지 이동 시 작동할 것으로 추정
        print('result() debug: is model hash')
        return shop_show(request, model_hash)


def update_database(request):
    '''
    A function that save models by POST vals
    '''
    model_hash = make_hash()
    cache.set('model_hash', model_hash)
    selected_lat = None
    selected_lng = None

    order = 1  # temp value

    if request.method == 'POST':
        # save user info
        current_latlng = get_current_latlng()
        current_lat = current_latlng['current_lat']
        current_lng = current_latlng['current_lng']

        if request.POST.get('selectCurrentLocationRange'):
            range = request.POST['selectCurrentLocationRange']
            # order = request.POST['selectCurrentLocationOrder']
            lat = current_lat
            lng = current_lng
        elif request.POST.get('selectSelectedLocationRange'):
            range = request.POST['selectSelectedLocationRange']
            # order = request.POST['selectSelectedLocationOrder']
            selected_lat = 34.67 # temp value
            selected_lng = 135.52 # temp value
            lat = selected_lat
            lng = selected_lng
        else:
            raise 'Direction Error'

        user_info = load_user_info(range, order, model_hash, current_lat, current_lng, selected_lat, selected_lng)
        model_form_save(user_info,models.UserInfoModel)

        # save shop info to show
        shop_info = load_shop_info(lat,lng,range,model_hash)
        model_form_save(shop_info, models.ShopInfoModel)
    return model_hash
        # context를 어떻게 집어넣어야 show가 가능하지? 해결
        # def result에서는 이제 정보 보내주기만 하면 될 듯 하다

