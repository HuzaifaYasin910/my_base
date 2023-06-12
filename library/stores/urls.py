from django.urls import path
from .views import *

app_name = 'stores'

urlpatterns = [
    path('home/',search,name='home'),
    path('authors/',author,name='author'),
    path('author/<int:author_pk>/', author_detail, name='author-detail'),
    path('book_detail/<int:book_id>/',book_detail,name='book_detail'),
    path('genre/', genres, name='genre'),
    path('stores/', stores_view, name='stores'),
    path('books/<int:genre_id>/', books, name='books'),
    path('admin_local/', admin_local, name='admin_local'),
    path('articles/', articles, name='articles'),
    path('children_genres/', children_genres, name='children_genres'),
    path('suggestions/', suggestions, name='suggestions'),
    path('policies/', policies, name='policies'),
    path('orders/<int:book_id>/', orders_view, name='orders'),
    path('order_action/<int:order_id>',order_action_view,name='order_action'),
    path('order_delete/<int:order_id>',order_delete_view,name='order_delete')

]