from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
import numpy as np
from datetime import datetime
from .models import *
from django.db import connection
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')

# Create your views here.
def calculate(request):
    file = request.FILES['fileInput']
    # print("# 사용자가 등록한 파일의 이름: ", file)

    #파일 저장하기
    origin_file_name = file.name
    # user_name = request.session['user_name']
    # now_HMS = datetime.today().strftime('%H%M%S')
    # file_upload_name = now_HMS+'_'+user_name+'_'+origin_file_name
    file_upload_name = origin_file_name
    file.name = file_upload_name
    document = Document(user_upload_file = file)
    document.save()

def chart(request):
    cursor = connection.cursor()
    sql = '''
        SELECT *
        FROM predict_data
        where price >=5000;
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(type(rows))
    print('rows : ',rows)
      
    user_date = [] # 년도를 저장할 리스트
    user_name = [] # salary를 저장할 리스트
      
    for row in rows:
        user_date.append(row[0])
        user_name.append(row[1])
    print(user_date)
    print(user_name)
    plt.plot(user_date, user_name) # post(x축데이터, y축데이터)
    plt.savefig('C:\practice\adminpractice\ExcelCalculate\calculate\static\images\chart.png') # 차트 이미지 저장
    return render(request, 'calculate/chart.html',{'rows',rows}) # rows데이터도 template으로 넘겨줌

# {% for %} 

# data= object.all()
# data.count

# {% endfor %}
