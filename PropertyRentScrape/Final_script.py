"""
This script will scrape information from a house rent website once run
"""

# importing all neccessary packages for this script
import requests
import bs4
import lxml
import datetime
from datetime import date
from datetime import datetime

#base_url = "https://nigeriapropertycentre.com/for-rent/lagos/"

#initiating the page number of the website
page_num = 1

house_dict={
    'location':[],
    'price':[],
    'link':[],
    'features':[]
}

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

#user to input desired specifications for the search
max_prize = input('State your max price: ')
bed_number = input('how many bedrooms: ')


cont = True

num = 0

while cont:

    query = f'https://nigeriapropertycentre.com/for-rent/lagos/{location.lower()}?bedrooms={bed_number}&maxprice={max_prize}&selectedLoc=1&q=for-rent+lagos+{location}+{bed_number}+bedrooms+maxprice+{max_prize}&page={page_num}'

    print(query)

    #requests.adapters.DEFAULT_RETRIES = 5
    search_request = requests.get(query)
    search_soup = bs4.BeautifulSoup(search_request.text, 'lxml')

    info = search_soup.select(".wp-block-body")
    check = len(info)

    
    if check > 0:
        print('we are good to go')
        
        for n in range(check):

            feature = ['kitchen', 'shared', 'Prepaid Meter', 'sharing', 'shared', 'parlour', 'mini flat']
            
            search_dict['hd'+str(num)] = {
                'location':info[n].address.text.strip(' \xa0'), 
                'price':int(info[n].select(".price")[1].text.replace(',','')), 
                'link':'https://nigeriapropertycentre.com/'+info[n].a['href'],
                'features':''
            }
            
            new_url = 'https://nigeriapropertycentre.com/' + info[n].a['href']
            mini_req = requests.get(new_url)
            mini_soup = bs4.BeautifulSoup(mini_req.text, 'lxml')

            print(mini_soup.select(".tab-body")[0].text)

            ft = []
            for feature in feature:
                if feature in mini_soup.select(".tab-body")[0].text:                    
                    ft.append(feature)
            ft_set = set(ft)
            search_dict['hd'+str(num)]['features'] = ', '.join(ft_set)


            num += 1

        
        page_num += 1

    else:
        print('we are not good to go')
        cont = False



format = '%y-%m-%d_%H:%M'

period = datetime.now().strftime(format)


file_name = 'result_' + period + '.txt'
file = open(file_name, 'w+')
file.write(str(search_dict))
file.close()