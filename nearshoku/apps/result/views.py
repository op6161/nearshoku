from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.cache import cache
from . import models
from .views_module import model_form_save


# settings, modules
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


def parsing_xml_to_json(xml_data):
    """
    Parse the xml data into json format

    Args:
         xml_data(requests.get():xml format)

    Returns:
        json_data(requests.get().txt:json format)
    """
    import xmltodict
    import json
    xml_pars = xmltodict.parse(xml_data.text)
    json_dump = json.dumps(xml_pars)
    json_data = json.loads(json_dump)
    return json_data


def check_u3000(item):
    """
    Replace the str has unicode u3000 -> ' ' (space)

    Args:
        item:str,list,dict,None: the string(s) that has unicode u3000

    Raises:
        ValueError: if the item is invalid type

    Returns:
        item:str,list,dict,None: the string(s) that changed from u3000 to space
    """
    item_type = type(item).__name__

    if item_type == 'str':
        return item.replace('\u3000', ' ')

    elif item_type == 'list':
        temp_list = []
        for text in item:
            temp_list.append(text.replace('\u3000', ' '))
        return templist

    elif item is None:
        return None

    elif item_type == dict:
        temp_keys = []
        temp_vals = []
        for key, val in item.items():
            tenp_keys.append(key.replace('\u3000', ' '))
            temp_vals.append(val.replace('\u3000', ' '))
        return dict(zip(temp_keys, temp_vals))

    else:
        raise ValueError(f'invalid type{type(item).__name__}')


def combine_dictionary(dict1, dict2):
    """
    Combine two dictionaries. but they should have different keys
    * if dicts have same keys, it can update dict1's value without combining

    Args:
        dict1: dict:
        dict2: dict:

    Returns:
         dict: dict:
    """
    dict1.update(dict2)
    return dict1


class InfoProcessor:
    """A class to split and replace string

    'string', 'mode' are essential args


    mode 'split' require from_value (it can be a list or string)
        (if 'string' is 'hello world' and from_value is 'o' : result ['hello','wo','rld']
    mode 'replace' require from_value and to_value
        (if 'string' is 'hello world' and from_value is 'o' to_value is 'p' : result 'hellp wprld'
    mode 'all' require from_value and to_value
        (if 'string' is 'hello world' and f:'o' t:'p' : result ['hellp' 'wp' 'rld']

        Args:
            string :str : The string to be processed
            mode :str: The processing mode. Possible values are "split", "replace", "all"
            to_value :str: The value to replace or the symbol to split on
            from_value :str,list (optional): The target to replace or the symbols to split on
            replace_ex :dict (optional): A dictionary for exception handling
            unicode_check :bool (optional): Whether to check for Unicode

        Raises:
            ValueError: If the input parameters are invalid or if required parameters are missing

        Attributes:
            info: A property to store the processed result

        Methods:
            _replace_split():
                Performs replace mode followed by split mode
            _replace():
                Replaces specific values in a given string
            _split():
                Splits a given string based on a specified symbol
            _split_set():
                Check split point when mode is 'split'
            result:
                A property to retrieve the processed result

        StaticMethods:
            _replace_info(info, from_list, to_value):
                Replaces specific values in a string with another value
            _replace_info_exceptions(info, first_check, second_check, to_value):
                Replaces specific values in a string with another value for exception handling
            _text_split(text, symbol):
                Splits a string into a list based on a specified symbol
        """
    def __init__(self, string, mode, from_value, to_value=None,
                 replace_ex=None, unicode_check=True):
        """Initialize InfoProcessor and process"""
        if not isinstance(string, str):
            raise ValueError('string must be a str')

        if unicode_check:
            self.info = check_u3000(string)
        else:
            self.info = list_

        if not isinstance(to_value, str) and to_value is not None:
            raise ValueError('to_value must be "str"')
        if from_value is not None and not isinstance(from_value, (str, list)):
            raise ValueError('from_value must be "str" or "list"')
        if mode != 'replace' and from_value is None:
            raise ValueError('split require "from_value" parameter')
        if not isinstance(replace_ex, (dict, type(None))):
            raise ValueError('"replace_ex" must be a dict')

        self.mode = mode
        self.to_value = to_value
        self.from_value = from_value
        self.replace_ex = replace_ex

        if mode == 'all':
            self.info = self._replace_split()
        elif mode == 'split':
            self.info = self._split_set()
            self.info = self._split()
        elif mode == 'replace':
            self.info = self._replace()
        elif mode is None:
            raise ValueError('InfoProcessor requires "mode" parameter')
        else:
            raise ValueError('Mode must be one of "split","replace","all"')

    def __str__(self):
        return f"InfoProcessor(mode='{self.mode}', to_value='{self.to_value}', from_value='{self.from_value}', replace_ex='{self.replace_ex}', info='{self.info}')"

    # funcs
    def _replace_split(self):
        """Perform replace mode followed by split mode"""
        self.info = self._replace()
        self.info = self._split()
        return self.info

    def _replace(self):
        """Replace specific values in a given string"""
        info = self.info
        from_value = self.from_value
        replace_ex = self.replace_ex
        to_value = self.to_value+';'

        if isinstance(from_value, list):
            info = self._replace_info(info, from_value, to_value)
        elif isinstance(from_value, str):
            info = self._replace_info(info, [from_value], to_value)

        if replace_ex:
            for first_check, second_check in zip(replace_ex.keys(), replace_ex.values()):
                info = self._replace_info_exceptions(info, first_check, second_check, to_value)
        return info

    def _split(self):
        """Split a given string based on a specified symbol"""
        info = self.info
        info = self._text_split(info, ';')
        return info

    def _split_set(self):
        """Check split point when mode is 'split'"""
        info = self.info
        if isinstance(self.from_value, list):
            from_value_list = self.from_value
            for from_value in from_value_list:
                to_value = from_value+';'
                info = self._replace_info(info, from_value, to_value)
        else:
            from_value = self.from_value
            to_value = from_value+';'
            info = self._replace_info(info,from_value,to_value)
        return info

    # static methods
    @staticmethod
    def _replace_info(info, from_list, to_value):
        """Replace specific values in a string with another value"""
        for from_value in from_list:
            info = info.replace(from_value, to_value)
        return info

    @staticmethod
    def _replace_info_exceptions(info, first_check, second_check, to_value):
        """Replace specific values in a string with another value for exception handling"""
        info = info.replace(first_check, to_value)
        info = info.replace(second_check, to_value)
        return info

    @staticmethod
    def _text_split(text, symbol):
        """Split a string into a list based on a specified symbol"""
        temp_list = text.split(symbol)
        return temp_list

    @property
    def result(self):
        """Retrieve the processed result"""
        return self.info


# init
CONST = _Const()
SHOP_INFO_MODEL_FORM = models.ShopInfoModel
USER_INFO_MODEL_FORM = models.UserInfoModel
SHOP_DETAIL_MODEL_FORM = models.ShopDetailModel


# use API function
def get_key(api_key_type):
    """Get protected key with from .env file use python-dotenv

    Args:
        api_key_type: str: A dotenv(.env) key

    Raises:
        ValueError: If api_type is not defined in .env file

    Returns:
        key: str: A dotenv(.env) value
    """
    from dotenv import load_dotenv
    import os
    load_dotenv()
    key = os.environ.get(api_key_type)
    if key is None:
        raise ValueError("Invalid api_key_type")
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
    except:
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
        # get new search method > db clear
        request.session.flush()
        searched_location, state = update_database(request)

        if state == 200:
            # request get page 1
            return redirect('result')

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
    # shop_list = SHOP_INFO_MODEL_FORM.objects.filter(searched_lat=searched_lat, searched_lng=searched_lng)
    shop_list = request.session.get('shop_info')
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
        'shop_list':shop_list,
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
            return render(request, 'result_detail.html', contexts)

    else:
        # Bad Request
        return err_direct(request, 'Bad Request', 400)

def update_database(request):
    '''
    Save to DB form models

    Returns:
        searched_location: dict: search arguments dictionary
        error_state: int: 200, 400, 404
    '''

    if request.method == 'POST':
        range_ = request.POST['range_select']
        order = request.POST['order_select']
        current_lng = request.POST['current_lng']
        current_lat = request.POST['current_lat']

        if request.POST.get('selected_lat'):
            selected_lat = request.POST['selected_lat']
            selected_lng = request.POST['selected_lng']
            lat = selected_lat
            lng = selected_lng

        else:
            selected_lat = None
            selected_lng = None
            lat = current_lat
            lng = current_lng

        searched_location = {'searched_lat': lat,
                             'searched_lng': lng,
                             'current_lat': current_lat,
                             'current_lng': current_lng,
                             'selected_lat': selected_lat,
                             'selected_lng': selected_lng,
                             'range': range_,
                             'order': order,}
        cache.set('searched_location', searched_location)

        shop_info_json, state = hot_pepper_api(lat=lat, lng=lng, range=range_, order=order, count=100,)

        if shop_info_json == 0:
            # got 0 from hot_pepper_api
            return searched_location, 404

        shop_info = info_pack(shop_info_json,
                              SHOP_INFO_MODEL_FORM, lat, lng)
        request.session['shop_info'] = shop_info

        # model_form_save(shop_info, SHOP_INFO_MODEL_FORM)
        return searched_location, 200

    elif request.method == 'GET':
        searched_location = cache.get('searched_location')
        return searched_location, 200

    else:
        return {}, 400

def info_pack(info_json, model_form, lat=None, lng=None):
    '''
    Pack information to show page
    Args:
        info_json: list[dict]: hotpepper_response['results']['shop'] format dicts list
        model_form: django.models.ModelForm object
        lat(optional): float: searched latitude
        lng(optional): float: searched longitude

    Returns:
        list[dict{}]
    '''

    # ----------------------------------------------------------------
    def use_info_processor(info_json, key, mode, to_value=None, from_value=None,
                           replace_ex=None, unicode_check=True, ):
        """Use InfoProcessor class for processing information in this project

        Args:
            info_json (list): A list of dictionaries containing information
            key (str): The key in each dictionary to be processed
            mode (str): The processing mode for InfoProcessor
            to_value (str, optional): The value to replace or the symbol to split on
            from_value (str or list, optional): The target to replace or the symbols to split on
            replace_ex (dict, optional): A dictionary for exception handling
            unicode_check (bool, optional): Whether to check for Unicode

        Returns:
            list: A list of dictionaries with processed information
        """
        temp_shop_list = []
        for shop in info_json:
            temp_shop = shop
            info_processor = InfoProcessor(string=shop[key],
                                           mode=mode,
                                           to_value=to_value,
                                           from_value=from_value,
                                           replace_ex=replace_ex,
                                           unicode_check=unicode_check, )
            temp_shop[key] = info_processor.result
            temp_shop_list.append(temp_shop)
            del info_processor
        return temp_shop_list
    # ----------------------------------------------------------------

    info_package = []

    info_json = use_info_processor(info_json, mode='all',
                                   key='access',
                                   to_value='分',
                                   from_value=['分。', '分／', '分/', '分，', '分、', '分』', '分！'],
                                   replace_ex={'分!!': '分!'})

    if model_form == SHOP_DETAIL_MODEL_FORM:
        # info_json = detail_processing_(info_json)
        info_json = use_info_processor(info_json,
                                       key='open',
                                       mode='split',
                                       from_value='）')
        for shop in info_json:
            model_template = {
                # 필수요구
                'detail_shop_id': shop['id'],
                'detail_name': check_u3000(shop['name']),
                'detail_address': check_u3000(shop['address']),
                'detail_image': shop['photo']['pc']['l'],
                'detail_time': shop['open'],
                # + info
                'detail_kana': check_u3000(shop['name_kana']),
                'detail_access': shop['access'],
                'detail_shop_memo': check_u3000(shop['shop_detail_memo']),
                'detail_budget_memo': check_u3000(shop['budget_memo']),
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
                'shop_name': check_u3000(shop['name']),
                'shop_kana': check_u3000(shop['name_kana']),
                'shop_access': shop['access'],
                'shop_thumbnail': shop['logo_image'],
                'searched_lat': lat,
                'searched_lng': lng,
            }
            info_package.append(model_template)

    return info_package

### test