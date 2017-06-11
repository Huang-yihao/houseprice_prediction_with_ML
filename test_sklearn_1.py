import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
import urllib
# url with dataset
url = "http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
# download the file
raw_data = urllib.urlopen(url)
# load the CSV file as a numpy matrix

#"C:\Users\charles\Desktop\kkk.txt"
dataset = np.loadtxt(raw_data, delimiter=",")

lists = []

lists.extend([[0,1,2,3,4,5,6,7,8]])
lists.extend([[2,3,4,5,6,7,8,9,10]])

_array=np.array(lists)
# separate the data from the target attributes
X = _array[:,0:7]
y = _array[:,8]

#print dataset

# normalize the data attributes
normalized_X = preprocessing.normalize(X)
# standardize the data attributes
standardized_X = preprocessing.scale(X)


model = ExtraTreesClassifier()
model.fit(X, y)
# display the relative importance of each attribute
print(model.feature_importances_)



model = LogisticRegression()
model.fit(X, y)
#print(model)
# make predictions
expected = y
predicted = model.predict(X)
# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
