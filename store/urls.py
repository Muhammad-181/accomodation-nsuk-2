from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import frontpage
from .import views




urlpatterns = [
    path('', frontpage, name='frontpage'),
    # path('search/', views.search, name='search-url'),
    path('<slug:slug>/', views.instituition_detail, name='instituition_detail-page'),
    path('<slug:instituition_slug>/<str:id>/', views.property_detail, name='property_deatil-page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
