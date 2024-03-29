from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.cache import cache
from . import models
from .views_module import model_form_save, combine_dictionary, check_unicode
from .views_module import constant, parsing_xml_to_json


# settings, tools
class _Const(object):
    """
    save constants
    """
    @constant
    def GOOGLE_API():
        return 'GEOLOCATION_API_KEY'

    @constant
    def RECRUIT_API():
        return 'HOTPEPPER_API_KEY'

    @constant
    def BAD_REQUEST():
        return 'Bad Request'

    @constant
    def NOT_FOUND():
        return 'Not Found'

    @constant
    def INTERNAL_SERVER_ERROR():
        return 'Internal Server Error'

    @constant
    def BAD_GATEWAY():
        return 'Bad Gateway'


CONST = _Const()
SHOP_INFO_MODEL_FORM = models.ShopInfoModel
USER_INFO_MODEL_FORM = models.UserInfoModel
SHOP_DETAIL_MODEL_FORM = models.ShopDetailModel


# use API function
def get_key(api_type):
    """
    Get protected key with from .env file use python-dotenv
    Args:
        api_type: str: a dotenv(.env) key
    Returns:
        key: str: a dotenv(.env) value
    """
    from dotenv import load_dotenv
    import os
    load_dotenv()
    key = os.environ.get(api_type)
    return key


def hot_pepper_api(**kwargs):
    '''
    Get shops data from using recruit-hot-pepper API
    Args:
        :**kwargs:hot-pepper api params key=value
    Returns:
        shop_data:list[dicts{}],dict{}: hot pepper api response parsed to json format
        error_state: int: 200, 404, 500, 502
    '''
    import requests
    api_key = get_key(CONST.RECRUIT_API)
    API_HOST = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'Accept': '*/*'}
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
        return {}, 502

    data_json = parsing_xml_to_json(hot_pepper_response)
    try:
        shop_data = data_json['results']['shop']
    except KeyError:
        # 'shop' key not found
        return 0, 404
    except:
        # API Server error
        return 0, 500

    return shop_data, 200


# def info_pack


# ORM
def update_database(request):
    '''
    Save to DB form models
    Returns:
        searched_location: dict: search arguments dictionary
        error_state: int: 200, 400, 404
    '''
    selected_lat = None
    selected_lng = None
    if request.method == 'POST':
        if request.POST.get('selectCurrentLocationRange'):
            range_ = request.POST['selectCurrentLocationRange']
            order = request.POST['selectCurrentLocationOrder']
            current_lng = request.POST['CurrentLat']
            current_lat = request.POST['CurrentLng']
            lat = current_lat
            lng = current_lng
        elif request.POST.get('selectSelectedLocationRange'):
            range_ = request.POST['selectSelectedLocationRange']
            order = request.POST['selectSelectedLocationOrder']
            selected_lat = request.POST['selected_lat']
            selected_lng = request.POST['selected_lng']
            current_lng = request.POST['BySelectedCurrentLng']
            current_lat = request.POST['BySelectedCurrentLat']
            lat = selected_lat
            lng = selected_lng
        else:
            return {}, 400

        searched_location = {'searched_lat': lat,
                             'searched_lng': lng,
                             'current_lat': current_lat,
                             'current_lng': current_lng,
                             'selected_lat': selected_lat,
                             'selected_lng': selected_lng,
                             'range': range_,
                             'order': order,}
        cache.set('searched_location', searched_location)

        shop_info_json, state = hot_pepper_api(lat=lat, lng=lng, range=range_
                                        , order=order, count=100,)
        if not shop_info_json:
            return searched_location, 404

        shop_info = info_pack(shop_info_json,
                              SHOP_INFO_MODEL_FORM, lat, lng)
        model_form_save(shop_info, SHOP_INFO_MODEL_FORM)
        return searched_location, 200

    elif request.method == 'GET':
        searched_location = cache.get('searched_location')
        return searched_location, 200

    else:
        return {}, 400


# error
def err_check(state):
    '''

    '''
    if state == 400:
        return CONST.BAD_REQUEST,
    elif state == 404:
        return CONST.NOT_FOUND
    elif state == 502:
        return CONST.BAD_GATEWAY
    else:
        return CONST.INTERNAL_SERVER_ERROR


def err_direct(request,msg,state=500):
    '''

    '''
    if state == 404:
        contexts = {}
        searched_location = cache.get('searched_location')
        if searched_location['selected_lat']:
            contexts = {'is_selected': True}

        return render(request, 'result_error.html', contexts)
    else:
        contexts = {'error_code': state,
                    'error_message': msg,
                    }
        return render(request, 'error_base.html', contexts)


# views
def index(request):
    '''
    apps.result.index
    '''
    api_key = get_key(CONST.GOOGLE_API)
    contexts = {'api_key': api_key}
    return render(request, 'result_index.html', contexts)


def result(request):
    '''
    apps.result.result(search-result)

    Raise:
        400 Bad Request: Get invalid request method
        404 Not Found: No search result
    Return:
        request to result_show()
    '''
    # GET method (page move request)
    if request.method == 'GET':
        searched_location, state = update_database(request)
        page = request.GET.get('page')

    # POST method (new search request)
    elif request.method == 'POST':
        # new search method > db clear
        SHOP_INFO_MODEL_FORM.objects.all().delete()
        searched_location, state = update_database(request)
        page = 1

    # bad request
    else:
        searched_location = {}
        state = 400

    if state == 200:
        return result_show(request, searched_location, page=page)

    else:
        error_message = err_check(state)
        return err_direct(request, error_message, state)


def result_show(request, searched_location, **kwargs):  ########################################!!
    '''
    Show shop search result
    Args:
        request
        searched_location: dict: dict of search arguments
        **kwargs: page number
    Returns:
        render
    '''

    searched_lat = searched_location['searched_lat']
    searched_lng = searched_location['searched_lng']
    # load shop/user info from database by searchedlatlng and userlatlng
    # 여기 트라이 있었음
    shop_list = SHOP_INFO_MODEL_FORM.objects.filter(searched_lat=searched_lat, searched_lng=searched_lng)

    # 여기 익셉션 있었음 NoSearchResult하려면 있어야함
    # except Exception: raise Exception('NoSearchResult')

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

    contexts = {
        'page_object': page_object,
        'paginator': paginator,
        'len_page_objects': len(page_object) * page_object.number,
        'len_shop_list': len(shop_list),
    }
    return render(request, 'result.html', contexts)


def detail(request):
    '''
    apps.result.detail(shop-detail-info)

    Raises:
        400 Bad Request: Get invalid request method
    Returns:
        render
    '''
    if request.method == 'GET':
        shop_id = request.GET.get('shop_id')
        detail_info_json, state = hot_pepper_api(id=shop_id)
        if state != 200:
            error_message = err_check(state)
            return err_direct(request, error_message, state)
        else:
            detail_info = info_pack([detail_info_json], SHOP_DETAIL_MODEL_FORM)
        contexts = detail_info[0]
        #
        # # 사실상 필요없는 작업이 되어버림
        # print("db 넣기 전")
        # print(detail_info)
        # # avoid duplication of data
        # if not SHOP_DETAIL_MODEL_FORM.objects.filter(detail_shop_id=shop_id).exists():
        #     model_form_save(detail_info, SHOP_DETAIL_MODEL_FORM)
        # detail_info = SHOP_DETAIL_MODEL_FORM.objects.get(detail_shop_id=shop_id)
        # print("db 넣은 후")
        # print(detail_info)
        # contexts = detail_info.__dict__
        # # 사실상 필요없음

        return render(request, 'result_detail.html', contexts)

    else:
        # Bad Request
        return err_direct(request, 'Bad Request', 400)


def info_pack(info_json, model_form, lat=None, lng=None):
    '''
    pack information to djagno-modelform-template
    Args:
        info_json: list[dict]: hotpepper_response['results']['shop'] format dicts list
        model_form: django.models.ModelForm object
        (lat): float: searched latitude
        (lng): float: searched longitude
    Returns:
        list[dict{}]
    '''
    info_package = []
    if model_form == SHOP_DETAIL_MODEL_FORM:
        info_json = detail_processing(info_json)
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
                'searched_lat': lat,
                'searched_lng': lng,
            }
            info_package.append(model_template)

    return info_package

def detail_processing(info_json):
    shop = info_json[0]
    temp_text = shop['open'].replace('）','）♩')
    temp_list = temp_text.split('♩')
    shop['open'] = temp_list
    print(shop['open'])
    print(shop)
    return [shop]