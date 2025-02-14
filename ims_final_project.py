# -*- coding: utf-8 -*-
"""IMS Final Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Koj1VNIJsq9GevDpi22PVaDVC0jHMUwY

**Introduction To Modelling & Simulation Final Project**
***

This Artificial Intelligence Model was built by Samuel Dartey-Baah, Eric Afari, Eddy Kubwimana, Kelvin Yanney, Emmanuel Agyei and Bismark Bedzrah.

The purpose of this model is to train a model to detect if an engine is in a good condition or not based on parameters;

Engine rpm: Revolutions per minute (rpm)

Lub oil pressure in Pounds per square inch (psi)

Fuel pressure in Pounds per square inch (psi)

Coolant pressure in Pounds per square inch (psi)

Lub oil temp in Degrees Celsius (°C)

Coolant temp in Degrees Celsius (°C)

This model can be used to detect early engine failure.
"""

from google.colab import drive
drive.mount('/content/drive')

# installing scikeras to import KerasClassifier
!pip install scikeras
!pip install keras-tuner

#importing necessary libraries which would be used
import pandas as pd
import numpy as np
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
import kerastuner as kt
from keras.models import Model
from keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from tensorflow import keras
from sklearn.impute import SimpleImputer
from keras.models import Sequential
from keras.layers import Dense, Input
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler

#importing the data set
engine_df = pd.read_csv('/content/drive/MyDrive/engine_data.csv')

engine_df.head()
#Note for engine condition; 0 is good and 1 is bad

#checking to see if there are any null values
print(engine_df.isnull().sum())
print('This shows that there are no null values in our dataset')

#checking the data types of the various values
engine_df.info()

"""**Training AI Model**"""

#splitting the output and input
X = engine_df.drop('Engine Condition', axis=1)
y = engine_df['Engine Condition']

# scaling the X
needed_features = X.columns.tolist()
from sklearn.preprocessing import StandardScaler
StandardScaler = StandardScaler()

X = StandardScaler.fit_transform(X.copy())
X = pd.DataFrame(X, columns = needed_features)

# splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state= 5)

# getting the number of neurons to be used
number_of_neurons = X_train.shape[1]

# create a functional api with keras
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import Adam

# Determine the number of input features
number_of_neurons = X.shape[1]

def create_model(activation='relu', hidden_layer_sizes=(5, 5), input_shape=(number_of_neurons,)):
    input_layer = Input(shape=input_shape)
    hidden_layer1 = Dense(hidden_layer_sizes[0], activation=activation)(input_layer)
    hidden_layer2 = Dense(hidden_layer_sizes[1], activation=activation)(hidden_layer1)
    output_layer = Dense(1, activation='sigmoid')(hidden_layer2)

    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    return model

# Assuming you have already split your data into training and test sets
# X_train, X_test, y_train, y_test = ...

model = create_model()
model.fit(X_train, y_train, epochs=100)

model.evaluate(X_test, y_test)

# defining parameters for the grid search
param_grid = {
    'hidden_layer_sizes': [(5, 5), (10, 10)],
    'activation': ['relu', 'tanh'],
    'batch_size': [16, 32],
    'epochs': [50, 100]
}

# creating an MLP classifier
mlp_classifier = KerasClassifier(build_fn = create_model, activation='relu',hidden_layer_sizes=(5, 5),verbose=0)

# using GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(estimator=mlp_classifier, param_grid=param_grid, n_jobs=-1, cv=3, scoring='accuracy')
grid_result = grid_search.fit(X_train, y_train)

# finding the best parameters
best_params = grid_result.best_params_
print(best_params)

#creating instance for a tuned model
tuned_model = create_model(
    activation=best_params['activation'],
    hidden_layer_sizes=best_params['hidden_layer_sizes']
    )

# tuning the model with the tuned hyperparameters and evaluating the model
tuned_model.fit(X_train, y_train, epochs=best_params['epochs'], batch_size=best_params['batch_size'])
tuned_model.evaluate(X, y)

# Evaluating the model's accuracy on the test set
accuracy = tuned_model.evaluate(X_test, y_test)[1]
print(f'Tuned Model Accuracy: {accuracy}')
print()

# Predicting probabilities for the test set
y_pred_prob = tuned_model.predict(X_test)

# Calculating the AUC score
auc_score = roc_auc_score(y_test, y_pred_prob)
print(f'Tuned Model AUC Score: {auc_score}')
print()

# Save the functional tuned model
#tuned_model.save('tuned_model.h5')

model.save('tuned_model')

import pickle
with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(StandardScaler, scaler_file)