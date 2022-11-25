from django.shortcuts import render, redirect
from django.http import HttpResponse
# import pandas as pd
from datetime import datetime
from .models import *
# Create your views here.
def calculate(request):
    file = request.FILES['fileInput']
    # print("# 사용자가 등록한 파일의 이름: ", file)

    #파일 저장하기
    origin_file_name = file.name
    user_name = request.session['user_name']
    now_HMS = datetime.today().strftime('%H%M%S')
    file_upload_name = now_HMS+'_'+user_name+'_'+origin_file_name
    file.name = file_upload_name
    document = Document(user_upload_file = file)
    document.save()
   