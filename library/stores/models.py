from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
# Create your models here.
from django.shortcuts import get_object_or_404
from django.utils import timezone




class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
class Genre(models.Model):
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    CHILDREN = 'Children'

    CATEGORY_CHOICES = [
        (FICTION, 'Fiction'),
        (NON_FICTION, 'Non-Fiction'),
        (CHILDREN, 'Children'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')

    def __str__(self):
        return self.name

class Subscribers(models.Model):
    name  = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.name 
    
class MailFirst(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=2000)




class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.CharField(max_length=2000,null=True, blank=True ,default='This author has no biography :)')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Define the URL pattern for an author detail view
        return reverse('author-detail', [str(self.pk)])


class Store(models.Model):
    City  = models.CharField(max_length=30)
    contact = models.CharField(null=True,max_length=20)
    address = models.CharField(max_length=50,null=False)

    def __str__(self):
        return f' {self.City} , {self.address}'

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=350, null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.pk)])
    

class Order(models.Model):
    CITY_CHOICES = (
    ('1', 'Lahore'),
    ('2', 'Islamabad'),
    ('3', 'Karachi'),
    ('4', 'Multan'),
    ('5', 'Quetta'),
    ('6', 'Peshawar'),
    ('7', 'Hyderabad'),
    )

    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100,choices=CITY_CHOICES)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    post_code = models.CharField(max_length=10)
    book_title = models.CharField(max_length=100,default='Cannot find!')
    book_price = models.CharField(max_length=100,default='0')
    date  = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'Order by {self.name} ,from {self.city}' 









total_books = Book.objects.all().count()
stores = Store.objects.all()