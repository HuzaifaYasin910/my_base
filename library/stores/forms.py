from django import forms
from .models import Book,Subscribers

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'



class SubscribersForm(forms.ModelForm):
    class Meta:
        model   = Subscribers
        fields  = '__all__'