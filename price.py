# coding:utf-8    ctrl+/  注释
import urllib2
import time
import bs4
from bs4 import BeautifulSoup
import sys
import pymongo
import requests

def geocode(address):
    parameters = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['geocodes']


reload(sys)
sys.setdefaultencoding("utf-8")

connection = pymongo.MongoClient()
tdb = connection.program
post_info = tdb.house


# 链家网d
def find_data(tmp_url, tmp_district, lists):
    count = 0
    # 每个区的最大显示页数为100页
    for page_Num in range(1, 100):
        f_url = tmp_url + tmp_district + "/d" + str(page_Num)
        print f_url
        # print f_url
        f_page = urllib2.urlopen(f_url)
        f_soup = BeautifulSoup(f_page, "html.parser")

        page_soup = f_soup.find(class_="m-list")
        # print page_soup
        ul_soup = page_soup.find('ul')
        # print ul_soup
        li_list = ul_soup.findAll('li')[0:]
        # print page_Num
        for tr in li_list:
            info = tr.findAll(class_="info-row")[0:]
            row1 = info[0].find(class_="info-col row1-text").text

            row1 = row1.strip()
            row1 = row1.replace(' ', '')
            # print row1
            cut_1 = row1.index('|')
            # 几室几厅
            house_type = row1[0:cut_1]
            print house_type
            cut_2 = row1[cut_1 + 1:].index('平')
            # 房屋大小
            house_size = float(row1[cut_1 + 1:cut_1 + cut_2 + 1])
            print house_size
            try:
                cut_3 = row1.index('/')
            except ValueError:
                continue
            cut_4 = row1.index('层')
            # 建筑总层高
            building_height = float(row1[cut_3 + 1:cut_4])
            print building_height
            cut_5 = row1.index('区')
            # 房屋层高
            house_height = row1[cut_5 - 1:cut_5]
            print house_height

            row2 = info[1].find(class_="info-col row2-text")
            # 均价
            average_price = info[1].find(class_="info-col price-item minor").text.strip()
            print average_price
            # 位置
            location = row2.findAll('a')[0:]

            try:
                year_1 = row2.text.index('年建')
                year = row2.text[year_1 - 4:year_1]
            except ValueError:
                continue

            print year_1
            print year
            # 小区
            housing_estate = location[0].text
            print housing_estate
            # 区县
            house_district = location[1].text
            print house_district
            count = count + 1
            # print count
            #
            #
            #整理出room和parlour数量
            room_1=house_type.index('室')
            room_number=int(house_type[0:room_1])
            parlour_1=house_type.index('厅')
            parlour_number=int(house_type[room_1+1:parlour_1])

            #判断房子的具体高度
            if(house_height=='中'):
                house_height_inlist=building_height*0.5
            elif(house_height=='高'):
                house_height_inlist = building_height * 0.88
            elif(house_height == '低'):
                house_height_inlist = building_height * 0.23

            #整理出具体房价
            price_1=average_price.index('价')
            price_2=average_price.index('元')
            average_price_inlist=float(average_price[price_1+1:price_2])

            #每个区映射一个数字
            if(house_district=="浦东"):
                house_district_inlist=4
            elif(house_district=="闵行"):
                house_district_inlist=3
            elif (house_district == "宝山"):
                house_district_inlist = 4
            elif (house_district == "徐汇"):
                house_district_inlist = 2
            elif (house_district == "普陀"):
                house_district_inlist = 2
            elif(house_district=="杨浦"):
                house_district_inlist=2
            elif (house_district == "长宁"):
                house_district_inlist = 2
            elif (house_district == "松江"):
                house_district_inlist = 4
            elif (house_district == "嘉定"):
                house_district_inlist = 4
            elif (house_district == "黄浦"):
                house_district_inlist = 1
            elif (house_district == "静安"):
                house_district_inlist = 1
            elif (house_district == "闸北"):
                house_district_inlist = 2
            elif (house_district == "虹口"):
                house_district_inlist = 2
            elif (house_district == "青浦"):
                house_district_inlist = 3
            elif (house_district == "奉贤"):
                house_district_inlist = 4
            elif (house_district == "金山"):
                house_district_inlist = 4
            elif (house_district == "崇明"):
                house_district_inlist = 5

            #计算地址经纬度
            address = house_district+housing_estate
            print address

            house_first_location=geocode(address)
            if(house_first_location==[]):
                continue
            house_location=geocode(address)[0]['location'].encode('utf-8')

            house_location_1=house_location.index(',')
            house_location_longtitude=float(house_location[0:house_location_1])
            print house_location_longtitude
            house_location_latitude=float(house_location[house_location_1+1:])
            print house_location_latitude
            list_use = [room_number,parlour_number, house_size, building_height, house_height_inlist,house_location_latitude,house_location_longtitude,float(year),
                        average_price_inlist]
            print list_use
            lists.extend([list_use])

            print "{\"户型\":\"%s\", \"大小\":\"%s\",\"楼高\":\"%s\",\"层高\":\"%s\",\"小区名\":\"%s\",\"市区\":\"%s\",\"均价\":\"%s\"}" % (
                house_type, house_size, building_height, house_height, housing_estate, house_district, average_price)
            # data = {"house_type": house_type, "house_size": house_size,"building_height": building_height,"house_height": house_height,"housing_estate": housing_estate,"house_district": house_district,"average_price": average_price}
            # post_info.save(data)
            # print "end"
            # print "all_end"


def use(district):
    lists = []
    for i in district:
        find_data('http://sh.lianjia.com/ershoufang/', i, lists)
    return lists

b=["jinshan"]
a = ["pudongxinqu", "minhang", "baoshan", "xuhui", "putuo", "yangpu", "changning", "songjiang", "jiading", "huangpu",
     "jingan", "zhabei", "hongkou", "qingpu", "fengxian", "jinshan", "chongming"]

dataset = use(a)

import numpy as np
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

_array = np.array(dataset)
x = _array[:, 0:8]
y = _array[:, 8]
X_train, X_test, y_train, y_test = train_test_split(x, y)

print X_train.shape
print y_train.shape
print X_test.shape
print y_test

abc = LinearRegression()
abc.fit(X_train, y_train)

y_pred = abc.predict(X_test)

print y_pred

print np.sqrt(metrics.mean_squared_error(y_test, y_pred))





