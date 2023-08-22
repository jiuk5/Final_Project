from django.urls import path
from . import views

app_name = 'landmark'

urlpatterns = [
    path('',views.index,name='index'),
    #path('test1/', views.modelloadtest, name='test1'),
    path('/upload/',views.upload, name='upload'),
    #path('list/',views.file_list,name='list'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
]