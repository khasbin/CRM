from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.
 
class User(AbstractUser):
    is_organizer = models.BooleanField(default = True)
    is_agent = models.BooleanField(default = False)

class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default= 0)
    organization = models.ForeignKey(UserProfileModel, on_delete = models.CASCADE)
    agent = models.ForeignKey("Agent", blank = True, null= True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    organization = models.ForeignKey(UserProfileModel, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.email

def create_userprofile_model(sender,instance,created, **kwargs):
    if created:
        UserProfileModel.objects.create(user = instance)
    

post_save.connect(create_userprofile_model, sender = User)






