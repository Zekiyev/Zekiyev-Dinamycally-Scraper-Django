from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests


from .utils import (test_parce_conditions, scrape_base_data, scrape_land_area, scrape_area,
                    scrape_room_count, generate_url_list, scrape_cost, deleted_or_old_list_id,
                    problem_list_id, get_id, get_latitude, get_longitude, get_building_type,
                    scrape_announcement_category, get_have_govern_deed, get_mortgage_support, 
                    get_stage_datas, scrape_description, scrape_pub_date, get_adress_text, 
                    get_city_region_township_names,
                    )

from .models import Advertisements, City, Region, Township

# Create your views here.

def upload_cities(request):
    responce = JsonResponse({'status':400})
    answer = get_city_region_township_names()[0]
    if answer != {}:
        city_list = answer['city']
        
        for city in city_list:
            City.objects.get_or_create(name=city)
        responce = JsonResponse({'status':200})
    
    return responce


def upload_regions(request):
    
    responce = JsonResponse({'status':400})
    answer_region = get_city_region_township_names()
    if answer_region[1] != {}:

        for region in answer_region[1]['region'][1]:
            parent=City.objects.get(name=answer_region[1]['region'][0])
            #parent = City.objects.filter(name=region)
            Region.objects.get_or_create(name=region,
                                         city_for_rel=parent)
        
        responce = JsonResponse({'status':200})
        
    return responce
        

def upload_township(request):

    responce = JsonResponse({'status':400})
    answer_township = get_city_region_township_names()
    
    
    if answer_township[2] != {}:
        try:
            for township in answer_township[2]['township'][1]:
                parent = Region.objects.get(name=answer_township[2]['township'][0])
                Township.objects.get_or_create(name=township,
                                            region_for_rel=parent),
                
            responce = JsonResponse({'status':200})
        except KeyError:
            responce = JsonResponse({'status':'KeyError'})
    return responce



def upload_advertisements(request):
    url_list = generate_url_list(3159424,3159440)
    temp_advertisement = []
    print(len(url_list),'secilmis')
    for i in url_list:
        page = requests.get(i)
        soup = BeautifulSoup(page.content,features='html.parser')

        answer = test_parce_conditions(soup, i)
        if answer != 'OK':
            deleted_or_old_list_id.append(i)
            continue
        
        else:
            temp_advertisement.append(Advertisements(
                room_count=scrape_room_count(soup, i),
                area=scrape_area(soup, i),
                area_of_land=scrape_land_area(soup, i),
                name=get_id(i),
                full_cost=scrape_cost(soup, i)['full_price'],
                cost_per_unit=scrape_cost(soup, i)['unit_price'], 
                #coast=scrape_cost(i),
                
                location_width=get_latitude(soup, i) if 
                type(get_latitude(soup, i))==float else 0,
                
                location_height=get_longitude(soup, i) if 
                type(get_longitude(soup, i))==float else 0,
                
                type=scrape_announcement_category(soup, i) if 
                type(scrape_announcement_category(soup, i))==int else 0,
                #sub_type=?
                
                have_government_deed=get_have_govern_deed(soup, i) if 
                type(get_have_govern_deed(soup, i))==bool else None,
                
                have_mortgage_support=get_mortgage_support(soup, i) if 
                type(get_mortgage_support(soup, i))==bool else None,
                
                building_stage_height=get_stage_datas(soup, i)[1],
                stage=get_stage_datas(soup, i)[0],
                
                description=scrape_description(soup, i) if 
                type(scrape_description(soup, i))==str else None,
                
                view_count=None,
                
                advertisement_create_date=scrape_pub_date(soup, i) if 
                type(scrape_pub_date(soup, i))!=list else None,
                
                advertisement_expire_date=None,
                advertisement_deleted_date=None,
                
                address=get_adress_text(soup, i) if 
                type(get_adress_text(soup, i))==str else None,
                
                building_type=get_building_type(soup, i),
                admin_confirmation_status=1,
                advertisement_type=1,                  
                
                ))
            print(temp_advertisement)
    Advertisements.objects.bulk_create(temp_advertisement,batch_size=1000)
    print(temp_advertisement)
    return JsonResponse({'status':200})

#you can add '##BUG##' in else case in fields with type charfield