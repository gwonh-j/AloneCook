from django.contrib import admin
from django.urls import include, path
from Alone_Cook.views import base_views

urlpatterns = [
    path('foods/', base_views.foods, name='foods'),
    path('common/', include('common.urls')),
    path('Alone_Cook/', include('Alone_Cook.urls')),
    path('admin/', admin.site.urls),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path

    
]
