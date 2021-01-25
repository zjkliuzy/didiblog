from django.http import *
from django.shortcuts import render


def test_cors(request):
    return render(request, "test_cors.html")


def test_cors_server(request):
    return HttpResponse("成功了")
