from django.shortcuts import render
from logic.const import Const, current_location
from . import models


# Logical
CONST = Const()

# use API
def get_current_latlng():
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    context = {'current_lat': current_lat, 'current_lng': current_lng}
    return context

def get_selected_latlng():
    api_key = get_api(CONST.GOOGLE_API)
    current_lat, current_lng = get_latlng(api_key)
    selected_lat, selected_lng = 1,1
    context = {
        'current_lat': current_lat, 'current_lng': current_lng,
        'selected_lat': selected_lat, 'selected_lng': selected_lng}
    return context

# views
def index(request):
    current_latlng = get_current_latlng()
    return render(request, 'result_index.html', current_latlng)

def result(request):
    return render(request, 'result.html', current_latlng)