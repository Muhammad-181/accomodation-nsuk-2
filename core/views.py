from django.shortcuts import render
from store.models import Property
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.filters import PropertyFilter


# Create your views here.



def frontpage(request):
    properties_list = Property.objects.exclude(status=Property.DELETED)
    property_filter = PropertyFilter(request.GET, queryset=properties_list)
 
    paginator = Paginator(properties_list, 5) 
    page = request.GET.get('page')
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        'properties': properties,
        'filter': property_filter
    }

    return render(request, 'core/frontpage.html', context)


def filter_results(request):
    properties_list = Property.objects.exclude(status=Property.DELETED)
    property_filter = PropertyFilter(request.GET, queryset=properties_list)

    context = {
        'property_filter': property_filter,
    }
    return render(request, 'core/filter_results.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact_us(request):
    return render(request, 'core/contact_us.html')