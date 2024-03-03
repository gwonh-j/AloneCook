from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer
from django.utils import timezone

def index(request):
    question_list = Question.objects.order_by('-create_date') # -가 들어가면 내림차순
    context = {'question_list' : question_list}
    return render(request, 'Alone_Cook\question_list.html', context) # request, html 파일, 변수로 담아놨던 question_list

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    # question = Question.objects.get(id = question_id)

    context = {'question' : question}
    return render(request, 'Alone_Cook\question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # 아래 create 함수는 Answer 클래스 모델을 가져와 저장할 때 사용하는 save()랑 동일한 기능
    a = question.answer_set.create(content=request.POST.get("content"), create_date = timezone.now())
    return redirect("Alone_Cook:detail", question_id= question.id)