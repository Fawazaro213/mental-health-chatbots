from django.contrib import admin
from .models import MentalHealthResource, ResourceCategory

admin.site.register(ResourceCategory)
admin.site.register(MentalHealthResource)