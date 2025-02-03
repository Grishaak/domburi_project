from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("<h2>Start django recipes site.</h2>")
