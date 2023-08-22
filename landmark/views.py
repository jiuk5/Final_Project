from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import LandmarkForm
from .models import Profile
import torch
import pandas as pd
import os
import joblib
from django.conf import settings
import numpy as np
from django.contrib.auth.models import User
from django.contrib import auth



file_path = './machine_model'
machine_list = os.listdir(file_path)
#model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')  
df_info = pd.read_csv('./final_info.csv', encoding='utf-8')
df_hotel = pd.read_csv('./hotel.csv', encoding='euc-kr')
landmark_name = []


for i in df_info['name_info']:
    split = i.split('_')
    landmark_name.append(split)

def index(request):
    return render(request, 'landmark/index.html')

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],password=request.POST["password1"])
            auth.login(request,user)
            return redirect('home')
        return render(request, 'landmark/signup.html')
    
    return render(request, 'landmark/signup.html')
    
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'landmark/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('home')



def upload(request):
    if request.method == 'POST':
        form = LandmarkForm(request.POST, request.FILES)
        if form.is_valid():     # 값에 이상이 없으면 (유효성 검사) 
            form.save()         # 저장
            return redirect(reverse('landmark:index'))
        
    else:
        form = LandmarkForm()
        
    return render(request, 'landmark/upload.html', {'form':form})





#def file_list(request):
    list = Profile.objects.all().order_by('-pk')
    results = model1(f'./media/{list[0].imgfile}')
    dict = results.pandas().xyxy[0].to_dict(orient="records")  
    name = dict[0]['name']
    name_split = name.split('_')[0]
    
    index_n = []
    for i in range(len(df_hotel['랜드마크'])):
        if name_split == df_hotel['랜드마크'][i].split('_')[0]:
            index_n.append(i)
    price = []
    star = []
    hotel_name = []
    for i in index_n:
        hotel_name.append(df_hotel.loc[i]['호텔이름'])
        price.append(df_hotel.loc[i]['금액'])
        star.append(df_hotel.loc[i]['등급'])
    price = np.array(price).reshape(-1,1)
    star = np.array(star).reshape(-1,1)
    
    pkl_n = []
    for i in range(len(machine_list)):
        if machine_list[i].split('_')[0] == name_split:
            pkl_n.append(i)

    score = '높음'
    for i in range(len(pkl_n)):
        if i == 0:
            model = joblib.load(f'./machine_model/{machine_list[pkl_n[i]]}')
            hotel_price_list = []
            for i in range(len(hotel_name)):

                rate = model.predict(price)[i]

                cluster = ['낮음', '중간', '높음']
                if cluster[rate] == score:
                    hotel_price_list.append(hotel_name[i])
        if i == 1:
            model = joblib.load(f'./machine_model/{machine_list[pkl_n[i]]}')
            hotel_star_list = []
            for i in range(len(hotel_name)):

                rate = model.predict(star)[i]

                cluster = ['낮음', '중간', '높음']
                if cluster[rate] == score:
                    hotel_star_list.append(hotel_name[i])
        
        
    #   'hotel_price_list':hotel_price_list, 'hotel_price_list':hotel_price_list  
        
    for i in range(len(landmark_name)):
        if name_split == landmark_name[i][0]:
            index = i
            country = landmark_name[-1]
    name = df_info.loc[index]['name']
    info = df_info.loc[index]['info']
    time = df_info.loc[index]['time']
    address = df_info.loc[index]['address']
    content = {'hotel_star_list':hotel_star_list,'hotel_price_list':hotel_price_list,'list':list,'name':name,'info':info, 'time':time, 'address':address, }
    return render(request, 'landmark/file_list.html', content)


def delete_file(request, id):
    file = Profile.objects.get(pk=id)

    # 실제 업로드 된 파일도 삭제 (삭제할 때 db 뿐만 아니라 실제 파일도 삭제하기 위해서) 
    media_root = settings.MEDIA_ROOT
    remove_file = media_root + "/" + str(file.imgfile)
    print('삭제할 파일: ', remove_file)
    
    if os.path.isfile(remove_file): # remove_file 이 존재한다면
        os.remove(remove_file)      # 실제 파일 삭제
    
    file.delete()   # DB에서 삭제 (데이터베이스에 들어있는 값을 삭제)
    
    return redirect(reverse('landmark:list'))

