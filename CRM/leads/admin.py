from django.contrib import admin
from leads.models import Lead, Agent, User, UserProfile, Category
# Register your models here.
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(UserProfile)
admin.site.register(Category)



