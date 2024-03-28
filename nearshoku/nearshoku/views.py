from django.shortcuts import render
from . import settings

def index(request):
    return render(request, 'result_index.html')