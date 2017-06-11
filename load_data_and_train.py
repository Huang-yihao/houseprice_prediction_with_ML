# coding:utf-8    ctrl+/  注释
import sys
import pymongo
import numpy as np

reload(sys)
sys.setdefaultencoding("utf-8")

connection = pymongo.MongoClient()
tdb = connection.program
post_info = tdb.house

lists=[]
count=0

for item in post_info.find():
    count+=1
    tmp=0

    if (item["house_district"].encode("utf-8")=="宝山"):
        tmp=1
    elif (item["house_district"].encode("utf-8")=="浦东"):
        tmp=2
    elif (item["house_district"].encode("utf-8")=="闵行"):
        tmp=3
    elif (item["house_district"].encode("utf-8")=="徐汇"):
        tmp=4
    elif (item["house_district"].encode("utf-8")=="普陀"):
        tmp=5
    elif (item["house_district"].encode("utf-8")=="杨浦"):
        tmp=6
    elif (item["house_district"].encode("utf-8")=="长宁"):
        tmp=7
    elif (item["house_district"].encode("utf-8")=="松江"):
        tmp=8
    elif (item["house_district"].encode("utf-8")=="嘉定"):
        tmp=9
    elif (item["house_district"].encode("utf-8")=="黄浦"):
        tmp=10
    elif (item["house_district"].encode("utf-8")=="静安"):
        tmp=11
    elif (item["house_district"].encode("utf-8")=="闸北"):
        tmp=12
    elif (item["house_district"].encode("utf-8")=="虹口"):
        tmp=13
    elif (item["house_district"].encode("utf-8")=="青浦"):
        tmp=14
    elif (item["house_district"].encode("utf-8")=="奉贤"):
        tmp=15
    elif (item["house_district"].encode("utf-8")=="金山"):
        tmp=16
    elif (item["house_district"].encode("utf-8")=="崇明"):
        tmp=17

    single_item=[item["room_number"],item["parlour_number"],item["house_size"],item["year"],
                 item["building_height"],item["house_height_inlist"],item["house_location_longtitude"],
                 item["house_location_latitude"],tmp,item["average_price_inlist"]]
    lists.extend([single_item])
    #print count


from sklearn import metrics
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

_array = np.array(lists)
x = _array[:, 0:9]
#normalized_X=preprocessing.normalize(x)
y = _array[:, 9]
#normalized_Y=preprocessing.normalize(y)
X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.2)

print X_train.shape
print y_train.shape
print X_test.shape
print y_test

clf = LinearRegression()
clf.fit(X_train, y_train)
print clf.coef_
y_pred = clf.predict(X_test)

print np.sqrt(metrics.mean_squared_error(y_test, y_pred))


#神经网络
# from sklearn.neural_network import MLPRegressor
# kmodel = MLPRegressor(learning_rate='adaptive',max_iter=2000).fit(X_train, y_train)
# y_kmodel_pred = kmodel.predict(X_test)
# print np.sqrt(metrics.mean_squared_error(y_test, y_kmodel_pred))

# #svm模型
# from sklearn import svm
# smodel=svm.LinearSVR()
# smodel.fit(X_train, y_train)
#
# print smodel.score(X_test,y_test)


#决策树模型
from sklearn.tree import DecisionTreeRegressor
dmodel=DecisionTreeRegressor()
dmodel.fit(X_train, y_train)

y_dmodel_pred=dmodel.predict(X_test)
print y_dmodel_pred
print np.sqrt(metrics.mean_squared_error(y_test, y_dmodel_pred))
print dmodel.score(X_test,y_test)

