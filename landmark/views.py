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
from django.contrib.auth.decorators import login_required



file_path = './machine_model'
landmark_pic_list = os.listdir('./media/landmark_pic')
machine_list = os.listdir(file_path)
model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')  
df_info = pd.read_csv('./final_info.csv', encoding='euc-kr')
df_hotel = pd.read_csv('./hotel.csv', encoding='euc-kr')
landmark_name = []
pic_list = []


for i in range(len(landmark_pic_list)):
    split_pic = landmark_pic_list[i].split('_')
    pic_list.append(split_pic)

for i in df_info['name_info']:
    split = i.split('_')
    landmark_name.append(split)

@login_required
def index(request):
    return render(request, 'landmark/index.html')

def home(request):
    return render(request, 'landmark/home.html')


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],password=request.POST["password1"])
            auth.login(request,user)
            return redirect(reverse('landmark:login'))
        return render(request, 'landmark/signup.html')
    
    return render(request, 'landmark/signup.html')
    

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(reverse('landmark:index'))
        else:
            return render(request, 'landmark/login.html', {'error': 'ID or Password is incorrect'})
    else:
        return render(request, 'landmark/login.html')
    
@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('landmark:login'))


@login_required
def upload(request):
    if request.method == 'POST':
        form = LandmarkForm(request.POST, request.FILES)
        if form.is_valid():    # 값에 이상이 없으면 (유효성 검사) 
            if request.user.is_authenticated:
                landmark_instance = form.save(commit=False)         # 저장
                landmark_instance.user = request.user
                landmark_instance.save()
                
                return redirect(reverse('landmark:info', args=[landmark_instance.id]))
            else:
                pass
        
    else:
        form = LandmarkForm()
        
    return render(request, 'landmark/upload.html', {'form':form})

def predict(info):
    results = model1(info)
    records = results.pandas().xyxy[0].to_dict(orient="records")
    if records:
        name = records[0]['name']
        name_split = name.split('_')[0]
        name_split1 = name_split.split('_')[0]
    
        return name_split1
    else:
        return records

@login_required
def file_list(request, id):
    id = request.user.id
    profiles = Profile.objects.filter(user_id=id).order_by('pk')
    content={'profiles':profiles}
    return render(request, 'landmark/file_list.html', content)

@login_required
def file_info(request, id):
    file = Profile.objects.get(pk=id)
    imgfile_path = f'./media/{file.imgfile}'
    
    if predict(imgfile_path):
        name_split = predict(imgfile_path)
        if name_split == 'Jerusalem':
            name_split = 'Dome'
        for i in range(len(pic_list)):
            if name_split == pic_list[i][0]:
                pic_index = i
        try:
            landmark_pic = landmark_pic_list[pic_index]
        except NameError:
            landmark_pic = None
            
        for i in range(len(landmark_name)):
            if name_split == landmark_name[i][0]:
                index = i
        name = df_info.loc[index]['name']
        info = df_info.loc[index]['info']
        time = df_info.loc[index]['time']
        address = df_info.loc[index]['address']
        content = {
            'file':file,
            'name':name,
            'info':info,
            'time':time,
            'address':address,
            'landmark_pic':landmark_pic
            }
        return render(request, 'landmark/file_info.html', content)
    else:
        return render(request, 'landmark/error.html')

@login_required
def result(request, id):
    file = Profile.objects.get(pk=id)
    imgfile_path = f'./media/{file.imgfile}'
    name_split = predict(imgfile_path)
    if name_split == 'Jerusalem':
        name_split = 'Dome'
    price_input = request.POST['price']
    star_input = request.POST['star']
    
    index_n = []
    for i in range(len(df_hotel['랜드마크'])):
        if name_split == df_hotel['랜드마크'][i].split('_')[0]:
            index_n.append(i)
    price_list = []
    star_list = []
    rate_list = []
    hotel_name = []
    hotel_link = []
    for i in index_n:
        hotel_name.append(df_hotel.loc[i]['호텔이름'])
        price_list.append(df_hotel.loc[i]['금액'])
        star_list.append(df_hotel.loc[i]['등급'])
        rate_list.append(df_hotel.loc[i]['평점'])
        hotel_link.append(df_hotel.loc[i]['링크'])
    price = np.array(price_list).reshape(-1,1)
    star = np.array(star_list).reshape(-1,1)
    
    pkl_n = []
    for i in range(len(machine_list)):
        if machine_list[i].split('_')[0] == name_split:
            pkl_n.append(i)
        
    for i in range(len(pkl_n)):
        if i == 0:
            model = joblib.load(f'./machine_model/{machine_list[pkl_n[i]]}')
            hotel_price_list = []
            hotel_price_link = []
            hotel_price_price = []
            hotel_price_star = []
            hotel_price_rate = []
        
            for i in range(len(hotel_name)):

                rate = model.predict(price)[i]

                cluster = ['낮음', '중간', '높음']
                if cluster[rate] == price_input:
                    hotel_price_list.append(hotel_name[i])
                    hotel_price_link.append(hotel_link[i])
                    hotel_price_price.append(price_list[i])
                    hotel_price_star.append(star_list[i])
                    hotel_price_rate.append(rate_list[i])
        elif i == 1:
            model = joblib.load(f'./machine_model/{machine_list[pkl_n[i]]}')
            hotel_star_list = []
            hotel_star_link = []
            hotel_star_price = []
            hotel_star_star = []
            hotel_star_rate = []
        
            for i in range(len(hotel_name)):

                rate = model.predict(star)[i]

                cluster = ['낮음', '중간', '높음']
                if cluster[rate] == star_input:
                    hotel_star_list.append(hotel_name[i])
                    hotel_star_link.append(hotel_link[i])
                    hotel_star_price.append(price_list[i])
                    hotel_star_star.append(star_list[i])
                    hotel_star_rate.append(rate_list[i])
    zipped_data_price = zip(hotel_price_list, hotel_price_link,hotel_price_price,hotel_price_star,hotel_price_rate)
    zipped_data_star = zip(hotel_star_list, hotel_star_link,hotel_star_price,hotel_star_star,hotel_star_rate)            
    context = {'zipped_data_star':zipped_data_star,'zipped_data_price':zipped_data_price,'hotel_price_link':hotel_price_link,'hotel_star_link':hotel_star_link,'price_input':price_input,'star_input':star_input,'hotel_star_list':hotel_star_list,'hotel_price_list':hotel_price_list}
        
    return render(request, 'landmark/result.html', context)
    
@login_required
def delete_file(request, id):
    try:
        file = Profile.objects.get(pk=id)
        # 실제 업로드 된 파일도 삭제 (삭제할 때 db 뿐만 아니라 실제 파일도 삭제하기 위해서) 
        media_root = settings.MEDIA_ROOT
        remove_file = media_root + "/" + str(file.imgfile)
        print('삭제할 파일: ', remove_file)

        if os.path.isfile(remove_file): # remove_file 이 존재한다면
            os.remove(remove_file)      # 실제 파일 삭제

        file.delete()   # DB에서 삭제 (데이터베이스에 들어있는 값을 삭제)
    except Profile.DoesNotExist:
        pass
    
    return redirect(reverse('landmark:list', args=[id]))


