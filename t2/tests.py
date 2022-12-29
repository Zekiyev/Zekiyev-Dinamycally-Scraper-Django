from django.test import TestCase

# Create your tests here.
from utils import *

def get_stage_datas(url):
    my_dict = scrape_base_data(url)
    ending = url[22:]
    result = [ending, "##BUG##", "There may be some unpredictable bugs"]
    stage_list = []
    if type(my_dict) == dict:
        
        if 'Mərtəbə'  in my_dict.keys():
            stage_list = [int(i) for i in my_dict['Mərtəbə'] if i.isdigit()==True]
        else:
            stage_list = [None,None]
    else:
        #error_list_id.append(result)
        stage_list = [0,0]
    return  stage_list