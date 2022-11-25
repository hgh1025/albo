from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length= 20)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length = 100)
    user_validate = models.BooleanField(default = False)
    


class Item(models.Model):
    item_name = models.CharField(max_length = 20)
    item_price = models.IntegerField(null=True)
    item_content = models.TextField(max_length = 200) 
    item_img = models.ImageField(upload_to="images/", blank=True, null=True)
    item_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'[{self.pk}]{self.item_name}'

    def get_absolute_url(self):
        return f'/upload/posting/{self.pk}/'



        