from logic.const import Const
from django.shortcuts import render
from logic.current_location import get_latlng, get_location, get_api

CONST = Const()


def index(request):
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    return render(request, 'index.html',{'current_lat':current_lat, 'current_lng':current_lng})