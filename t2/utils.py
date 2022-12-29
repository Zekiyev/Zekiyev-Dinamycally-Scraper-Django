from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date,datetime
import timedelta
from bs4 import BeautifulSoup
import requests

problem_list_id = []
deleted_or_old_list_id = []

#----------------------------------------------------------------------------------------------

def test_parce_conditions(url):
    
    #This function helps us to determine that data is or not apropriate for scraping
    #The function accept a str which is determine full url of  the page, the function returns int type
    #If it returns 0, it says that we can continue scraping operation, else we have to skip scraping
    #operations
    
    #0 - It means, everything is ok and we can scrape
    
    ending = url[22:]
    result = 0
    
    #loading html content of image
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features='html.parser')
    
    #searching data in tags with specific attributes
    
    test_h1 = soup.find_all('h1')
    test_p = soup.find_all('p',attrs={'class':'flash'})

    #testing parce conditions
    if len(test_h1) == 1 and str(test_h1)[:19] == "[<h1>Tapılmadı</h1>":
        result = [ending, "##BUG##", "Bu elan tapılmadı"]
        deleted_or_old_list_id.append(result)
        
    elif len(test_p) == 1 and str(test_p)[:55] == '[<p class="flash" id="alert">Bu elanın müddəti başa çat':
        result = [ending, "##BUG##", "Bu elanın vaxtı bitmiş və ya silinmişdir"]
        deleted_or_old_list_id.append(result)
        
    return result

#----------------------------------------------------------------------------------------------

def scrape_base_data(url):
    
    #This function helps us to get all highlighted key and values, and it can be used as 
    #additional categories .
    #The function accept a str which is determine full url of the page .
    #The function returns dict type either it goes normally, or wrongly
    
    my_list = []
    result = {}
    ending = url[22:]
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features='html.parser')
    tables = soup.find_all('table',attrs = {'class':'parameters'})
    
    if tables != []:
        for table in tables:
            for tr in table.find_all('tr'):
                x = str(tr).replace('<tr>','').replace('</tr>','\n')

                #seperating str into 2 parts by '---' char, first will be key, 
                #second will be value and convert data into list

                y = x.replace('<td>','').replace('</td>','---')[:-4].split('---')
                my_list.append(y)
                result.update({y[0]:y[1]})
    else:
        result = [ending, "##BUG##", "class=parameters atributlu table tegi tapılmadı"]
            
    return result

#----------------------------------------------------------------------------------------------

def scrape_land_area(url):
    
    #This function helps us to get value of land's area which values have been showed in 'sot'
    #It returns float normally,  None if there is not any data, and 0 if there are any problem
    
    my_dict = scrape_base_data(url)
    result = 0
    
    if type(my_dict)==dict:
        
        my_list = [i for i in my_dict.values() if i.endswith('sot')]

        if len(my_list)>0:
            result = float(my_list[0].replace('sot','').replace(' ',''))
        else:
            result = None
            
    return result

#----------------------------------------------------------------------------------------------

def scrape_area(url):
    
    #This function helps us to get value of building's area which values have been showed in 'm²'
    #It returns float normally, None if there is not any data, and zero if there are any problem
    
    my_dict = scrape_base_data(url)
    result = 0
    
    if type(my_dict)==dict:
        my_list = [i for i in my_dict.values() if i.endswith('m²')]
        
        if len(my_list) > 0:
            result = float(my_list[0].replace('m²','').replace(' ',''))
        else:
            result = None
    return result

#----------------------------------------------------------------------------------------------

def scrape_room_count(url):
    
    #This function helps us to get value of room_count
    #It returns integer normally, None if there is not any data, and zero if there are any problems
    
    result = 0
    my_dict = scrape_base_data(url)
    
    if type(my_dict)==dict:
        if 'Otaq sayı' in my_dict.keys():
            result = int(my_dict['Otaq sayı'])
        else:
            result = None
            
    return result

#----------------------------------------------------------------------------------------------

def generate_url_list(start, ending):
    
    #It help us to generate url list for looping parce process
    #Note: start<ending ant type are int
    
    num_list = list(range(start,ending))
    url_list = []
        
    for i in num_list:
        url_list.append("https://bina.az/items/" + str(i))
        
    result = []
    
    for i in url_list:
        if test_parce_conditions(i)!=0:
            continue
        else:
            result.append(i)
    
    return result

#----------------------------------------------------------------------------------------------

def get_id(url):
    
    ending = url[22:]
   
    return ending

#----------------------------------------------------------------------------------------------

def scrape_cost(url):
    
    #This function get cost data of item
    #It returns dict usual in every case
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features='html.parser')
    ending = url[22:]
    cost_dict = {}
    result= [ ending,
            "##BUG##",
            "Cost_front_class_error - May be there are some unpredictable bugs" ]

    div = soup.find('div',attrs={'class','price_header'})
    
    if div != None:

        if div.section['class']==['price']:
            cost = div.section.p.text.replace(' ','')
            sep_index = cost.index('AZN')
            numeric_cost = cost[:sep_index]
            cost_dict['full_price'] = float(numeric_cost)
            result = cost_dict
            

        elif div.section['class']==['price', 'compound']:
            cost = div.section.p.text.replace(' ','')
            unit_price = div.section.div.text.replace(' ','')
            sep_index_cost = cost.index('AZN')
            sep_index_unit = unit_price.index('AZN')
            numeric_cost = cost[:sep_index_cost]
            numeric_unit_price = unit_price[:sep_index_unit]
            cost_dict['full_price'] = float(numeric_cost)
            cost_dict['unit_price'] = float(numeric_unit_price)
            result = cost_dict
            
    problem_list_id.append(result)

    return result

#----------------------------------------------------------------------------------------------

def get_latitude(url):
    
    #This function get value of latitude coordinate, if everything ok, it returns float
    #Else error in list type
 
    ending = url[22:]
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features='html.parser')
    coordinates = soup.find('div',attrs = {'id':'item_map'})
    
    if coordinates != None:
        
        try:
            result = float(coordinates['data-lat'])
            
        except KeyError:
            result = [ending, "##BUG##", "Coordinates_error-There are may be some unpredictable bugs"]
            problem_list_id.append(result)
    else:
        result = [ending, "##BUG##", "Coordinates_error-There are may be some unpredictable bugs"]
        problem_list_id.append(result)
    
    return result

#----------------------------------------------------------------------------------------------

def get_longitude(url):
    
    #This function get value of longitude coordinate, if everything ok, it returns float
    #Else error in list type
    
    ending = url[22:]
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features='html.parser')
    coordinates = soup.find('div',attrs = {'id':'item_map'})
    
    if coordinates != None:
        
        try:
            result = float(coordinates['data-lng'])
            
        except KeyError:
            result = [ending, "##BUG##", "Coordinates_error-There are may be some unpredictable bugs"]
            problem_list_id.append(result)
    else:
        result = [ending, "##BUG##", "Coordinates_error-There are may be some unpredictable bugs"]
        problem_list_id.append(result)
    
    return result

#----------------------------------------------------------------------------------------------

def scrape_announcement_category(url):
    
    #This function helps us to determine type of announcement  about For sale, for rent montly or 
    #for rent daily
    #The function accept a str which is determine full url of  the page
    #If everything is ok the function returns str, else list
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features='html.parser')
    ending = url[22:]
    category = []
    result = []
    
    try:
        h3 = soup.find('h3',attrs={'class':'type'})
        
        try:
            category = h3.find('a').text
            if category == 'Satış':
                result = 3
                
            #There are may be 2 type of rent categories, daily rent and monthly rent, both of them startswith
            #the 'Kirayə', so we must to seperate it from each other
            
            elif category == 'Kirayə':
                span = soup.find('span', attrs={'class':'price-per'})

                if span.text =='/gün':
                    #category = 'Kirayə - Günlük'
                    result = 2
                elif span.text =='/ay':
                    #category = 'Kirayə - Aylıq'
                    result = 1
                else:                
                    result = [ending, "##BUG##",
                                        """Category_Problem, (Satış, Kirayə - Günlük, Kirayə - Aylıq)
                                        Elan tipi solda sadalanan 3 ündən biri olmaldır""" ]
                    problem_list_id.append(result)

        except AttributeError:
            result = [ending, "##BUG##", """AttributeError, Parent tegi class='type' h3 
                                            tegi olan a tegi tapılmadı"""]      
            problem_list_id.append(result)
            
    except AttributeError:
        result = [ending, "##BUG##", "AttributeError, class=type olan h3 teg-i tapılmadı"]
        problem_list_id.append(result)

    return result

#----------------------------------------------------------------------------------------------

def get_sub_type_adv(url):
    
    #This function helps us to appoint type of building or item
    
    sub_type = scrape_base_data(url)
    ending = url[22:]
    result = [ending, '##BUG##', 'There some unpredictable bugs']
    
    if 'Kateqoriya' in sub_type.keys():
        
        #By variable named result_dict we want to adapt our data into
        #ADVERTISEMENT_SUB_TYPE_CHOICES, because class_field accept integer data
        result_dict = {'Köhnə tikili': 1,
                        'Yeni tikili': 2,
                        'Ev / Villa': 3,
                        'Bağ': 4,
                        'Ofis': 5,
                        'Qaraj': 6,
                        'Obyekt': 7,
                        'Torpaq': 8}
        
        element = sub_type['Kateqoriya']
        result = result_dict[element]
        
    return result

#----------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------
