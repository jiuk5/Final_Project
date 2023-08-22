from django.shortcuts import render, redirect
from django. http.response import HttpResponse, HttpResponseRedirect
from . models import Profile
import joblib
import torch

#model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')

def index(request):
    print('hi')
    return render(request, 'landmark/index.html')


def modelloadtest(request):
    landmark = joblib.load('Deoksugung_price.pkl')
    pre = landmark.predict([[2000000]])[0]
    
    cluster = ['높음', '중간', '낮음']
    a =  cluster[pre]
    #return HttpResponse(a)
    return render(request, 'landmark/test1.html', {'a':a})

def upload(request):
    return render(request, 'landmark/upload.html')

def upload_create(request):
    form=Profile()
    form.title=request.POST['title']
    try:
        form.image=request.FILES['image']
    except:
        pass
    form.save()
    return redirect('/landmark/profile/')

def profile(request):
    profile=Profile.objects.all()
    return render(request, 'profile.html', {'profile':profile})