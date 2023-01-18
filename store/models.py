from django.db import models
import uuid
# from django.contrib.auth.models import User
from profiles.models import User


# Create your models here.


class Instituition(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

   
    
    def __str__(self):
        return self.title



class Property(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'
    SELFCONTAIN = 0
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = '5+'

    STATUS_CHOICES = (
        (DRAFT, 'draft'),
        (WAITING_APPROVAL, 'watingapproval'),
        (ACTIVE, 'active'),
        (DELETED, 'deleted'),
    )

    BATH_CHIOCES = (
        (SELFCONTAIN, 0),
        (ONE, 1),
        (TWO, 2),
        (THREE, 3),
        (FOUR, 4),
        (FIVE, '5+'),

    )
    BED_CHIOCES = (
        (ZERO, 0),
        (ONE, 1),
        (TWO, 2),
        (THREE, 3),
        (FOUR, 4),
        (FIVE, '5+'),

    )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        editable=False, unique=True)
    instituition = models.ForeignKey(Instituition, related_name='properties', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    bathroom = models.IntegerField(choices=BATH_CHIOCES, null=True)
    bedroom = models.IntegerField(choices=BED_CHIOCES, null=True)
    building_size_in_SQFT = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    thumbnail = models.ImageField(upload_to='uploads/product_thumbnails', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)


    class Meta:
        ordering = ('-updated_at',)
        verbose_name_plural = 'Properties'
    
    def __str__(self):
        return self.title
    
    def get_display_price(self):
        return self.price / 100


class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='uploads/product_images')

    def __str__(self) -> str:
        return self.property.title