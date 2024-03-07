from django.urls import path
from . import views

app_name = "Alone_Cook"

urlpatterns = [
    path("", views.index, name='index'), # localhost:8000/ 주소의 루트를 의미함

    # 게시글 제목의 a 태그에 href 속성에 해당하는 동적 URL 매핑
    path("<int:question_id>", views.detail, name= 'detail'),

    path("answer/create/<int:question_id>/", views.answer_create, name="answer_create"),

    path('question/create/', views.question_create, name='question_create'),

    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
]

