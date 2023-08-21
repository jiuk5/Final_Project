from django.shortcuts import render, redirect
from django. http import HttpResponse, HttpResponseRedirect
from . models import Profile
import joblib

def index(request):
    print('hi')
    return render(request, 'landmark/index.html')


def modelloadtest(request):
    landmark = joblib.load()

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