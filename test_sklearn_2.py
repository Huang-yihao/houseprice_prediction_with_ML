import numpy as np
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

lists = []

lists.extend([[1,1,2]])
lists.extend([[2,2,4]])
lists.extend([[3,3,6]])
lists.extend([[-1,-1,-2]])
lists.extend([[-2,-2,-4]])
lists.extend([[-3,-3,-6]])

_array=np.array(lists)
x = _array[:,0:2]
y = _array[:,2]
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1)


print x
print y
print X_train.shape
print y_train.shape
print X_test.shape
print y_test.shape

abc=LinearRegression()
abc.fit(X_train,y_train)


y_pred=abc.predict(X_test)

print y_pred

print np.sqrt(metrics.mean_squared_error(y_test, y_pred))
