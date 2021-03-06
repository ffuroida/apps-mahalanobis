import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
# import seaborn as sns
# sns.set(color_codes=True)
# import matplotlib.pyplot as plt

from numpy.random import seed
from tensorflow.python.keras import backend as K
from tensorflow import set_random_seed

from keras.layers import Input, Dropout
from keras.layers.core import Dense 
from keras.models import Model, Sequential, load_model
from keras import regularizers
from keras.models import model_from_json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

# Calculate the covariance matrix
def cov_matrix(data, verbose=False):
    covariance_matrix = np.cov(data, rowvar=False)
    if is_pos_def(covariance_matrix):
        inv_covariance_matrix = np.linalg.inv(covariance_matrix)
        if is_pos_def(inv_covariance_matrix):
            return covariance_matrix, inv_covariance_matrix
        else:
            print("Error: Inverse of Covariance Matrix is not positive definite!")
    else:
        print("Error: Covariance Matrix is not positive definite!")
        

# Calculate the Mahalanobis distance
def MahalanobisDist(inv_cov_matrix, mean_distr, data, verbose=False):
    inv_covariance_matrix = inv_cov_matrix
    vars_mean = mean_distr
    diff = data - vars_mean
    md = []
    for i in range(len(diff)):
        md.append(np.sqrt(diff[i].dot(inv_covariance_matrix).dot(diff[i])))
    return md


# Calculate threshold value for classifying datapoint as anomaly
def MD_threshold(dist, extreme=False, verbose=False):
    k = 1. if extreme else 2.
    threshold = np.mean(dist) * k
    return threshold


# Detecting outliers
def MD_detectOutliers(dist, extreme=False, verbose=False):
    k = 3. if extreme else 2.
    threshold = np.mean(dist) * k
    outliers = []
    for i in range(len(dist)):
        if dist[i] >= threshold:
            outliers.append(i)  # index of the outlier
    return np.array(outliers)


# Check if matrix is positive definite
def is_pos_def(A):
    if np.allclose(A, A.T):
        try:
            np.linalg.cholesky(A)
            return True
        except np.linalg.LinAlgError:
            return False
    else:
        return False
    
    

headers = ['date','abpmean','hr','pulse','resp','spo2','label']
dataset = pd.read_csv('dataset1.csv',names=headers)
# dataset = dataset.drop(dataset.columns[0], axis=1)
dataset.label = pd.factorize(dataset.label)[0]
X = dataset.iloc[:, 1:6]
y = dataset.label
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=1)
sc = MinMaxScaler(feature_range=(0, 1))
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
pca = PCA(n_components=2)
principalComponents_Xtrain = pca.fit_transform(X_train)
principalComponents_Xtest = pca.transform(X_test)
principalDf = pd.DataFrame(data = principalComponents_Xtrain, columns = ['principal component 1', 'principal component 2'])

# Set up PCA model
data_train = np.array(principalComponents_Xtrain)
data_test = np.array(principalComponents_Xtest)

# Calculate the covariance matrix and its inverse, based on data in the training set
cov_matrix, inv_cov_matrix  = cov_matrix(data_train)

# calculate the mean value for the input variables in the training set
mean_distr = data_train.mean(axis=0)

# calculate the Mahalanobis distance for the datapoints in the test set, and compare that with the anomaly threshold
dist_test = MahalanobisDist(inv_cov_matrix, mean_distr, data_test, verbose=False)
dist_train = MahalanobisDist(inv_cov_matrix, mean_distr, data_train, verbose=False)
threshold = MD_threshold(dist_train, extreme = True)

# well as the threshold value and “anomaly flag” variable for both train and test data in a dataframe
anomaly_train = pd.DataFrame()
anomaly_train['Mob dist']= dist_train
anomaly_train['Thresh'] = threshold
# If Mob dist above threshold: Flag as anomaly
anomaly_train['Anomaly'] = anomaly_train['Mob dist'] > anomaly_train['Thresh']
# anomaly_train = data_train

anomaly = pd.DataFrame()
anomaly['Mob dist']= dist_test
anomaly['Thresh'] = threshold
# If Mob dist above threshold: Flag as anomaly
anomaly['Anomaly'] = anomaly['Mob dist'] > anomaly['Thresh']
# print("==========================")
return anomaly
    