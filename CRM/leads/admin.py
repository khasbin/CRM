from django.contrib import admin
from leads.models import Lead, Agent, User
# Register your models here.
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Lead)



