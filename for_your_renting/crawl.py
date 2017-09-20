import requests
import csv
from bs4 import BeautifulSoup as Bs
from urllib.parse import urljoin

url = 'http://gz.58.com/tianhe/pinpaigongyu/pn/{page}/?minprice=1500_2000'
page = 0

csv_file = open("rent.csv", "w")
csv_writer = csv.writer(csv_file, delimiter=',')


while True:
    page += 1
    print('fetching:', url.format(page=page))
    res = requests.get(url.format(page=page))
    result = Bs(res.text, 'html.parser')
    house_list = result.select('.list > li')

    if not house_list:
        break

    for house in house_list:
        house_title = house.select('h2')[0].text
        house_url = urljoin(url, house.select('a')[0]['href'])
        house_info_list = house_title.split()

        if '公寓' in house_info_list[1] or '青年公寓' in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select('.money')[0].select('b')[0].text
        csv_writer.writerow([house_title, house_location, house_money, house_url])

csv_file.close()
