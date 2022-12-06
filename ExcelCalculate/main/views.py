from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import * 
from django.db import connection
from django.urls import reverse
from django.db.models import Q # Q는 Django내 Model을 관리할 때 사용되는 ORM으로 SQL의 WHERE절과 같은 조건문을 추가할 때 사용한다.
from .forms import *
from datetime import datetime

from PIL import Image
import tensorflow as tf
import os,glob
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Dense, GlobalAveragePooling2D
import shutil


import pandas as pd
# Create your views here.
def index(request):
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html')
    else:
        return redirect('main_signin')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print(request)
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()
    code = randint(1000, 9999)
    response = redirect('main_verifyCode')
    response.set_cookie('code', code)
    response.set_cookie('user_id',user.id)
    # 이메일 발송 함수 호출
    send_result = send(email,code)
    if send_result:
        return response
    else:
        return HttpResponse("이메일 발송에 실패했습니다.")

def signin(request):
    # username = User.objects.get(['user_name'])
    # password = User.objects.get(['user_password'])
    # if username and password:
    #     try:
    #         member = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         self.add_error('username', '아이디가 없습니다!')
    #         return
    #     # 예외처리를 하고 return 을 실행해서 바로 아래 코드를 실행하지 않고 빠져나오게 한다.

    # if not password(password, member.password):
    #     self.add_error('password', '비밀번호가 다릅니다!')
    # else:
    #     self.user_id = member.id

    return render(request, 'main/signin.html')

def login(request):
    loginEmail = request.POST['loginEmail'] # signin.html <input name=loginEmail> 사용을 위해
    loginPW = request.POST['loginPW']  # signin.html <input name=loginPW> 사용을 위해
    user = User.objects.get(user_email = loginEmail)
    if user.user_password == loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_upload')
    else:
        return redirect('main_signin')   

def logout(request):
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_signin')

def verifyCode(request): 
    return render(request, 'main/verifyCode.html')

def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
       
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return response
    else:
        redirect('main_verifyCode')

def result(request):
    if 'user_name' in request.session.keys():

        return render(request, 'main/result.html')
    else:
        return redirect('main_signin')

def upload(request):
 
        return render(request, 'main/upload.html')
    

def posting(request):
 
    items = Item.objects.all().order_by('-pk') 
    # users = Item.objects.filter().select_related("write_name") #fk추가
    users = User.objects.get(user_name=request.session['user_name']) #fk추가
    print(request)
    print(users)

    trade_status = request.POST.get('trade_status')
    item_name = request.POST.get('item_name',False)
    item_price =request.POST.get('item_price',False)
    item_content = request.POST.get('item_content',False)
    item_img= request.FILES.get('item_img')
    now_HMS = datetime.today().strftime('%Y.%H.%M.%S')
    item_upload_name  = now_HMS + '.jpeg'
    item_img.name = item_upload_name 
    new_name = Item(trade_status=trade_status, item_name=item_name, item_price=item_price, item_content=item_content, item_img = item_img, user_name= users)# model = ...
    
    new_name.save()
     
    return render(request, 'main/posting.html',{'items':items})




def blog(request):
    blogs = Item.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옴 
    return render(request, 'main/blog.html', {'blogs':blogs})
    

def new_post(request, pk):
    
    items = Item.objects.get(pk=pk)
    
    # trade_status = items.trade_status
    login_user = request.session['user_name']
    post_user = str(items.user_name)
     
    comments = CommentForm() #forms.py
   
    context = dict()
    context['items'] = items
    context['comments'] = comments
    context['login_user'] = login_user
    context['post_user'] =  post_user
    context['trade_status'] = items.trade_status
                                  #1/14 맞으면 삭제
    return render(request, 'main/new_post.html', context)
    
UPLOAD_DIR = r'C:\albino\My-albo\ExcelCalculate\media\images'


#가격예측버튼 누르면 실행되는 함수
def predict_price(request):
    #predict_img = request.POST['predict_img']

    if 'file1' in request.FILES:
        file = request.FILES['file1']
        file_name = file.name
        fp = open("%s%s" % (UPLOAD_DIR, file_name), 'wb')

    for chunk in file.chunks():
        fp.write(chunk)
        fp.close()

    model_weight_path = r'C:\albino\My-albo\ExcelCalculate\epoch100.h5'
    img = Image.open("%s%s"%(UPLOAD_DIR,file_name))


    #가격예측함수
    def predict(model_path, img):
        
        model_saved = load_model(model_path)

        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)

        prediction = model_saved.predict(img)
        label = np.argmax(prediction[0])

        if label == 0:
            return '10만원 이상 45만원 미만'
        elif label == 1:
            return '45만원 이하 80만원 미만'
        else:
            return '80만원 이상 160만원 미만'

    
    
    context = dict()
    context['predict'] = predict(model_weight_path, img)

    return render(request, 'main/upload.html', context) 
# def remove_post(request, pk):
#     #사용자가 작성자라면 삭제 (22.11.29 허지훈)
#     user_name = User.objects.filter(user_name=pk)
#     post = Item.objects.filter(user_name=pk)
    
#     if request.method == post:
#         form = EditForm(request.POST, request.FILES)

#         if form.is_valid():
#             post.delete()
#         return redirect('new_post' ,{'user_name': user_name})
    
#     else:
#         form = EditForm()
    
#     return render(request, 'main/new_post.html' ,{'user_name': user_name})
    
 
# def remove_post(request, pk):
#     #사용자가 작성자라면 삭제 (22.11.29 허지훈)
#     post = Item.objects.get(pk=pk)
#     # request = User.objects.get(user_name=request.session['user_name'])
#     remove_request =  request.session['user_name']
   
#     if remove_request != post.user_name:
#         return render(request, 'main/new_post.html',{'post': post})    
    
#     post.delete()
    
#     print(post)
#     print(remove_request)
#     return render(request, 'main/posting.html',{'post': post}) 

    
def remove_post(request, pk):
    post = Item.objects.get(pk=pk)
    items = Item.objects.all()
    # request.method == 'POST'
    post.delete()
    return render(request, 'main/index.html', {'items':items})
    


def boardEdit(request, pk):
    # board = User.objects.filter(user_name=pk)
    items = Item.objects.get(pk=pk)
    # board = User.objects.filter(user_name=request.session['user_name'])
     
    if request.method == "POST":
       
        items.item_name = request.POST.get('item_name')
        items.item_content = request.POST.get('item_content')
        items.item_price = request.POST.get('item_price')
        # items.item_img =request.FILES.get('item_img')
        items.trade_status =request.POST.get('trade_status')

        # new_item = Item(item_name=item_name, item_price=item_price, item_content=item_content, item_img = item_img, items=items)
        # # new_board = User(board=board)
        
        items.save()

        items = Item.objects.get(pk=pk)
    
        if items.trade_status == "거래완료":
            item_img = items.item_img
            item_price = items.item_price
            
            status = Trade(item_img=item_img, item_price=item_price)
            
            status.save()

    items = Item.objects.all()
    # context = dict()
    # context['item'] = items  
    print(type(items))
    print(items)
   
   
    return render(request, 'main/posting.html', {'items':items})
 
   

def create_comment(request, items_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.cleaned_data['comment']
        parent=None
        

    user = User.objects.get(user_name=request.session['user_name'])
    items = Item.objects.get(pk=items_id)
    

    new_comment = Comment(comment=comment, user_name=user, item_id=items, parent=parent)
    new_comment.save()

    return redirect('main_new_post', items_id)

def create_reply(request, items_id):
    reply_form = ReplyForm(request.POST) 
    if reply_form.is_valid():
        parent = reply_form.cleaned_data['parent']
        reply = reply_form.cleaned_data['comment']
        

    user = User.objects.get(user_name=request.session['user_name'])
    items = Item.objects.get(pk=items_id)

    print("hello")

    new_comment = Comment(comment=reply, user_name=user, item_id=items, parent=parent)
    new_comment.save()

    return redirect('main_new_post', items_id)


def trade(request, item_id):
    filled_form = Trade(request.POST) #POST 요청이 들어오면,
    if filled_form.is_valid(): #유효성 검사 성공시 진행
        
        temp_form = filled_form.save(commit=False)
        
        temp_form.item_id = Item.objects.get(id=item_id)
        temp_form.user_name = User.objects.get(user_name=request.session['user_name'])
        temp_form.item_status = "거래상태"
        temp_form.save()
    return redirect('posting', {'trade':trade})



