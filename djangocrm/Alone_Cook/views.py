from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    max_index = len(paginator.page_range)

    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj,'max_index':max_index}
    return render(request, 'Alone_Cook/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    # question = Question.objects.get(id = question_id)

    context = {'question' : question}
    return render(request, 'Alone_Cook\question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('Alone_Cook:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'Alone_Cook/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST': # post 요청일 때는 입력한 값들을 전달받아 DB에 저장
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('Alone_Cook:index')
    else: # Get 요청일 때는 단순히 질문등록 페이지 요청
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'Alone_Cook/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('Alone_Cook:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('Alone_Cook:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'Alone_Cook/question_form.html', context)