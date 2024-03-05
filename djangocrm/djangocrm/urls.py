from django.contrib import admin
from django.urls import include, path
from Alone_Cook import views

urlpatterns = [
    path('common/', include('common.urls')),
    path('Alone_Cook/', include('Alone_Cook.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # '/' 에 해당되는 path
    
]
