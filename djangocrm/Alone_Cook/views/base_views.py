from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question
from ..models import Answer

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준
        # 정렬
    if so == 'recommend':
        # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    max_index = len(paginator.page_range)

    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj,'max_index':max_index, 'page': page, 'kw': kw}
    return render(request, 'Alone_Cook/question_list.html', context)

def detail(request, question_id):
    
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent') # 정렬 기준

    if so == 'recommend':
        answer_list = Answer.objects.annotate(
            num_voter=Count('voter'))(question=question).order_by('-num_voter', '-create_date')

    else:  # recent
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')
    
    question = get_object_or_404(Question, pk=question_id)
    
    #answer_list = question.answer_set.all() # 질문을통해 답변 리스트 찾기
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    context = {'question' : question, 'answer_list' : page_obj}
    return render(request, 'Alone_Cook/question_detail.html', context)


