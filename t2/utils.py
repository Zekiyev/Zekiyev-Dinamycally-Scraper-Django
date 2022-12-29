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

def month_converter(month_val):
    
    ##This function helps us to convert month from number format into letter format
    ##The function accepts only 1 argument, which is str and it returns str also
    
    result = month_val
    
    month_dict = {
                    '01': 'January', 'Yanvar':'January',
                    '02': 'February', 'Fevral':'February',
                    '03': 'March', 'Mart':'March',
                    '04': 'April', 'Aprel':'April',
                    '05': 'May', 'May':'May',
                    '06': 'June', 'İyun':'June', 'Iyun':'June',
                    '07': 'July', 'İyun':'July', 'Iyul':'July',
                    '08': 'Auqust', 'Avqust': 'Auqust',
                    '09': 'September', 'Sentyabr':'September',
                    '10': 'Oktober', 'Oktraybr':'Oktober',
                    '11': 'November', 'Noyabr':'November',
                    '12': 'December', 'Dekabr':'December',
    }
    
    if month_val in month_dict.keys():
        result = month_dict[month_val]
        
    return result

#----------------------------------------------------------------------------------------------

def test_parce_conditions(soup, url):
    
    #This function helps us to determine that data is or not apropriate for scraping
    #The function accept a str which is determine full url of  the page, the function returns int type
    #If it returns 0, it says that we can continue scraping operation, else we have to skip scraping
    #operations
    
    #0 - It means, everything is ok and we can scrape
    
    ending = url[22:]
    result = 0
        
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

def scrape_base_data(soup, url):
    
    #This function helps us to get all highlighted key and values, and it can be used as 
    #additional categories .
    #The function accept a str which is determine full url of the page .
    #The function returns dict type either it goes normally, or wrongly
    
    my_list = []
    result = {}
    ending = url[22:]
    
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

def scrape_land_area(soup, url):
    
    #This function helps us to get value of land's area which values have been showed in 'sot'
    #It returns float normally,  None if there is not any data, and 0 if there are any problem
    
    my_dict = scrape_base_data(soup, url)
    result = 0
    ending = url[22:]
    
    if type(my_dict)==dict:
        
        my_list = [i for i in my_dict.values() if i.endswith('sot')]

        if len(my_list)>0:
            result = float(my_list[0].replace('sot','').replace(' ',''))
        else:
            result = None
            
    problem_list_id.append([ending, "##BUG##", "There are some unpredictable bugs"])
        
    return result

#----------------------------------------------------------------------------------------------

def scrape_area(soup, url):
    
    #This function helps us to get value of building's area which values have been showed in 'm²'
    #It returns float normally, None if there is not any data, and zero if there are any problem
    
    my_dict = scrape_base_data(soup, url)
    result = 0
    ending = url[22:]
    
    if type(my_dict)==dict:
        my_list = [i for i in my_dict.values() if i.endswith('m²')]
        
        if len(my_list) > 0:
            result = float(my_list[0].replace('m²','').replace(' ',''))
        else:
            result = None
            
    problem_list_id.append([ending, "##BUG##", "There are some unpredictable bugs"])
    
    return result

#----------------------------------------------------------------------------------------------

def scrape_room_count(soup, url):
    
    #This function helps us to get value of room_count
    #It returns integer normally, None if there is not any data, and zero if there are any problems
    
    result = 0
    my_dict = scrape_base_data(soup, url)
    ending = url[22:]
    
    if type(my_dict)==dict:
        if 'Otaq sayı' in my_dict.keys():
            result = int(my_dict['Otaq sayı'])
        else:
            result = None
    problem_list_id.append([ending, "##BUG##", "There are some unpredictable bugs"])
            
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
        
        page = requests.get(i)
        soup = BeautifulSoup(page.content,features='html.parser')

        if test_parce_conditions(soup, i)!=0:
            continue
        else:
            result.append(i)
    
    return result

#----------------------------------------------------------------------------------------------

def get_id(url):
    
    ending = url[22:]
   
    return ending

#----------------------------------------------------------------------------------------------

def scrape_cost(soup, url):
    
    #This function get cost data of item
    #It returns dict usual in normal, but zero in error case
    
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
            cost_dict['unit_price'] = 0
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
            
        else:
            problem_list_id.append(result)
            cost_dict = {'full_price': 0, 'unit_price': 0}
            
    else:
        problem_list_id.append(result)
        cost_dict = {'full_price': 0, 'unit_price': 0}

    return cost_dict

#----------------------------------------------------------------------------------------------

def get_latitude(soup, url):
    
    #This function get value of latitude coordinate, if everything ok, it returns float
    #Else error in list type
 
    ending = url[22:]
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

def get_longitude(soup, url):
    
    #This function get value of longitude coordinate, if everything ok, it returns float
    #Else error in list type
    
    ending = url[22:]
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

def scrape_announcement_category(soup, url):
    
    #This function helps us to determine type of announcement  about For sale,
    #for rent montly or for rent daily
    #The function accept a str which is determine full url of  the page
    #If everything is ok the function returns str, else list
    
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

def get_building_type(soup, url):
    
    #This function helps us to appoint type of building or item
    
    building_type = scrape_base_data(soup, url)
    ending = url[22:]
    error_msg = [ending, '##BUG##', 'There some unpredictable bugs']
    result = 10
    
    if 'Kateqoriya' in building_type.keys():
        
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
        
        element = building_type['Kateqoriya']
        result = result_dict[element]
    
    
    problem_list_id.append(error_msg)    
        
    return result

#----------------------------------------------------------------------------------------------
def get_have_govern_deed(soup, url):
    
    #This function helps us to appoint existence of order(kupca) of home,house
    #it return bool if everything is ok, none if there is not any data, and list if there are
    #any error
    
    my_dict = scrape_base_data(soup, url)
    answer_dict = {'var': True, 'yoxdur': False}
    ending = url[22:]
    result = [ending, "##BUG##", "There may be some unpredictable bugs"]
    
    if type(my_dict) == dict:
        
        if 'Çıxarış' in my_dict.keys():
            deed_value = my_dict['Çıxarış']
            result = answer_dict[deed_value]
            
        else:
            result = False
    else:
        problem_list_id.append(result)
        
    return result
#----------------------------------------------------------------------------------------------

def get_mortgage_support(soup, url):
    
    #This function helps us to appoint existence of order(kupca) of home,house
    #it return bool if everything is ok, none if there is not any data, and list if there are
    #any error
    
    my_dict = scrape_base_data(soup, url)
    answer_dict = {'var': True, 'yoxdur': False}
    ending = url[22:]
    result = [ending, "##BUG##", "There may be some unpredictable bugs"]
    
    if type(my_dict) == dict:
        
        if 'İpoteka' in my_dict.keys():
            mortgage_val = my_dict['İpoteka']
            result = answer_dict[mortgage_val]
            
        else:
            result = False
    else:
        problem_list_id.append(result)
            
    return result

#----------------------------------------------------------------------------------------------
def get_stage_datas(soup, url):
    
    #This function get 2 datas about stage building. First building general stage
    #Second is the house stage
    #It returns list always 
    
    my_dict = scrape_base_data(soup, url)
    ending = url[22:]
    result = [ending, "##BUG##", "There may be some unpredictable bugs"]
    stage_list = []
    if type(my_dict) == dict:
        
        if 'Mərtəbə'  in my_dict.keys():
            stage_list = [int(i) for i in my_dict['Mərtəbə'] if i.isdigit()==True]
        else:
            stage_list = [None,None]
    else:
        problem_list_id.append(result)
        stage_list = [0,0]
        
    return stage_list           

#----------------------------------------------------------------------------------------------
def scrape_description(soup, url):
    
    #This function helps us to get data about description of item, and it stores data as str
    #If everything ok, the function returns list, else list
    
    ending = url[22:]
    result_list = []
    article = soup.find('article')
      
    if article != None:
        for i in article:
            result_list.append(i.text)
        result = ''.join(result_list)
        
    else:
        result = [ending, "##BUG##", "article tegi tapılmadı"]

    return result


#----------------------------------------------------------------------------------------------

def scrape_pub_date(soup, url):
    
    #This function helps us to get publishing date or updated date of item in page
    #It returns str in normal cases, else dict
    
    ending = url[22:]
    div = soup.find('div',attrs = {'class':'item_info'})
    result = {}

    if div != None:
        for i in div.find_all('p'):
            p = str(i.text)

            #Skipping useles data
            if p.startswith('Elanın')==True or p.startswith('Baxışların')==True:
                continue

            #Catching the data which we need. We want to store data in dictionary, 
            #so we must to seperate data 2 parts by ':' this char
            else:
                index_pub = p.index(":")
                key_pub = p[:index_pub].strip(" ")
                value_pub = p[index_pub+1:]

                #After parcing process we will see that there will be data which consist of 
                #letters, and it means maybe today or yesterday, so we must to convert it 
                #to other datas date type for example '06 Dekabr 2002'
                
                today_date = date.today()
                ay  = month_converter(str(today_date.month))
                il = str(today_date.year)
   

                if 'Dünən' in value_pub:
                    gun = str(today_date.day -1)
                    my_date = (gun + ' ' + ay + ' ' + il).replace(' ','-')
                    result_list = my_date.split('-')
                    result_list[1] = month_converter(result_list[1])
                    result_str = '-'.join(result_list)
                    result = datetime.strptime(result_str, '%d-%B-%Y')


                elif 'Bugün' in value_pub:
                    gun = str(today_date.day)
                    my_date = (gun + ' ' + ay + ' ' + il).replace(' ','-')
                    result_list = my_date.split('-')
                    result_list[1] = month_converter(result_list[1])
                    result_str = '-'.join(result_list)
                    result = datetime.strptime(result_str, '%d-%B-%Y')

                else:
                    my_date = value_pub[1:-1].replace(' ','-')
                    result_list = my_date.split('-')
                    result_list[1] = month_converter(result_list[1])
                    result_str = '-'.join(result_list)
                    result = datetime.strptime(result_str, '%d-%B-%Y')

    else:
        result = [ending, "##BUG##", "attrs = {'class':'item_info'}) atributlu div tegi tapılmadı"]
        problem_list_id.append(result)
        
    return result

#----------------------------------------------------------------------------------------------

def get_adress_text(soup, url):
    
    #This function helps us to get adress value by text
    #If everything is ok it returns str, else dict
    
    adress_list = []
    ending = url[22:]
    result = [ending, "##BUG##", "Adress_text_error-There are may be some unpredictable bugs"]
    
    divs = soup.find_all('div',attrs = {'class':'map_address'})
    
    if divs != []:
        for div in divs:
            adress_list.append(div.text)
        
        if len(adress_list) == 1:
            result = adress_list[0]
        else:
            result = [ending, "##BUG##", "Address_text_error, len(adress_list)!=0 olmuşdur"]
            problem_list_id.append(result)
    
    else:
        problem_list_id.append(result)
        
    return result

#----------------------------------------------------------------------------------------------
def get_all_city_list(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features='html.parser')
    
    result = []
    a_tag_list = soup.find_all('a',attrs={'class':'footer__locations-i bz-d-flex'})
    
    if len(a_tag_list) != []:
        city_list = [city.text for city in a_tag_list]
        result = city_list
        
    return result

#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------
