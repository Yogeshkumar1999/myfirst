from .models import *
import django_filters
from django_filters import DateFilter, CharFilter

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name = "date_created", lookup_expr = "gte")
    end_date = DateFilter(field_name = "date_created", lookup_expr = "lte")
    #note = CharFilter(filed_name = 'note', lookup_expr='icontaines')###icontainer for case sensitivity
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fileds = '__all__'
        exclude = ['date_created', 'tags', 'description']
