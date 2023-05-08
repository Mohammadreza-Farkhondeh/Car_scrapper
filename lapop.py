from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as ps
import datetime
from unidecode import unidecode

brands = ['lenovo', 'hp', 'dell', 'asus', 'apple', 'acer']
DATA = {}
data = []
price = []
milage = []


for brand in brands:
    try:
        url = f'https://divar.ir/s/tehran/laptop-notebook-macbook/{brand}?goods-business-type=all'
        print(f'Try to get all of {brand}.')

        r = requests.get(url, timeout=5 )
        soup = bs(r.text, 'html.parser')

        res = soup.find_all('div', attrs={'class' : 'kt-post-card__body'})
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


    for i in range(len(DATA['milage'])):
        p = DATA['milage'][i]
        # p = unidecode(p)
        if p == 'نو':
            p = 'A'
        elif p == 'در حد نو':
            p = 'B'
        elif p =='کارکرده':
            p = 'C'
        elif p == 'نیازمند تعمیر':
            p = 'D'

        DATA['milage'][i] = p




time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_name = f'scraped-divar-laptops-{time}'

df = ps.DataFrame(DATA).to_excel(file_name+'.xlsx')


print(len(DATA['data']), 'car found')
