from django.urls import path
from . import views

app_name = 'landmark'

urlpatterns = [
    path('', views.index, name ='index'),
    path('test/', views.modelloadtest, name='test'),
    path('image/', views.simple_upload, name='image' ),
    # path('img/', views.landmark, name = 'landmark'),
]
