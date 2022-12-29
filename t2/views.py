from django.shortcuts import render
from django.http import JsonResponse
from .utils import (test_parce_conditions, scrape_base_data, scrape_land_area, scrape_area,
                    scrape_room_count, generate_url_list, scrape_cost, deleted_or_old_list_id,
                    problem_list_id, get_id, get_coordinates)
from .models import *

# Create your views here.


def upload_advertisements(request):
    url_list = generate_url_list(3159424,3159440)
    temp_data = []
    #print(len(url_list),'secilmis')
    for i in url_list:
        answer = test_parce_conditions(i)
        if answer !=0:
            deleted_or_old_list_id.append(i)
            continue
        else:
            temp_data.append(Advertisements(
                room_count=scrape_room_count(i) if scrape_room_count(i)!=0 else None,
                area=scrape_area(i) if scrape_area(i)!=0 else None,
                area_of_land=scrape_land_area(i) if scrape_land_area(i)!=0 else None,
                name=get_id(i),
                full_cost=scrape_cost(i)['full_price'] if 1<=len(scrape_cost(i))<=2 else None,
                cost_per_unit=scrape_cost(i)['unit_price'] if len(scrape_cost(i))==2 else None, 
                #coast=scrape_cost(i),
                location_width=get_coordinates(i)['Latitude'] if len(get_coordinates(i))==2 else None,
                location_height=get_coordinates(i)['Longitude'] if len(get_coordinates(i))==2 else None,
                ))
            #print(temp_data)
    Advertisements.objects.bulk_create(temp_data,batch_size=1000)
    print(temp_data)
    return JsonResponse({'status':200})