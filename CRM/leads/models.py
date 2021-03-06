from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.
 
class User(AbstractUser):
    is_organizer = models.BooleanField(default = True)
    is_agent = models.BooleanField(default = False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default= 0)
    organization = models.ForeignKey(UserProfile, null = True, on_delete = models.CASCADE)
    agent = models.ForeignKey("Agent", blank = True, null= True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name = "leads", blank = True, null= True,on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):  #new, contacted, converted, unconverted(types of category)
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.email

def create_userprofile(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

    
post_save.connect(create_userprofile, sender = User)







