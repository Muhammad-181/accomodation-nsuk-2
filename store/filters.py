import decimal
from django_filters import FilterSet, NumberFilter, CharFilter
from django.forms import ModelChoiceField, ChoiceField
from django import forms
from django.db.models import Max
from .models import Property


class PriceRangeFilter(NumberFilter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = map(decimal.Decimal,str(value).split(','))
            return qs.filter(price__gte=min_price, price__lte=max_price)
        return qs


# class PropertyFilter(FilterSet):
#     price_range = PriceRangeFilter(field_name='price', lookup_expr='range')
#     location = CharFilter(field_name='location', lookup_expr='icontains')
#     bedroom = NumberFilter(field_name='bedroom', lookup_expr='exact')
#     bathroom = NumberFilter(field_name='bathroom', lookup_expr='exact')
#     class Meta:
#         model = Property
#         fields = ['price_range', 'bathroom', 'bedroom', 'location']


class PropertyFilter(FilterSet):
    price_range = NumberFilter(field_name='price', lookup_expr='range')
    location = ModelChoiceField(queryset=Property.objects.values_list('location', flat=True).distinct(), empty_label="All", widget=forms.Select)
    bedroom = ChoiceField(choices=[(i, i) for i in range(1, Property.objects.all().aggregate(Max('bedroom'))['bedroom__max']+1)], widget=forms.Select)
    bathroom = ChoiceField(choices=[(i, i) for i in range(1, Property.objects.all().aggregate(Max('bathroom'))['bathroom__max']+1)], widget=forms.Select)
    class Meta:
        model = Property
        fields = ['price_range', 'bedroom', 'location', 'bathroom']
