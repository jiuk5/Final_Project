from django.urls import path
from . import views

app_name = 'landmark'

urlpatterns = [
    path('',views.index,name='index'),
    path('test1/', views.modelloadtest, name='test1'),
    path('landmark/upload/',views.upload, name='upload'),
    path('landmark/upload_create/',views.upload_create,name='upload_create'),
    path('landmark/profile/',views.profile,name='profile'),
]