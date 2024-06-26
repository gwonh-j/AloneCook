from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests, json
from django.conf import settings

from ..models import Question, Answer

API_KEY = settings.API_KEY


def index(request):
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준

    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')

    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so,
            }
    return render(request, 'Alone_Cook/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent') # 정렬 기준

    if so == 'recommend':
        answer_list = Answer.objects.filter(question=question).annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    else:  # recent
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    paginator = Paginator(answer_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj, 'page': page, 'so': so}
    return render(request, 'Alone_Cook/question_detail.html', context)

#http://openapi.foodsafetykorea.go.kr/api/keyId/serviceId/dataType/startIdx/endIdx
@api_view(['GET'])
def foods(request):
    url = 'http://openapi.foodsafetykorea.go.kr/api'
    params = {
        'keyId': API_KEY,
        'serviceId': 'COOKRCP01',
        'dataType': 'json',
        'startIdx': '1',
        'endIdx': '1000' 
    }
    response = requests.get(url, params=params)
    products_data = response.json()['result']['baseList']
    
    return Response(products_data)