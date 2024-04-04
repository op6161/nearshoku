from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
from . import models
from .views_module import model_form_save


# settings, modules
def constant(func):
    """A decorator function for creating constant properties in a class.

    This decorator is intended to be used with a class '_Const' to create constant properties.
    It ensures that the decorated property can not be modified after initialization.

    Args:
        func: function: The function that returns the constant value.

    Returns:
        property: A property object that acts as a constant property.
    """

    def func_set(self, value):
        """Raises TypeError when attempting to set the constant property."""
        raise TypeError

    def func_get(self):
        """Returns the constant value."""
        return func()

    return property(func_get, func_set)


class _Const(object):
    """A container for constant values.

    This class provides a convenient way to define and access constant values.
    Constants are defined as properties using the @constant decorator,
    ensuring that they cannot be modified after initialization.

    Example:
        GOOGLE_API: str = _Const.GOOGLE_API
        NOT_FOUND: str = _Const.BAD_REQUEST
    """

    @constant
    def GOOGLE_API():
        # a .env file data key that saved the google api key
        # It will be used on 'index' to show the google map(JS) that to select the location
        # or 'detail' to show the google map(static) that to show the location of restaurant
        return 'GEOLOCATION_API_KEY'

    @constant
    def RECRUIT_API():
        # a .env file data key that saved the hotpepper api key
        # It will be used to load shop info
        return 'HOTPEPPER_API_KEY'


def parsing_xml_to_json(xml_data):
    """
    Parse the xml data into json format

    Args:
         xml_data :requests.Response : The XML data obtained from a web request.

    Returns:
        str: JSON-formatted data converted from the XML input.
        (requests.Response.text() json format)
    """
    import xmltodict
    import json
    xml_pars = xmltodict.parse(xml_data.text)
    json_dump = json.dumps(xml_pars)
    json_data = json.loads(json_dump)
    return json_data


def check_u3000(item, exception=False):
    """Replace all '\u3000' to ' ' (space) in the input string(and list, dict).

    it works left-side first

    Args:
        item: str, list, dict, None: the string(s) that has unicode u3000
            If 'item' is a list or dict, its elements should be type of str or None.
        exception (bool, optional): If True, exceptions will be raised when encountering errors during replacement.
            Defaults to False.

    Raises:
        ValueError: if the item is invalid type

    Returns:
        item: str, list, dict, None: the string(s) that changed from u3000 to space
    """
    if isinstance(item, str):
        # if item is a string
        return item.replace('\u3000', ' ')
    elif isinstance(item, list):
        # if item is a list
        temp_list = []
        for text in item:
            # If exception is True, Export errors if there is a problem with internal elements
            if exception:
                try:
                    temp_list.append(text.replace('\u3000', ' '))
                except Exception:
                    raise Exception

            # If exception is False, Ignore errors on internal elements
            else:
                try:
                    temp_list.append(text.replace('\u3000', ' '))
                except:
                    temp_key.append(text)
        return templist

    elif item is None:
        # When processing database data
        # To prevent an error from stopping when there is None data
        return None

    elif isinstance(item, dict):
        temp_keys = []
        temp_vals = []
        for key, val in item.items():
            # If exception is True, Export errors if there is a problem with internal elements
            if exception:
                try:
                    temp_keys.append(key.replace('\u3000', ' '))
                    temp_vals.append(val.replace('\u3000', ' '))
                except Exception:
                    raise Exception

            # If exception is False, Ignore errors on internal elements
            else:
                try:
                    temp_keys.append(key.replace('\u3000', ' '))
                    temp_vals.append(val.replace('\u3000', ' '))
                except Exception:
                    temp_keys.append(key)
                    temp_vals.append(val)
        return dict(zip(temp_keys, temp_vals))

    else:
        # if item is a invalid type value
        raise TypeError(f'invalid type{type(item).__name__}')


def check_list_has_blank(list_data):
    """Remove blank elements from the input list

        Args:
            list_data: list: The list to be checked for blank elements.

        Raises:
            TypeError: If list_data is not a list.

        Returns:
            list: The list with blank elements removed.
    """
    if not isinstance(list_data, list):
        raise TypeError('list_data must be a list')
    temp_list_data = []
    for data in list_data:
        if data != '':
            temp_list_data.append(data)
    return temp_list_data


def combine_dictionary(dict1, dict2):
    """Combine two dictionaries. but they should have different keys

    * If the two dicts have same keys, values from dict2 will update
    the corresponding values in dict1.
     * If the dictionaries have different keys, the function will simply merge them.

    Args:
        dict1: dict
        dict2: dict

    Returns:
         dict: A dictionary containing the combined key-value pairs from both dictionaries.
    """
    dict1.update(dict2)
    return dict1


class InfoProcessor:
    """A class to split and replace string

    This class provides methods to split a string based on a specified symbol or
     to replace specific values in a given string with another value.

        Examples:
        - To split a string:
            processor = InfoProcessor('hello world', mode='split', from_value='o')
            result = processor.result
            # result will be ['hello', ' wo', 'rld']

        - To replace specific values in a string:
            processor = InfoProcessor('hello world', mode='replace', from_value='o', to_value='p')
            result = processor.result
            # result will be 'hellp wprld'

        - To perform both split and replace operations:
            processor = InfoProcessor('hello world', mode='all', from_value='o', to_value='p')
            result = processor.result
            # result will be ['hellp', ' wp', 'rld']

        Args:
            string :str : The string to be processed
            mode :str: The processing mode. Possible values are "split", "replace", "all".
            to_value :str: The value to replace or the symbol to split on.
            from_value :str,list (optional): The target to replace or the symbols to split on.
                if you want to 'split', this argument is essential.
            replace_ex :dict (optional): A dictionary for exception handling.
            unicode_check :bool (optional): Whether to check for Unicode.

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
            self.info = string

        if not isinstance(to_value, str) and to_value is not None:
            # if to_value is not a None/string
            raise ValueError('to_value must be "str"')

        if from_value is not None and not isinstance(from_value, (str, list)):
            # if from_value is not a None/string/list
            raise ValueError('from_value must be "str" or "list"')

        if mode != 'replace' and from_value is None:
            # if mode is 'replace', it requires from_value
            raise ValueError('split require "from_value" parameter')

        if not isinstance(replace_ex, (dict, type(None))):
            # if replace_ex is not a Dictionary
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
        mode = self.mode
        from_value = self.from_value
        replace_ex = self.replace_ex

        # If mode is 'replace', 'to_value' will be used just to replace
        to_value = self.to_value
        if mode != 'replace':
            # If mode is 'split'/'all', 'to_value' will be used to replace and to split too
            # ';' is a flag to split. It must be replaced if the data already contains ';'.
            to_value = to_value + ';'

        if isinstance(from_value, list):
            # If from_value is a list, it's working normally
            info = self._replace_info(info, from_value, to_value)
        elif isinstance(from_value, str):
            # If from_value is a str, it must be formulated to a list
            # (because _replace_info() has for loop in 'from_value' list)
            info = self._replace_info(info, [from_value], to_value)

        if replace_ex:
            # If replace_ex came in
            for first_check, second_check in zip(replace_ex.keys(), replace_ex.values()):
                info = self._replace_info_exceptions(info, first_check, second_check, to_value)
        return info

    def _split(self):
        """Split a given string based on a specified symbol"""
        info = self.info
        # ';' is a flag to split. It must be replaced if the data already contains ';'.
        info = self._text_split(info, ';')
        return info

    def _split_set(self):
        """Check split point when mode is 'split'"""
        # if mode is 'split', it must set special
        # splitting need 'to_value' but 'split' mode don't need to_value.
        # so from_value must be changed to 'to_value'
        # It's complicated, but I did this for parameter's consistency.

        info = self.info
        if isinstance(self.from_value, list):
            # If 'from_value' is a list
            # Add flags to all 'from_value' list's variables to split.
            from_value_list = self.from_value
            for from_value in from_value_list:
                to_value = from_value + ';'
                info = self._replace_info(info, from_value, to_value)
        else:
            # If 'from_value' is a string, add flag to split.
            from_value = self.from_value
            to_value = from_value + ';'
            info = self._replace_info(info, from_value, to_value)
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
    else:
        return key


def hot_pepper_api(**kwargs):
    """Get shops data from using recruit-hot-pepper API

    Args:
        **kwargs: hot-pepper api params key=value reference https://webservice.recruit.co.jp/doc/hotpepper/reference.html

    Returns:
        shop_data:list[dicts{}],dict{}: hot pepper api response parsed to json format
        error_state: int: 200, 404, 500
    """
    API_HOST = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    headers = {'Content-Type': 'application/json',
               'charset': 'UTF-8',
               'Accept': '*/*'}

    import requests
    api_key = get_key(CONST.RECRUIT_API)
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
        return None, 500

    data_json = parsing_xml_to_json(hot_pepper_response)

    try:
        shop_data = data_json['results']['shop']
        return shop_data, 200
    except KeyError:
        # 'shop' key not found
        # when occurred no search results
        return None, 404
    except:
        # API Server error
        return None, 500


# error
def err_direct(request, state=500):
    """Handle direct error response

    Args:
        request: HttpRequest: Django HTTP request
        state: int(optional): state code received from logical functions

    Returns:
        HttpResponse: The rendered error response page
    """

    def err_check(check_state):
        """Internal function to check error code

        Args:
            check_state: int: state code received from logical functions

        Returns:
            str: error message
        """
        if check_state == 400:
            return 'Bad Request', 'Request Error!'

        elif check_state == 404:
            return 'No Search Result', 'Search Error!'

        else:
            return 'Server Error!', 'Server Error!'

    # ----------------------------------------------------------------

    err_msg, err_title = err_check(state)
    contexts = {'state': state,
                'err_msg': err_msg,
                'title': err_title}

    if state == 404:
        search_by = request.session['search_by']

        if search_by == 'selected':
            contexts['is_selected'] = True
        else:
            contexts['is_current'] = True

    return render(request, 'result_error.html', contexts)


# views
def index(request):
    """View function to render 'index' of 'result' app

    In this function, retrieve the GOOGLE_MAP_API key using get_key()
    and pass it to result_index template for rendering.
    Then the result_index page load google-maps to select location to search

    Args:
        request: HttpRequest: Django HTTP request
    Returns:
        HttpResponse: Render 'result_index' page of 'result app'
    """
    api_key = get_key(CONST.GOOGLE_API)
    contexts = {'api_key': api_key}
    return render(request, 'result_index.html', contexts)


def result(request):
    """View function to render 'search result' of 'result' app

    result() function handles both 'GET' and 'POST' requests.
    For 'POST' request, it processes the form data to retrieve search-results
        from hot-pepper-API and stores them in the session.
    For 'GET' request, it retrieves the stored search-results by API from session
        and paginate them to display on template.
    If the API call is unsuccessful, calls err_direct() to render 'result_error'

    Return:
        HttpResponse:
            result: Render 'result' page of 'result app'
            400 Bad Request: Render 'result_error' page of 'result app' when an invalid request method is received
            404 Not Found: Render 'result_error' page of 'result app' when no search results received by API server.
    """

    def post_shop_info(request):
        """Internal function to process POST request and retrieve search results from hot-pepper-API

        post_shop_info() retrieves param data from POST request, send a request to hot-pepper-API to retrieve shop data.
        And store them in session.

        Args:
            request: HttpRequest: Django HTTP request

        Raises:
            ValueError: If the request method is not POST.

        Returns:
            int: A state code of hot_pepper_api() function
                - 200: If the API call was successful
                - others: If there was an error
        """
        if request.method == 'POST':
            # Delete an existing session
            request.session.flush()

            # Init API params
            range_ = request.POST['range_select']
            order = request.POST['order_select']
            current_lng = request.POST['current_lng']
            current_lat = request.POST['current_lat']

            if request.POST.get('submitSelectedLocation') == 'True':
                selected_lat = request.POST['selected_lat']
                selected_lng = request.POST['selected_lng']
                search_lat = selected_lat
                search_lng = selected_lng
            else:
                selected_lat, selected_lng = None, None
                search_lat = current_lat
                search_lng = current_lng

            # 'search_by' will use when there are no search results
            # 'no search result from your location/from you selected'
            if selected_lat:
                request.session['search_by'] = 'selected'
            else:
                request.session['search_by'] = 'current'

            # request api
            shop_info_json, api_state = hot_pepper_api(lat=search_lat, lng=search_lng, range=range_, order=order,
                                                       count=100)

            if isinstance(shop_info_json, dict):
                # If hot_pepper_api result is only 1 shop
                # shop_info_json would be dictionary type not dictionaries list
                # So I need to convert it
                shop_info_json = [shop_info_json]

            if api_state != 200:
                # API error occurred
                return api_state

            shop_info = info_pack(shop_info_json, SHOP_INFO_MODEL_FORM)

            # Save data to session
            request.session['shop_info'] = shop_info
            return api_state
        else:
            raise ValueError('post_shop_info() requires request.method POST')

    # ----------------------------------------------------------------

    def result_method_check(request):
        """Internal function to check the request method and dispatch the processing accordingly.

        result_method_check() examines the request method and dispatches the processing accordingly.
        If request method is 'POST', it calls post_shop_info() to process the POST request.
        If request method is 'GET', it sets the function state to 200 and retrieved 'page' to proceed result() process.

        Args:
            request: HttpRequest: Django HTTP request

        Returns:
            Tuple(int, str): A tuple containing the function state and page parameter
         """
        if request.method == 'POST':
            f_state = post_shop_info(request)
            request_page = None
        elif request.method == 'GET':
            f_state = 200
            request_page = request.GET.get('page')
            if not request_page:
                # For PRG pattern
                request_page = 1
        else:
            f_state = 400
            request_page = None

        return f_state, request_page

    # ----------------------------------------------------------------

    # load saved data in session
    state, page = result_method_check(request)

    if state != 200:
        # loading failed
        return err_direct(request, state)

    elif request.method == 'POST':
        # POST Redirect GET to prevent POST redirecting error
        return redirect('result')

    else:  # request.method == 'GET'
        PAGING_POST_NUMBER = 10
        shop_list = request.session.get('shop_info')
        paginator = Paginator(shop_list, PAGING_POST_NUMBER)

        try:
            # Normal operation
            page_object = paginator.page(page)
        except EmptyPage:
            # page is empty (if ?page=99999)
            page = paginator.num_pages
            page_object = paginator.page(page)
        except PageNotAnInteger:
            # page is not an integer
            # (and post-redirect-get)
            page = 1
            page_object = paginator.page(page)
        except:
            # Direction is incorrect
            return err_direct(request, 400)

        contexts = {
            'page_object': page_object,
            'paginator': paginator,
            'cur_page_min_number': len(page_object) * page_object.number - len(page_object) + 1,
            'cur_page_max_number': len(page_object) * page_object.number,
            'cur_page_shop_number_sub': 0 - int(len(page_object)),
            'cur_page_shop_number': len(page_object),
            'len_shop_list': len(shop_list),
            'cur_page': page,
            'max_page': paginator.num_pages}
        return render(request, 'result.html', contexts)


def detail(request):
    """View function to render 'search_detail' of 'result' app

    detail() handles GET request to retrieve detailed information about a shop
    from hot-pepper-API based on the provided shop-id.
    If the API call is successful, it renders 'result_detail' page with retrieved information of 'result app'.
    If the API call is unsuccessful, calls err_direct() to render 'result_error'.

    Returns:
        HttpResponse:
            result_detail: Render 'result_detail' page of 'result app'.
            err_direct: Render 'result_error' page of 'result app'.
    """
    if request.method == 'GET':
        shop_id = request.GET.get('shop_id')

        if shop_id is None:
            # Direction is incorrect
            return err_direct(request, 400)

        detail_info_json, state = hot_pepper_api(id=shop_id)

        if state != 200:
            # API error
            return err_direct(request, state)
        else:
            # Normal operation
            detail_info = info_pack([detail_info_json], SHOP_DETAIL_MODEL_FORM)
            contexts = detail_info[0]
            return render(request, 'result_detail.html', contexts)
    else:
        # Bad Request
        return err_direct(request, 400)


def info_pack(info_json, model_form):
    """Pack information to prepare display on the page

    info_pack() takes a list of dicts retrieved from hot-pepper-API shop information response['result']['shop'] format.
    Process that using InfoProcessor class, and formats it according to the specified data format.

    Args:
        info_json: list[dict]: hotpepper_response['results']['shop'] format dicts list
            A list of dictionaries representing shop information.
        model_form: django.models.ModelForm: The Django model form object to
            determine the format of the output information.

    Returns:
        list[dict]: A list of dictionaries of shop information formatted for template variables name to
            be displayed on the page.
    """

    def use_info_processor(info_json, key, mode, to_value=None, from_value=None,
                           replace_ex=None, unicode_check=True, ):
        """Use InfoProcessor class to process information in this project

        use_info_processor() is an internal function to apply the InfoProcessor class to
        process information in the project.
        It iterates over each shop dictionary in the info_json(list),
        extracts the specified key from the hot-pepper-API, processes the value using the InfoProcessor class and
        updates the value in the shop dictionary with the processed result.
        Finally, it returns the list of shop dictionaries with processed information.

        * If the mode is 'all' or 'split', the value is converted from str to list.

        Args:
            info_json: list[dict]: A list of dictionaries of shop information.
            key: str: The key to extract from shop dictionary.
            mode: str: The processing mode for InfoProcessor.
                Possible values ar "split", "replace", "all"
            to_value: str(optional): The value to replace or the symbol to split on.
            from_value: str, list(optional): The target to replace or the symbol to split on.
            replace_ex: dict(optional): A dictionary for exception replace handling.
            unicode_check: (bool, optional): Check u3000 to replace ' '(space). Default is True.

        Returns:
            list[dict]: A list of dictionaries processed shop information

        """

        temp_shop_list = []
        for shop in info_json:
            temp_shop = shop
            if isinstance(key, list):
                string = shop[key[0]][key[1]]
            else:
                string = shop[key]

            if isinstance(string, list):
                string = ';'.join(string)

            info_processor = InfoProcessor(string=string,
                                           mode=mode,
                                           to_value=to_value,
                                           from_value=from_value,
                                           replace_ex=replace_ex,
                                           unicode_check=unicode_check, )

            # if the data includes '', it will be replaced a new line.
            # so it must be deleted
            if isinstance(key, list):
                temp_shop[key[0]][key[1]] = check_list_has_blank(info_processor.result)
            else:
                temp_shop[key] = check_list_has_blank(info_processor.result)
            temp_shop_list.append(temp_shop)
            del info_processor
        return temp_shop_list

    # ----------------------------------------------------------------

    def use_replace(info_json, key, from_to_dict):
        """Replace specified values in the 'info_json' dictionary.

            This function is used to replace specified values in the 'info_json' dictionary
            with corresponding values provided in 'from_to_dict'.

            Args:
                info_json: list[dict]: A list of dictionaries containing shop information.
                key: str: The key in the shop dictionary to be replaced.
                from_to_dict: dict: A dictionary with values to be replaced as keys and their replacements as values.

            Returns:
                list[dict]: A list of dictionaries with replaced values.
            """
        for from_v, to_v in from_to_dict.items():
            info_processor = InfoProcessor(info_json[0][key], mode='replace', unicode_check=False,
                                           from_value=from_v, to_value=to_v)
            info_json[0][key] = info_processor.result
            del info_processor
        return info_json

    # ----------------------------------------------------------------

    def special_1_processing(info_json):
        """Process special case of data in 'info_json'

            This function processes a special case of data in 'info_json'. It identifies specific pattern.
            and manipulates the data accordingly.

            Args:
                info_json: list[dict]: A list of dictionaries containing shop information.

            Returns:
                list[dict]: A list of dictionaries with processed special case data.
            """
        shop = info_json[0]

        # a flag to split lines
        # it will replace to green-line in Templates
        flag = '§'
        temp_time = []

        # ['月: ', '10:30~12:30', '火: ', '11:00~13:30'] > ['月: ', '§', '10:30~12:30', '火: ', '§', '11:00~13:30']
        # Then the page appears like this
        # 月:
        # ----
        # 10:30~12:30
        # 火:
        # ----
        # 11:00~13:30

        for idx, open_time in enumerate(shop['open']):
            if open_time[0] in ['月', '火', '水', '木', '金',
                                '金', '土', '日', '祝'] and idx != 0:  # Don't add flag to the first line
                temp_time.append(flag)
            temp_time.append(open_time)
        shop['open'] = ';'.join(temp_time)
        return [shop]

    # ----------------------------------------------------------------

    info_package = []

    # detail/shop both preprocessing ---------------------------------

    # split accesses to show several lines
    info_json = use_info_processor(info_json, mode='all',
                                   key='access',
                                   to_value='分',
                                   from_value=['分。', '分／', '分/', '分，',
                                               '分、', '分』', '分！', '分♪'],
                                   replace_ex={'分!!': '分!'})

    # special case: shop_id=J000638173
    info_json = use_info_processor(info_json,
                                   key='access',
                                   from_value='◇',
                                   to_value=';',
                                   mode='all')

    # Split long genre into two lines
    info_json = use_info_processor(info_json,
                                   key=['genre', 'name'],
                                   mode='all',
                                   from_value='・',
                                   to_value=';')

    # detail info preprocessing ---------------------------------
    if model_form == SHOP_DETAIL_MODEL_FORM:

        # '14:3017:00' → '14:30、17:00' formatting
        info_json = use_replace(info_json,
                                key='open',
                                from_to_dict={':300': ':30、0', ':000': ':00、0',
                                              ':301': ':30、1', ':001': ':00、1'})

        # case shop_id=J003433085
        # ':30月' > ':30','月'
        info_json = use_replace(info_json,
                                key='open',
                                from_to_dict={":30月": ":30;月",
                                              ":00月": ":00;月",
                                              ":30火": ":30;火",
                                              ":00火": ":00;火",
                                              ":30水": ":30;水",
                                              ":00水": ":00;水",
                                              ":30木": ":30;木",
                                              ":00木": ":00;木",
                                              ":30金": ":30;金",
                                              ":00金": ":00;金",
                                              ":30土": ":30;土",
                                              ":00土": ":00;土",
                                              ":30日": ":30;日",
                                              ":00日": ":00;日",
                                              }
                                )

        info_json = use_info_processor(info_json,
                                       key='open',
                                       mode='split',
                                       from_value='）')

        # To split 'open' with <hr class='green-line'>
        info_json = special_1_processing(info_json)

        # To change ':\n' if ': ' found
        # It's this format when data 'open' shows the time of day
        # ['月: 10:30~12:30火: 11:00~13:30']
        # So, this code will make 'open' to be divided into several lines
        # like ['月: ', '10:30~12:30', '火: ', '11:00~13:30']
        info_json = use_replace(info_json,
                                key='open',
                                from_to_dict={": ": ":;"})
        info_json = use_info_processor(info_json,
                                       key='open',
                                       mode='split',
                                       from_value=';')

        for shop in info_json:
            model_template = {
                # 필수
                'detail_shop_id': shop['id'],
                'detail_name': check_u3000(shop['name']),
                'detail_address': check_u3000(shop['address']),
                'detail_image': shop['photo']['pc']['l'],
                'detail_time': shop['open'],
                # 추가
                'detail_kana': check_u3000(shop['name_kana']),
                'detail_access_list': shop['access'],
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
                'api_key': get_key(CONST.GOOGLE_API),
            }
            info_package.append(model_template)

    # shop info preprocessing ---------------------------------
    elif model_form == SHOP_INFO_MODEL_FORM:
        for shop in info_json:
            model_template = {
                'shop_id': shop['id'],
                'shop_name': check_u3000(shop['name']),
                'shop_kana': check_u3000(shop['name_kana']),
                'shop_access_list': shop['access'],
                'shop_thumbnail': shop['logo_image'],
                'shop_genre': shop['genre']['name'],
                'shop_card': shop['card'],
                'shop_open': shop['open'],
            }
            info_package.append(model_template)

    return info_package

#  test codes  #
