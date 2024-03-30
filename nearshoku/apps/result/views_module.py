


def model_form_save(item_list, form_model):
    """
    Save the items into the modelform(db)

    Args:
        item_list(list): list of dict items
        form_model(models.Model): model form in models.py
    """
    object_bulk = [form_model(**item) for item in item_list]
    form_model.objects.bulk_create(object_bulk)


def make_hash():# 필요없어짐
    """
    Make hash key from current time

    Returns: hash key (int)
    """
    import time
    key = time.time_ns()
    return hash(key)






def get_latlng(api_key):
    """
    Get server's current lat/lng from google-geolocation
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


def get_current_latlng():
    '''

    '''
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    context = {'current_lat': current_lat, 'current_lng': current_lng}
    return context


def info_processor(dict, key, to_value, from_list, exceptions=None, unicode_check=True, is_split=None):
    '''

    '''
    # funcs
    def replace_info(info, from_list, to_value):
        '''

        '''
        for from_value in from_list:
            info = info.replace(from_value, to_value + ';')
        return info

    def replace_info_exceptions(info, first_check, second_check, to_value):
        '''

        '''
        info = info.replace(first_check, to_value + ';')
        info = info.replace(second_check, to_value + ';')
        return info

    def text_split(text, symbol):
        '''

        '''
        temp_list = text.split(symbol)
        return temp_list

    # process
    info = dict[key]
    if unicode_check:
        info = check_unicode(info)

    info = replace_info(info,from_list,to_value)

    if exceptions is not None:
        for first_check, second_check in exceptions.items():
            info = replace_info_exceptions(info, first_check, second_check, to_value)

    info = text_split(info, ';')

    return info