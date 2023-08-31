from django.urls import path
from . import views

app_name = 'landmark'

urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('upload/',views.upload, name='upload'),
    path('list/<int:id>/',views.file_list,name='list'),
    path('info/<int:id>/', views.file_info, name='info'),
    path('delete/<int:id>/', views.delete_file, name='delete'),
    path('result/<int:id>/', views.result, name='result'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
]