from django import forms
from .models import Book,Subscribers,Order

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'



class SubscribersForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=100)
    post_code = forms.CharField(max_length=100)