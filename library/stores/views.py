from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpRequest, HttpResponse , JsonResponse
from django.views.generic import CreateView,View
from django.urls import reverse_lazy
from .filters import BookFilter
import random
from django.contrib import messages
import os
from .utility import send_email

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.paginator import Paginator




    
   

def categorize_genres(genres):
    categorized_genres = {
        'fiction_genres': [],
        'nonfiction_genres': [],
        'children_genres': [],
    }
    for genre in genres:
        if genre.category == Genre.FICTION:
            categorized_genres['fiction_genres'].append(genre)
        elif genre.category == Genre.NON_FICTION:
            categorized_genres['nonfiction_genres'].append(genre)
        elif genre.category == Genre.CHILDREN:
            categorized_genres['children_genres'].append(genre)

    return categorized_genres

def genres(request):
    all_genres = Genre.objects.all()
    categorized_genres = categorize_genres(all_genres)
    return render(request, 'stores/genre.html', categorized_genres)

def children_genres(request):
    all_genres = Genre.objects.filter(category=Genre.CHILDREN)
    categorized_genres = categorize_genres(all_genres)
    context = {'categorized_genres':categorized_genres['children_genres']}
    return render(request, 'stores/books.html',context=context)

def books(request,genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books_list = genre.book_set.all()
    
    p = Paginator(books_list,1)
    page = request.GET.get('page')
    books = p.get_page(page)

    context = {
        'genre': genre,
        'books': books,
        'books_list':books_list
    }
    return render(request, 'stores/books.html', context)

def author(request):
    authors = Author.objects.all()
    p = Paginator(authors,15)    
    page = request.GET.get('page')
    authors = p.get_page(page)
    return render(request,'stores/authors.html',{'authors':authors})

def author_detail(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    books = author.book_set.all()
    p = Paginator(books,20)
    page = request.GET.get('page')
    books = p.get_page(page)
    return render(request, 'stores/authors-detail.html', {'author': author,'books':books})

def book_detail(request,book_id):
    book_detailed = get_object_or_404(Book,id=book_id)
    return render(request,'stores/book_detail.html',{'book':book_detailed})

def search(request):
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            my_model = Subscribers(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
            )
            try:
                if Subscribers.objects.filter(email = my_model.email).first():
                    messages.success(request, 'Email is already taken.')
                    subject = "Thank you for joinig our NewsLetter"
                    message = "Thank you for joinig our NewsLetter,we'll keep you notified for latest updates."
                    send_email(my_model.email,subject,message)
                    return redirect('#newsletter')
                else:
                    my_model.save()
                    return redirect('#newsletter')
            except Exception as e:
                print(e)
            
            
    else:
        form = SubscribersForm()

    book = Book.objects.all()
    if 'search_query' in request.GET and request.GET.get('search_query', '').strip():
        myfilter = BookFilter(request.GET, queryset=book)
        filtered_book = myfilter.qs
        print(filtered_book)
    else:
        myfilter = BookFilter(queryset=Book.objects.none())
        filtered_book = []
    

    return render(request, 'stores/index.html',{'form':form,'filtered_book':filtered_book})

def admin_local(request):
    orders = Order.objects.all()
    
    book   = Book.objects.all()
    if 'search_query' in request.GET and request.GET.get('search_query', '').strip():
        myfilter = BookFilter(request.GET, queryset=book)
        filtered_book = myfilter.qs
    else:
        myfilter = BookFilter(queryset=Book.objects.none())
        filtered_book = []

    return render(request,'stores/admin.html',{'total_books':total_books,'filtered_book':filtered_book,'orders':orders})

def orders_view(request, book_id):
    order = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            new_order = Order(
                name=form.cleaned_data['name'],
                city=form.cleaned_data['city'],
                address=form.cleaned_data['address'],
                email=form.cleaned_data['email'],
                telephone=form.cleaned_data['telephone'],
                post_code=form.cleaned_data['post_code'],
                book_title = order.title,
                book_price = order.price
            )
            new_order.save()
            return redirect('/')
        return render(request, 'stores/order.html', {"book": order, 'is_authenticated': True})
    else:
        form = CheckoutForm()
    return render(request, 'stores/order.html', {"book": order, 'form': form})

def order_action_view(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'stores/order_detail.html',{'order':order})

def order_delete_view(request,order_id):
    obj = Order.objects.get(pk=order_id)
    obj.delete()
    return redirect('/admin_local')

#==================================================================================================================================================================================

def stores_view(request):   
    return render(request, 'stores/stores.html', {'stores': stores})
def suggestions(request):
    return render(request,'stores/suggestions.html')
def policies(request):
    return render(request,'stores/policies.html')
def articles(request):
    return render(request,'stores/articles.html')

