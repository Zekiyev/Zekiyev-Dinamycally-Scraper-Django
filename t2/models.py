from django.db import models
import uuid

# Create your models here.

class BaseModel(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True



class Advertisements(BaseModel):
    room_count = models.BigIntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area_of_land = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    name = models.CharField(max_length=50)
    #coast = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    full_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, 
                                    null=True, help_text='AZN')
    
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, 
                                        null=True, help_text='AZN/m²')
    
    location_width = models.DecimalField(max_digits=10, decimal_places=7, blank=True, 
                                        null=True, help_text='Longitude')
    
    location_height = models.DecimalField(max_digits=10, decimal_places=7, blank=True, 
                                          null=True, help_text='Latitude')

    def __str__(self):
        return self.name
    