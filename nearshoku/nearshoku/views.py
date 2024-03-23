from logic.const import Const
from django.shortcuts import render
from logic.current_location import get_latlng, get_location, get_api

CONST = Const()

def get_current_latlng():
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    context = {'current_lat': current_lat, 'current_lng': current_lng}
    return context

def index(request):
    current_latlng = get_current_latlng()
    return render(request, 'result_index.html', current_latlng)