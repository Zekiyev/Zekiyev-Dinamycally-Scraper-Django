from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests

from .utils import (test_parce_conditions, scrape_base_data, scrape_land_area, scrape_area,
                    scrape_room_count, generate_url_list, scrape_cost, deleted_or_old_list_id,
                    problem_list_id, get_id, get_latitude, get_longitude, get_building_type,
                    scrape_announcement_category, get_have_govern_deed, get_mortgage_support, 
                    get_stage_datas, scrape_description, scrape_pub_date, get_adress_text, 
                    )

from .models import Advertisements

# Create your views here.


def upload_advertisements(request):
    url_list = generate_url_list(3159424,3159440)
    temp_advertisement = []
    print(len(url_list),'secilmis')
    for i in url_list:
        page = requests.get(i)
        soup = BeautifulSoup(page.content,features='html.parser')

        answer = test_parce_conditions(soup, i)
        if answer !=0:
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
                type(scrape_announcement_category(soup, i))==int else 10,
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
                type(scrape_pub_date(soup, i))==str else None,
                
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