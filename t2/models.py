from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

from .constants import (ADVERTISEMENT_TYPE_CHOICES, #ADVERTISEMENT_SUB_TYPE_CHOICES, 
                          BUILDING_TYPE_CHOICES, ADVERTISEMENT_VIP_TYPE_CHOICES, 
                          ADMIN_CONFIRMATION_STATUS_CHOICES, ADVERTISEMENT_VIP_TYPE_CHOICES,
                          USER_TYPE_CHOICES,)

# Create your models here.

class BaseModel(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class City(BaseModel):
    name = models.CharField("City", max_length=255)
    
    def __str__(self):
        return self.name
    
class Region(models.Model):
    name = models.CharField("Region", max_length=255)
    #city_id_for_rel = models.BigIntegerField(choices='', null=True, blank=True)
        
    def __str__(self):
        return self.name

class Township(models.Model):
    name = models.CharField("Township", max_length=255)
    #rel_region = models.ForeignKey("Township", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name



class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    company_name = models.CharField("company", max_length=255,null=True,blank=True)
    person_in_charge = models.CharField("person_in_charge",max_length=255)
    phone_number = models.CharField("phone_number", max_length=255,unique=True)
    user_type = models.BigIntegerField(choices=USER_TYPE_CHOICES,default=4)
    role = models.TextField("role",null=True,blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Advertisements(BaseModel):
    
    room_count = models.BigIntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                               help_text='Sahə, m² ilə göstərilmişdir')
    area_of_land = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                       help_text='Torpaq sahəsi, sot ilə göstərilmişdir')
    #
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
    
    #what is sub type
    #sub_type = models.BigIntegerField(choices=?)

    have_government_deed = models.BooleanField(blank=True, null=True)
    have_mortgage_support = models.BooleanField(blank=True, null=True)
    building_stage_height = models.BigIntegerField(blank=True, null=True)
    stage = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    #view_count = models.BigIntegerField()
    view_count = models.BigIntegerField(blank=True,null=True)
    #advertisement_create_date = models.DateTimeField(blank=True, null=True)
    
    advertisement_create_date = models.DateTimeField(blank=True, null=True)
    advertisement_expire_date = models.DateTimeField(blank=True, null=True)
    advertisement_deleted_date = models.DateTimeField(blank=True, null=True)
    
    address = models.TextField(blank=True, null=True)
    building_type = models.BigIntegerField(choices=BUILDING_TYPE_CHOICES)
    admin_confirmation_status = models.BigIntegerField(blank=True, null=True, 
                                                       choices=ADMIN_CONFIRMATION_STATUS_CHOICES)
    
    advertisement_type = models.BigIntegerField(choices=ADVERTISEMENT_VIP_TYPE_CHOICES)
    #office_building_type = models.CharField(max_length=255)
    
    #user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    #city = models.ForeignKey('City', on_delete=models.CASCADE)
    #town_ship = models.ForeignKey('Township', on_delete=models.CASCADE)
    #repair = models.BooleanField(blank=True, null=True)


    def __str__(self):
        return self.name
    
#1)I think cost value can be divide into 2 parts as general_price and price_per_unit,
#look at full_cost and cost_per_unit fields

#2)If you ll give these long and lat coordinates to front in map, decimal_places option must
#be minimum 14, and max_digit must increase also, look at location_width and 
#location_height fields


#3)I must change options view_count field into blank=True, null=True. Because the data which
#we got by scraping process is fake.
#Look at view_count field

#)I added a field which called name, to show object in admin, look at name field

