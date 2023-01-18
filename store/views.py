from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Property, Instituition, Image
from .forms import PropertyForm
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.



def property_detail(request, instituition_slug, id):
    property = get_object_or_404(Property, id=id)
    images = Image.objects.filter(property=property)
    site = get_current_site(request)
    current_path = request.path
    Wmessage = "Check out this website:"+site.domain


    context = {
        'property': property,
        'images': images,
        'Wmessage': Wmessage,
        'current_path': current_path,
    }
    return render(request, 'store/property_detail.html', context)


def instituition_detail(request, slug):
    instituition = get_object_or_404(Instituition, slug=slug)
    properties = instituition.properties.exclude(status=Property.DELETED)


    context = {
        
    }

    return render(request, 'store/instituition_detail.html', context)



# def search(request):
#     query = request.GET.get('query', '')
#     properties = Property.objects.filter(
#         Q(title__icontains=query) |
#         Q(price__iexact=query) |
#         Q(location__contains=query) |
#         Q(description__icontains=query)
#     )

#     context = {
#         'query': query,
#         'properties': properties
#     }
#     return render(request, 'store/search_results.html', context)

