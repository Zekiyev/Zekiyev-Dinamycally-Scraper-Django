from django.contrib import admin
from .models import Advertisements, City, Region, Township
# Register your models here.

admin.site.register([Advertisements, City, Region, Township ])