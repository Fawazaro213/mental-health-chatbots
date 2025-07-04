from django.shortcuts import render
from .models import MentalHealthResource, ResourceCategory
import json
import os
from django.conf import settings

def resources_page(request):
    categories = ResourceCategory.objects.prefetch_related('mentalhealthresource_set')
    return render(request, "resources/resources.html", {"categories": categories})

def emergency_contacts(request):
    json_path = os.path.join(settings.BASE_DIR, "resources", "contacts.json")
    with open(json_path, "r", encoding="utf-8") as f:
        contacts = json.load(f)
    return render(request, "resources/emergency.html", {"contacts": contacts})