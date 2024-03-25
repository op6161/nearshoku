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
    def GOOGLE_API():
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
    if text is None:
        return None
    return text.replace('\u3000', ' ')


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


# ----- settings ----- #
# const class using set
CONST = _Const()
# model form using set
SHOP_INFO_MODEL_FORM = models.ShopInfoModel
USER_INFO_MODEL_FORM = models.UserInfoModel
SHOP_DETAIL_MODEL_FORM = models.ShopDetailModel
# shop_info_model_form = models.ShopInfoModel
# user_info_model_form = models.UserInfoModel
# shop_detail_model_form = models.ShopDetailModel
# ----- -------- ----- #


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
    selected_lat, selected_lng = 1, 1 #
    context = {
        'current_lat': current_lat, 'current_lng': current_lng,
        'selected_lat': selected_lat, 'selected_lng': selected_lng}
    return context

def hot_pepper_api(**kwargs):
    api_key = get_api(CONST.RECRUIT_API)
    API_HOST = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'Accept': '*/*'
    }
    kwargs['key'] = api_key

    query = '?'
    keys = kwargs.keys()
    vals = kwargs.values()

    for key, val in zip(keys, vals):
        query += f'{key}={val}&'

    url = API_HOST + query

    try:
        hot_pepper_response = requests.get(url, headers=headers)
    except Exception:
        # API Error
        raise Exception

    shop_info_json = parsing_xml_to_json(hot_pepper_response)
    try:
        shop_info_json = shop_info_json['results']['shop']  # ****
    except KeyError:
        # shop errpr
        # API의 한계로 일본 외의 나라에서는 사용할 수 없다
        # 일본 내에서도 주변에 등록된 식당이 없다면 사용할 수 없을 것 같다
        # >> keyError:'shop' 발생함
        # 검색 결과가 없습니다 출력하면 좋을 듯 하다
        raise 404
    except:
        # detail: API Server error
        raise 404

    return shop_info_json


def info_pack(info_json, model_form,model_hash=None):
    info_package = []
    if model_form == SHOP_DETAIL_MODEL_FORM:
        for shop in info_json:
            model_template = {
                # 필수요구
                'detail_shop_id': shop['id'],
                'detail_name': check_unicode(shop['name']),
                'detail_address': check_unicode(shop['address']),
                'detail_image': shop['photo']['pc']['l'],
                'detail_time': shop['open'],
                # + info
                'detail_kana': check_unicode(shop['name_kana']),
                'detail_access': check_unicode(shop['access']),
                'detail_shop_memo': check_unicode(shop['shop_detail_memo']),
                'detail_budget_memo': check_unicode(shop['budget_memo']),
                'detail_lat': shop['lat'],
                'detail_lng': shop['lng'],
                'detail_url': shop['urls']['pc'],
                'detail_card': shop['card'],
                'detail_genre': shop['genre']['name'],
                'detail_genre_catch': shop['genre']['catch'],
                'detail_price_average': shop['budget']['average'],
                'detail_station': shop['station_name'],
            }
            info_package.append(model_template)
    elif model_form == SHOP_INFO_MODEL_FORM:
        for shop in info_json:
            model_template = {
                'shop_id': shop['id'],
                'shop_name': check_unicode(shop['name']),
                'shop_kana': check_unicode(shop['name_kana']),
                'shop_access': check_unicode(shop['access']),
                'shop_thumbnail': shop['logo_image'],
                'shop_model_hash': model_hash
            }
            info_package.append(model_template)

    return info_package


# 두 함수는 return은 다르지만 args가 중복되니 기능을 합칠 수 잇어보인다
# API 호출을 분리시키면 될 듯 **kwargs로 하면 될거같은데
def load_user_info(range,order,model_hash,current_lat,
                   current_lng,selected_lat=None,selected_lng=None):
    '''

    '''
    user_info_json = [True] # default
    user_info = []
    for user in user_info_json: #template for modularize
        model_template = {
            'user_model_hash': model_hash,
            'current_lat': current_lat,
            'current_lng': current_lng,
            'selected_lat': selected_lat,
            'selected_lng': selected_lng,
            'range': range,
            'order': order,
        }
        user_info.append(model_template)
    return user_info


# views
# # # 페이징 구현 이후 views.result 합치기
def shop_show(request, model_hash, **kwargs):
    '''

    '''
    try:
        # load shop/user info from database by model_hash
        shop_list = SHOP_INFO_MODEL_FORM.objects.filter(shop_model_hash=model_hash)
        user_info = USER_INFO_MODEL_FORM.objects.get(user_model_hash=model_hash)
    except:
        # model_hash changed
        raise "Cache Lost Error"

    # paging =================================
    if kwargs.get('page'):
        # if got page number from request.GET['page']
        page = kwargs['page']
    else:
        # default page number
        page = 1

    PAGING_POST_NUMBER = 10  # page 마다 출력 상점 수
    paginator = Paginator(shop_list, PAGING_POST_NUMBER)
    try:
        page_object = paginator.page(page)
    except:
        # invalid page number
        # it has url print err
        page = paginator.num_pages
        page_object = paginator.page(page)
    # ========================================

    # *cont1: {user info}
    cont1 = user_info.__dict__
    # *cont2: {shop info, page info}
    cont2 = {
        'shop_list': shop_list,
        'page_object': page_object,
        'paginator': paginator,
        'len_page_objects': len(page_object)*page_object.number,
        'len_shop_list': len(shop_list),
    }

    # *contexts: {user info, shop info, page info}
    contexts = combine_dictionary(cont1, cont2)

    return render(request, 'result.html', contexts)


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

    if request.method == 'GET':
        # get GET method (move page)
        print('result() debug: GET method')
        page = request.GET.get('page')
        return shop_show(request, model_hash, page=page)
    elif request.method == 'POST':
        # get POST method (new search request)
        print('result() debug: POST method')
        model_hash = update_database(request)
        return shop_show(request, model_hash)

    print('*' * 10)
    print('*' * 10)
    print('active this code??')
    print('*' * 10)
    print('*' * 10)

    if model_hash is None:
        print('result() debug: model hash isNone')
        # 새로운 검색 요청을 받았을 때, 분기 수정 후 발생하지 않고 있음
        model_hash = update_database(request)
        return shop_show(request, model_hash)
    else:
        # 페이지 이동 시 작동할 것으로 추정
        print('result() debug: model_hash is True')
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
            raise 'Direction Error in update_database'

        user_info = load_user_info(range, order, model_hash, current_lat, current_lng, selected_lat, selected_lng)
        model_form_save(user_info, USER_INFO_MODEL_FORM)

        # save shop info to show
        shop_info_json = hot_pepper_api(lat=lat, lng=lng, range=range, count=100)#나중에추가order=order
        shop_info = info_pack(shop_info_json, SHOP_INFO_MODEL_FORM, model_hash)
        model_form_save(shop_info, SHOP_INFO_MODEL_FORM)
    return model_hash


def detail(request):
    if request.method == 'GET':
        shop_id = request.GET.get('shop_id')
        detail_info_json = hot_pepper_api(id=shop_id)
        detail_info = info_pack([detail_info_json], SHOP_DETAIL_MODEL_FORM)
        if not SHOP_DETAIL_MODEL_FORM.objects.filter(detail_shop_id=shop_id).exists():
            # 데이터 중복 저장 시 오류 발생으로
            # 이미 있는 데이터는 저장하지 않음
            model_form_save(detail_info, SHOP_DETAIL_MODEL_FORM) #데이터 중복 오류 발생

        detail_info = SHOP_DETAIL_MODEL_FORM.objects.get(detail_shop_id=shop_id)
        contexts = detail_info.__dict__
        return render(request,'result_detail.html',contexts)