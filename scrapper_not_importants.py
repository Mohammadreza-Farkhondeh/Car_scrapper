from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as ps
import datetime
from unidecode import unidecode

brands = ['arisun', 'mvm', 'merecedes-benz', 'bmw', 'porsche', 'peykan', 'tara',
          'tiba', 'jac', 'changan', 'chery', 'volkswagen', 'suzuki', 'mazda',
          'nissan', 'volvo', 'runna', 'zamyad','shahin', 'lifan',]
DATA = {}
data = []
price = []
milage = []


for brand in brands:
    try:
        url = 'https://divar.ir/s/tehran/car/'+brand
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


for var in ['price','milage']:
    for i in range(len(DATA[var])):
        p = DATA[var][i].split()[0]
        p = unidecode(p)
        DATA[var][i] = p




time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_name = f'scraped-divar-not-importants- {time}'

df = ps.DataFrame(DATA).to_excel(file_name+'.xlsx')


print(len(DATA['data']), 'car found')
