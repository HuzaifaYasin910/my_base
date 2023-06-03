from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(Subscribers)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Store)
admin.site.register(Language)
admin.site.register(MailFirst)
