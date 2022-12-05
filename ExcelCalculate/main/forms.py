from .models import *
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets= {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels={
            'comment': '질문',
        }

class ReCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'reply_location']

class EditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields= ['item_name','item_price','item_content','item_img']


# class status(forms.ModelForm):
#     class Meta:
#         model = Trade
#         fields = ['item_img', 'item_status','item_price']