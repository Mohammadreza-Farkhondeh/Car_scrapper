from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as ps
import datetime
from unidecode import unidecode

#definig empty variables and desired Car brands
brands = ['pride', 'peugeot','dena', 'samand']
DATA = {}
data = []
price = []
milage = []

#Getting pages and scrapping data from them
for brand in brands:

    #try for getting pages
    try:
        url = 'https://divar.ir/s/tehran/car/'+brand
        print(f'Try to get all of {brand}.')
        
        #defining page and soup
        r = requests.get(url, timeout=5 )
        soup = bs(r.text, 'html.parser')
        
        #finding divs with desired class
        res = soup.find_all('div', attrs={'class' : 'kt-post-card__body'})

        #finding patterns for title and details in finded divs
        #also append data to DATA dictionary
        pattern1 = r'<h2 class="kt-post-card__title">(.*?)</h2>'
        pattern2 = r'<div class="kt-post-card__description">(.*?)</div>'
        for i in range(len(res)):
            result1 = re.search(pattern1, str(res[i]))
            result2 = re.findall(pattern2, str(res[i]))
            if result1:
                data.append(result1.group(1))
            else:
                continue
            if result1:
                milage.append(result2[0])
                price.append(result2[1])
            else:
                continue
            DATA.update({'data':data, 'milage':milage, 'price':price})
        print(f'{brand} done')
    except:
        print(f'{brand} failed')

#deleting measures and converting persian numbers to english UTF-8
for var in ['price','milage']:
    for i in range(len(DATA[var])):
        p = DATA[var][i].split()[0]
        p = unidecode(p)
        DATA[var][i] = p



#defined file name with date and seving dATA to excel file
time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_name = f'scraped-divar-importants-{time}'

df = ps.DataFrame(DATA).to_excel(file_name+'.xlsx')


print(len(DATA['data']), 'car found')
