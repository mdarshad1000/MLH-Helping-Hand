#loading dataset
import pandas as pd
import numpy as np
# data preprocessing
from sklearn.preprocessing import StandardScaler
# data splitting
from sklearn.model_selection import train_test_split
# data modelling
from sklearn.linear_model import LinearRegression

import warnings
warnings.filterwarnings("ignore")

import pickle

data = pd.read_csv(r".\ml model\data.csv")

#Model Preparation 

y = data["Food Wasted"]
X = data.drop('Food Wasted',axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state = 0)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

lnr = LinearRegression()
lnr.fit(X_train, y_train)

# y_prediction =  lnr.predict(X_test)
# y_prediction
# from sklearn.metrics import r2_score
# from sklearn.metrics import mean_squared_error

# score=r2_score(y_test,y_prediction)
# print('r2 socre is ',score)
# print('mean_sqrd_error is==',mean_squared_error(y_test,y_prediction))
# print('root_mean_squared error of is==',np.sqrt(mean_squared_error(y_test,y_prediction)))

pickle.dump(lnr,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))


def training_scaler(X_train=X_train):

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    return scaler
