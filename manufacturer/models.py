from django.db import models
from django.contrib.auth.models import AbstractUser
from client.models import Request2, Client


# Create your models here.
class Manufacturer(AbstractUser):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=255, unique=True, null=False)
    password1 = models.TextField(max_length=255, default='', blank=False)
    password2 = models.TextField(max_length=255, default='', blank=False)
    city = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)
    postalCode = models.CharField(max_length=255, null=True)
    idNumber = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    profile_name = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='manuf-images/', blank=True, null=True)

    username = None
    
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('-created',)
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='manufacturer_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='manufacturer_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.first_name
    

class Offer(models.Model):
    request = models.ForeignKey(Request2, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    price = models.IntegerField(null=False, blank=False)
    days = models.IntegerField(null=False, blank=False)
    description = models.CharField( max_length=2000, null=False, blank=False)
    accepted_status = models.BooleanField(default=False)
    accepted_by_client = models.OneToOneField(Client, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    expired = models.BooleanField(default=False)#on expiry, set active to false

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.manufacturer.first_name


RATING_CHOICES = (
    ('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),
)


class Rating(models.Model):
    rating_value = models.CharField(choices=RATING_CHOICES, max_length=1, default='5',blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    client_id = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.rating_value