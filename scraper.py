import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl, QEventLoop
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from bs4 import BeautifulSoup
import requests
import csv


class Client(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


# MAIN

page = Client(
    'https://www.air.irctc.co.in/onewaytrip?type=O&origin=BOM&originCity=Mumbai&originCountry=IN&destination=MAA&destinationCity=Chennai&destinationCountry=IN&flight_depart_date=2020-04-11&ADT=1&CHD=0&INF=0&class=Economy&airlines=&ltc=0&searchtype=')

soup = BeautifulSoup(page.html, 'lxml')


airline = soup.find_all('div', class_='right_Airline_no')
price = soup.find_all('strong', class_="red-text")
dep_time = soup.find_all('div', class_='SearchData_List_in SearchData_Departure font-14')
arr_time = soup.find_all('div', class_="SearchData_List_in SearchData_Arrival font-14")
duration = soup.find_all('div', class_="SearchData_List_in SearchData_Duration font-14")
status = soup.find_all('div', class_="SearchData_List_in SearchData_Price")

csv_file = open('BOM-MAA.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['flight_no', 'airline', 'dep_time', 'duration', 'stop', 'arr_time', 'price1'])

number_l = list()
name_l = list()
for no in airline:
    number = no.find_all('span')[1]
    name = no.find_all('span')[0]
    number_l.append(number.get_text())
    name_l.append(name.get_text())

dep_time_l = list()
for dtime in dep_time:
    time = dtime.find('strong')
    dep_time_l.append(time.get_text())
    # print(time.get_text())

price_l = list()
for p in price:
    l_price = list(p.get_text())
    v = int(''.join(l_price[2:len(l_price)]))
    # print(v)
    price_l.append(v)

arr_time_l = list()
for atime in arr_time:
    time = atime.find('strong')
    # print(time.get_text(),'--',stop.get_text())
    arr_time_l.append(time.get_text())

duration_l = list()
stop_l = list()
for d in duration:
    dur = d.find('strong')
    stop = d.find('span')
    # print(dur.get_text(),'--',stop.get_text())
    duration_l.append(dur.get_text())
    stop_l.append(stop.get_text())

for i in range(0, len(price_l)):
    csv_writer.writerow([number_l[i], name_l[i], dep_time_l[i], duration_l[i], stop_l[i], arr_time_l[i], price_l[i]])

csv_file.close()

'''    
count = 0
for r in status:
    st = r.find(class_="font-12")
    if st.get_text() == "(Partially Refundable)":
        count=count+1
    if st.get_text() == "(Non Refundable)":
        count=count+1

print(count)

'''














