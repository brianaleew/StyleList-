from django.db import models
from django.contrib.auth.models import User 
from datetime import date 
from django.urls import reverse 

# Tuples for Apparel Model will be here
TYPES = (
    ('T', 'Top'),
    ('B', 'Bottom'),
    ('S', 'Shoe')
)

# Create your models here.

# User model (will be a subclass of the already made django user model so i can add special features?)


#Apparel Model 
class Apparel(models.Model):
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=40)
    img = models.ImageField(default='images/img-error.png')
    style = models.CharField(max_length=70, default='not specified')
    type = models.CharField(
        max_length=1,
        choices = TYPES, 
        default = TYPES[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.type} : {self.name}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'apparel_id': self.id })
    
     


# Outfit Model 
class Outfit(models.Model):
    name = models.CharField(max_length=40)
    date = models.DateField('Date Made')
    event = models.CharField(max_length=40)
    caption = models.CharField(max_length=50)

    apparels = models.ManyToManyField(Apparel)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('outfits_detail', kwargs={'outfit_id': self.id })

# this class extends the built in django User model to add extra  non auth related info 
# by creating a one to one relation (aka profile model)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=50)
    color_palette = models.CharField(max_length=50)
    top_styles = models.CharField(max_length=50)
    profile_img = models.ImageField

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'user_id': self.id })



