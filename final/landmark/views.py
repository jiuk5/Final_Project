from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image
# Create your views here.

import joblib
from django.http.response import HttpResponse
import pandas as pd
import numpy as np
import os

hotel = pd.read_csv('hotel.csv', encoding='cp949')
info = pd.read_csv('final_info.csv')

def modelloadtest(request):
    model = joblib.load('HollyWood_price.pkl')
    
    rate = model.predict([[250000]])[0]
    
    cluster = ['낮음', '중간', '높음']

    price = hotel[hotel['랜드마크'] == 'HollyWood Sign']['금액'].tolist()
    star =  hotel[hotel['랜드마크'] == 'HollyWood Sign']['등급'].tolist()
    hotelname = hotel[hotel['랜드마크'] == 'HollyWood Sign']['호텔이름'].tolist()
    price_np = np.array(price).reshape(-1, 1)
    star_np = np.array(star).reshape(-1, 1) 
    
    folder_path = './machine_model'
    pkl_list = os.listdir(folder_path)
    
    pkl = []
    for i in range(len(pkl_list)):
        b = pkl_list[i].split('_')[0]
        pkl.append(b)
    
    x = 'HollyWood Sign'
    a = x.split(' ')[0]
    list = []
    for i in range(len(pkl_list)):
        if a == pkl[i] :
            list.append(i)
            
    cl = input("금액 : ")
    hotel_list = []
    for i in range(len(hotelname)):

        rate = model.predict(price_np)[i]

        cluster = ['낮음', '중간', '높음']
        print(hotelname)
        if cluster[rate] == cl:
            hotel_list.append(hotelname[i])
            
    return render(request, 'landmark/index.html', {'hotel_list':hotel_list})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location='./media', base_url='media')
        # FileSystemStorage.save(file_name, file_content)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'landmark/image.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'landmark/image.html')

import torch
import pandas as pd
# from .models import Info

def landmark(request):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='model.pt')
    
    path = 'media/CN.jpg'

    image = model(path)
    a = image.pandas().xyxy[0].to_dict(orient="records")
    b = a[0]['name'].split('_')[0]
    
    x = info['name_info']
    landmark = []
    for i in range(len(info)):
        y = x[i].split('_')[0]
        landmark.append(y)
    
    for i in range(len(landmark)):
        if b == landmark[i]:
            name = info.loc[i]['name']
            inform = info.loc[i]['info']
            time = info.loc[i]['time']
            address = info.loc[i]['address']
            # Info(name=name, inform=inform, time=time, address=address).save()
            
    return render(request, "landmark/landmark.html")
