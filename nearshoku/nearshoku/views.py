from django.shortcuts import render
from . import settings


def index(request):
    # direct to nearshoku.apps.result
    return render(request, 'result_index.html')