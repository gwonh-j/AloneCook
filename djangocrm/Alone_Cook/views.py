from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm

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

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('Alone_Cook:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'Alone_Cook/question_detail.html', context)


def question_create(request):
    if request.method == 'POST': # post 요청일 때는 입력한 값들을 전달받아 DB에 저장
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('Alone_Cook:index')
    else: # Get 요청일 때는 단순히 질문등록 페이지 요청
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'Alone_Cook/question_form.html', context)
