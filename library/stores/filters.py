from django.db.models import Q
from stores import django_filters
from .models import *

class BookFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method='filter_search_query')

    class Meta:
        model = Book
        fields = []

    def filter_search_query(self, queryset, search_query, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(isbn__icontains=value) |
            Q(price__icontains=value)
        )
