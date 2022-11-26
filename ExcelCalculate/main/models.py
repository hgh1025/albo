from django.db import models

# Create your models here.
class User(models.Model):
    # user_num = models.AutoField(primary_key=True) #회원번호
   #-----------------------------------------------------
    user_name = models.CharField(max_length= 20)
    # user_id = models.CharField(max_legth = 10, unique=True)
    user_date = models.DateTimeField(auto_now_add=True) #가입일(처음 등록한 시간으로 저장)
    # user_nickname = models.CharField(max_legth = 10, unique=True) #닉네임
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length = 100)
    user_validate = models.BooleanField(default = False)
    def __str__(self):
        return f'[{self.pk}]{self.user_name}'
    
    

class Item(models.Model):
    # user_num = models.ForeignKey('User',  on_delete = models.CASCADE) #판매자 번호(fk)
    # item_id = models.AutoField(primary_key=True) #게시글ID
     #-------------------------------------------------
    # trade_status = models.CharField() #거래상태(판매중,거래완료)
    item_name = models.CharField(max_length = 20)
    item_price = models.IntegerField(null=True)
    item_content = models.TextField(max_length = 200) 
    item_img = models.ImageField(upload_to="images/", blank=True, null=True)
    item_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.pk}]{self.item_name}'

    def get_absolute_url(self):
        return f'/upload/posting/{self.pk}/'
    
  

       
# class Comment(models.Model):
#     comment_id = models.AutoField(primary_key=True) #댓글번호
#     user_id = models.ForeignKey('User', related_name='commenter', on_delete = models.CASCADE) #댓글/답글 작성자
#     item_id = models.ForeignKey('Item', related_name='post', on_delete = models.CASCADE) #게시글ID
#     comment = models.TextField() #댓글/답글 내용
#     comment_date = models.DateTimeField(auto_now_add=True) #등록날짜
#     comment_state = models.CharField() #상태(댓글or답글)
#     reply_location = models.IntegerField() #위치 : 댓글은 -1 / 답글은 해당 댓글의 댓글번호 부여



        