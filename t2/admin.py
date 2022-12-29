from django.contrib import admin
from .models import Advertisements, City
# Register your models here.

admin.site.register([Advertisements, City])