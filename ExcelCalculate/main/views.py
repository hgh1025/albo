from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import * 
from django.db import connection

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
    return render(request, 'main/signin.html')

def login(request):
    loginEmail = request.POST['loginEmail'] # signin.html <input name=loginEmail> 사용을 위해
    loginPW = request.POST['loginPW']  # signin.html <input name=loginPW> 사용을 위해
    user = User.objects.get(user_email = loginEmail)
    if user.user_password == loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_index')
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
    # if request.method == "POST":
    #     name = request.POST.get('items_name')
    #     content = request.POST.get('items_content')
    #     pirce = request.POST.get('items_pirce')
    #     new_item =  Item()
    #     new_item.text = name
    #     new_item.text = content
    #     new_item.text = pirce
    #     new_item.save()
        return render(request, 'main/upload.html')
    

def posting(request):
    # if request.method == "POST":
    #     temp = request.POST.get('items_input')
    #     new_item =  Item()
    #     new_item.text = temp
    #     new_item.save()
    #     return render(request, 'main/posting.html',{'items':new_item})
    items = Item.objects.all().order_by('-pk') 

    print(request)
    item_name = request.POST['item_name']
    item_price =request.POST['item_price']
    item_content = request.POST['item_content']
    item_img= request.FILES['item_img']
    

    new_name = Item(item_name=item_name, item_price=item_price, item_content=item_content, item_img = item_img)
    
    new_name.save()
     
    return render(request, 'main/posting.html',{'items':items})




def blog(request):
    blogs = Item.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옴 
    return render(request, 'main/blog.html', {'blogs':blogs})
    

def new_post(request, pk):
  
  items = Item.objects.get(pk=pk)

 
  return render(request, 'main/new_post.html',{'items': items})
    

def remove_post(request, pk):
    post = Item.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog/')
    return render(request, "main/remove_post.html", {'post':post})



