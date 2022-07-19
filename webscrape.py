"""
This script will scrape information from a house rent website once run
"""


import requests
import bs4
import lxml
import datetime
from datetime import date
from datetime import datetime
import pandas as pd


def dict_to_excel(dict_info):
    data = pd.DataFrame.from_dict(dict_info).transpose()
    data.to_excel('Test_excel.xlsx', sheet_name='Test creation')

def id_num(link):
    id = ''
    for i in range(len(link)):
        if link[i].isdigit():
            id+=link[i]
            if link[i+1]=='-':
                break
    return id

#base_url = "https://nigeriapropertycentre.com/for-rent/lagos/"

page_num = 1

spec_list = ['kitchen', 'shared', 'Prepaid Meter']
loc_list = []
LOC = []
search_dict = {}

print('Welcome, answer the following questions to begin web scrape')


location = input(
    """
    Choose from the following locations:

    - Ajah 
    - Sangotedo
    - Lekki
    - Abijo 
    - lekki-ibeju   
    
    :- 
    """ 
    )

max_prize = input('State your max price: ')
bed_number = input('how many bedrooms: ')

cont = True

num = 0

while cont:

    query = f'https://nigeriapropertycentre.com/for-rent/lagos/{location.lower()}?bedrooms={bed_number}&maxprice={max_prize}&selectedLoc=1&q=for-rent+lagos+{location}+{bed_number}+bedrooms+maxprice+{max_prize}&page={page_num}'

    print(query)
    requests.adapters.DEFAULT_RETRIES = 5
    search_request = requests.get(query)
    search_soup = bs4.BeautifulSoup(search_request.text, 'lxml')

    info = search_soup.select(".wp-block-body")
    check = len(info)

    
    if check > 0:
        print('we are good to go')
        
        for n in range(check):

            p = ['kitchen', 'Prepaid Meter', 'sharing', 'shared', 'parlour', 'mini flat', 'miniflat']
            
            id = id_num(info[n].a['href'])
             
            search_dict[id] = {
                'location':info[n].address.text.strip(' \xa0'), 
                'price':int(info[n].select(".price")[1].text.replace(',','')), 
                'link':'https://nigeriapropertycentre.com'+info[n].a['href'],
                'features':''
            }
            
            

            new_url = search_dict[id]['link']
            mini_req = requests.get(new_url)
            mini_soup = bs4.BeautifulSoup(mini_req.text, 'lxml')

            
            ft = []
            for p in p:
                if p in mini_soup.select(".tab-body")[0].text.lower():                    
                    ft.append(p)
            ft_set = set(ft)
            search_dict[id]['features'] = ', '.join(ft_set)


            num += 1

        
        page_num += 1

    else:
        print('we are not good to go')
        cont = False



#format = '%y-%m-%d_%H:%M'
format1 ='%y-%m-%d'

period = datetime.now().strftime(format1)

print(period)
file_name = 'result_' + period + '.txt'
print(file_name)
file = open(file_name, 'w')
file.write(str(search_dict))
file.close()

dict_to_excel(search_dict)