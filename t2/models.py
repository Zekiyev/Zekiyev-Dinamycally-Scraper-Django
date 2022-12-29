from django.db import models
import uuid

from .assignments import (ADVERTISEMENT_TYPE_CHOICES, ADVERTISEMENT_SUB_TYPE_CHOICES, 
                          BUILDING_TYPE_CHOICES, ADVERTISEMENT_VIP_TYPE_CHOICES, 
                          )

# Create your models here.

class BaseModel(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True



class Advertisements(BaseModel):
    room_count = models.BigIntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                               help_text='Sahə, m² ilə göstərilmişdir')
    area_of_land = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                       help_text='Torpaq sahəsi, sot ilə göstərilmişdir')
    name = models.CharField(max_length=50, help_text='Url ending')
    #coast = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    full_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, 
                                    null=True, help_text='AZN')

    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, 
                                        null=True, help_text='AZN/m²')
    #decimal_places must be 14 minimum
    location_width = models.DecimalField(max_digits=10, decimal_places=7, blank=True, 
                                        null=True, help_text='Longitude')
    
    location_height = models.DecimalField(max_digits=10, decimal_places=7, blank=True, 
                                          null=True, help_text='Latitude')
    
    type = models.BigIntegerField(choices=ADVERTISEMENT_TYPE_CHOICES)
    sub_type = models.BigIntegerField(choices=ADVERTISEMENT_SUB_TYPE_CHOICES)
    have_government_deed = models.BooleanField(blank=True, null=True)
    have_mortgage_support = models.BooleanField(blank=True, null=True)
    building_stage_height = models.BigIntegerField(blank=True, null=True)
    stage = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    view_count = models.BigIntegerField()

    def __str__(self):
        return self.name
    