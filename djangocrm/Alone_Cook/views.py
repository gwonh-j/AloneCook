from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("안녕하세요! 자취밥의 메인페이지입니다.")