from django.db import models
from django.contrib.auth.models import AbstractUser
#from manufacturer.models import Manufacturer
from datetime import timedelta


# Create your models here.
class Client(AbstractUser):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    profile_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True, null=False)
    password1 = models.TextField(max_length=255, blank=False, default='')
    password2 = models.TextField(max_length=255, blank=False, default='')
    address = models.CharField(max_length=255, null=True)
    postalCode = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='client-images/', blank=True, null=True)
    username = None
    
    USERNAME_FIELD = 'email'
    '''
    REQUIRED_FIELDS = [
        'first_name',
        'email',
    ]
    '''
    class Meta:
        ordering = ('-created',)
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='client_user_set',  # Unique related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='client_user_permissions_set',  # Unique related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    

    def __str__(self):
        return self.first_name


OFFER_TYPE_CHOICES = (
    ('Classic', 'Classic'),
    ('Modern', 'Modern'),
    ('Different', 'Different'),
)

class Request(models.Model):
    title = models.CharField(max_length=200, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='request-images/', blank=True)
    image2 = models.ImageField(upload_to='request-images/', blank=True)
    image3 = models.ImageField(upload_to='request-images/', blank=True)
    image4 = models.ImageField(upload_to='request-images/', blank=True)
    image5 = models.ImageField(upload_to='request-images/', blank=True)
    file1 = models.FileField(upload_to='client-documents/', blank=True, null=True)
    file2 = models.FileField(upload_to='client-documents/', blank=True, null=True)
    file3 = models.FileField(upload_to='client-documents/', blank=True, null=True)
    material = models.CharField(max_length=200)
    offer_type = models.CharField(choices=OFFER_TYPE_CHOICES, max_length=20, default='Classic')
    description = models.CharField(max_length=2000, null=False, blank=False)
    urgent = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    mailbox_send = models.BooleanField(default=False)
    relaypoint_send = models.BooleanField(default=False)
    deadline = models.IntegerField(null=True, blank=True)
    #accepted_manufacturer= models.OneToOneField(Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    accepted_manufacturer_id= models.IntegerField(null=True, blank=True)
    completed_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    completed_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def get_accepted_manufacturer(self, accepted_manufacturer_id):
        from manufacturer.models import Manufacturer
        try:
            return Manufacturer.objects.get(id=accepted_manufacturer_id)
        except Manufacturer.DoesNotExist:
            return None
        
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
    
class Request2(models.Model):
    title = models.CharField(max_length=200, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='request-images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='request-images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='request-images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='request-images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='request-images/', blank=True, null=True)
    file1 = models.FileField(upload_to='client-documents/', blank=True, null=True)
    file2 = models.FileField(upload_to='client-documents/', blank=True, null=True)
    file3 = models.FileField(upload_to='client-documents/', blank=True, null=True)
    material = models.CharField(max_length=200)
    offer_type = models.CharField(choices=OFFER_TYPE_CHOICES, max_length=20, default='Classic')
    description = models.CharField(max_length=2000, null=False, blank=False)
    urgent = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    mailbox_send = models.BooleanField(default=False)
    relaypoint_send = models.BooleanField(default=False)
    deadline = models.IntegerField(null=True, blank=True)
    #accepted_manufacturer= models.OneToOneField(Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    accepted_manufacturer_id= models.IntegerField(null=True, blank=True)
    completed_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    completed_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def get_accepted_manufacturer(self, accepted_manufacturer_id):
        from manufacturer.models import Manufacturer
        try:
            return Manufacturer.objects.get(id=accepted_manufacturer_id)
        except Manufacturer.DoesNotExist:
            return None
        
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
    


RATING_CHOICES = (
    ('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),
)


class Rating(models.Model):
    rating_value = models.CharField(choices=RATING_CHOICES, max_length=1, default='5',blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    #manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    manufacturer_id= models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    def get_manufacturer(self, manufacturer_id):
        from manufacturer.models import Manufacturer
        try:
            return Manufacturer.objects.get(id=manufacturer_id)
        except Manufacturer.DoesNotExist:
            return None

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.rating_value
    

class News(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    image = models.ImageField(upload_to='news-images/', blank=True, null=True)
    tags = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    article = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title