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


def make_hash():# 필요없어짐
    """
    Make hash key from current time

    Returns: hash key (int)
    """
    import time
    key = time.time_ns()
    return hash(key)


def parsing_xml_to_json(xml_data): #사용하지 않음
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
