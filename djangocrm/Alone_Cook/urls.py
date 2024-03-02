from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # localhost:8000/Alone_Cook 주소의 루트
    path('test/',views.test)
]