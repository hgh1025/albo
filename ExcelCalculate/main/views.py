from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import * 
from django.db import connection
from django.urls import reverse
from django.db.models import Q # Q는 Django내 Model을 관리할 때 사용되는 ORM으로 SQL의 WHERE절과 같은 조건문을 추가할 때 사용한다.



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
        # response.set_cookie('user', user)
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
    # if request.method == "POST":
    #     temp = request.POST.get('items_input')
    #     new_item =  Item()
    #     new_item.text = temp
    #     new_item.save()
    #     return render(request, 'main/posting.html',{'items':new_item})
    items = Item.objects.all().order_by('-pk') 
    # users = Item.objects.filter().select_related("write_name") #fk추가
    users = User.objects.get(user_name=request.session['user_name']) #fk추가
    print(request)
    item_name = request.POST['item_name']
    item_price =request.POST['item_price']
    item_content = request.POST['item_content']
    item_img= request.FILES['item_img']
    

    new_name = Item(item_name=item_name, item_price=item_price, item_content=item_content, item_img = item_img, user_name= users)# model = ...
    
    new_name.save()
     
    return render(request, 'main/posting.html',{'items':items})




def blog(request):
    blogs = Item.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옴 
    return render(request, 'main/blog.html', {'blogs':blogs})
    

def new_post(request, pk):
    
    items = Item.objects.get(pk=pk)
    
                                      #1/14 맞으면 삭제
    return render(request, 'main/new_post.html',{'items': items})
    

def remove_post(request, pk):
    #사용자가 작성자라면 삭제 (22.11.29 허지훈)
    user_name = User.objects.filter(user_name=pk)
    post = Item.objects.filter(user_name=pk)
    if user_name == post:
        user_name.delete()
        post.delete()
        return render(request, 'main/posting.html',{'user_name': user_name})
   
    else:
                                      #1/14 맞으면 삭제
        return render(request, 'main/posting.html',{'post': post})


def boardEdit(request, pk):
    board = User.objects.filter(user_name=pk)
    items = Item.objects.filter(user_name=pk)
    if request.method == "POST":
        # try:
        
        item_name = request.POST['item_name']
        item_content = request.POST['item_content']
        item_price = request.POST['item_price']
        item_img =request.POST['item_img']

        new_board = Item(item_name=item_name, item_price=item_price, item_content=item_content, item_img = item_img, board=board)
        new_board.save()
        return redirect('upload/posting/<int:pk>/boardEdit/',{'board':board})
        # except:
        #     return HttpResponse('정보가 일치하지 않습니다.')
    else:
        
        return render(request, 'main/boardEdit.html')
