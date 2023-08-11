# -*- coding: utf-8 -*-
"""Supervised Learning for Fall detection ARCO Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SABHV4jcqQ9g3xCySND3irkc0a2rFm0O
"""

import numpy as np
import random
def chooseData(org_data, no_of_points):
    # Create a copy of the original data to avoid modifying it
    shuffled_data = org_data.copy()

    # Randomly shuffle the data
    np.random.shuffle(shuffled_data)
    shuffled_data = shuffled_data.tolist()

    reduced_data = random.sample(shuffled_data, no_of_points)

    # Split the data and labels
    data, labels = np.array(reduced_data)[:, :-1], np.array(reduced_data)[:, -1]

    return data, labels

import os
import zipfile
import pandas as pd

zip_path = 'fall-dataset-raw.zip' #zip_path = 'fall-dataset-all.zip'

# Extract the CSV files from the zip file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    csv_files = [file for file in zip_ref.namelist() if file.endswith('.csv')]
    zip_ref.extractall(members=csv_files)

# Read and concatenate the extracted CSV files into a DataFrame
data = pd.concat([pd.read_csv(file, encoding='latin-1') for file in csv_files], ignore_index=True)
accelerometer_data = data[["Acc(X)", "Acc(Y)", "Acc(Z)", "Rot(X)", "Rot(Y)", "Rot(Z)", "Pitch", "Roll", "Yaw", "Timestamp"]].values
labels = list(data["Fall"])#.values
# # Standardize the data
# scaler = StandardScaler()
# standardized_data = scaler.fit_transform(accelerometer_data)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load your dataset
# train_data = pd.read_csv("raw182_Training_Relabeled_Auto_25.csv")

# # Separate features and labels
# raw_data = data[[" ms_accelerometer_x", " ms_accelerometer_y", " ms_accelerometer_z"]].values
# labels = data["outcome"]

num_training_points = 8000
num_testing_points = 2000

data_with_labels = np.column_stack((accelerometer_data, labels))

# Split the data into training and testing sets with an 80:20 ratio
split = int(0.8 * len(data_with_labels))
train_data = data_with_labels[:split]
test_data = data_with_labels[split:]

print(train_data)
print(test_data)

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score

# # Initialize and train the model
# model = RandomForestClassifier(random_state=42)
# model.fit(X_train_scaled, y_train_chosen)

# # Make predictions
# y_pred = model.predict(X_test_scaled)

# # Calculate accuracy
# accuracy = accuracy_score(y_test_chosen, y_pred)
# print(f"Accuracy: {accuracy:.2f}")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score
import numpy as np

# Initialize the model
model = RandomForestClassifier(random_state=42)

# Set the number of iterations
num_iterations = 3
accuracies = []
recalls = []


for iteration in range(num_iterations):
    #Choose different data for training and testing in every iteration
    X_train_chosen, y_train_chosen = chooseData(train_data, num_training_points)
    X_test_chosen, y_test_chosen = chooseData(test_data, num_testing_points)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_chosen)
    X_test_scaled = scaler.transform(X_test_chosen)

    # Initialize and train the model
    model.fit(X_train_scaled, y_train_chosen)

    # Make predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test_chosen, y_pred)
    accuracies.append(accuracy)

    # Calculate recall
    recall = recall_score(y_test_chosen, y_pred)
    recalls.append(recall)

    print(f"Iteration {iteration+1} - Accuracy: {accuracy:.2f}, Recall: {recall:.2f}")

average_accuracy = np.mean(accuracies)
average_recall = np.mean(recalls)

print(f"Average Accuracy across {num_iterations} iterations: {average_accuracy:.2f}")
print(f"Average Recall across {num_iterations} iterations: {average_recall:.2f}")

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Initialize the logistic regression model
logreg_model = LogisticRegression(random_state=42)

# Set the number of iterations
num_iterations = 3
accuracies = []
recalls = []

for iteration in range(num_iterations):
    #Choose different data for training and testing in every iteration
    X_train_chosen, y_train_chosen = chooseData(train_data, num_training_points)
    X_test_chosen, y_test_chosen = chooseData(test_data, num_testing_points)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_chosen)
    X_test_scaled = scaler.transform(X_test_chosen)

    # train the model
    logreg_model.fit(X_train_scaled, y_train_chosen)

    # Make predictions
    y_pred = logreg_model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test_chosen, y_pred)
    accuracies.append(accuracy)

    # Calculate recall
    recall = recall_score(y_test_chosen, y_pred)
    recalls.append(recall)

    print(f"Iteration {iteration+1} - Accuracy: {accuracy:.2f}, Recall: {recall:.2f}")

average_accuracy = np.mean(accuracies)
average_recall = np.mean(recalls)

print(f"Average Accuracy across {num_iterations} iterations: {average_accuracy:.2f}")
print(f"Average Recall across {num_iterations} iterations: {average_recall:.2f}")

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Initialize and train the KNN model
k = 5  # Number of neighbors
knn_model = KNeighborsClassifier(n_neighbors=k)

# Set the number of iterations
num_iterations = 3
accuracies = []
recalls = []

for iteration in range(num_iterations):
    #Choose different data for training and testing in every iteration
    X_train_chosen, y_train_chosen = chooseData(train_data, num_training_points)
    X_test_chosen, y_test_chosen = chooseData(test_data, num_testing_points)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_chosen)
    X_test_scaled = scaler.transform(X_test_chosen)

    # train the model
    knn_model.fit(X_train_scaled, y_train_chosen)

    # Make predictions
    y_pred = knn_model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test_chosen, y_pred)
    accuracies.append(accuracy)

    # Calculate recall
    recall = recall_score(y_test_chosen, y_pred)
    recalls.append(recall)

    print(f"Iteration {iteration+1} - Accuracy: {accuracy:.2f}, Recall: {recall:.2f}")

average_accuracy = np.mean(accuracies)
average_recall = np.mean(recalls)

print(f"Average Accuracy across {num_iterations} iterations: {average_accuracy:.2f}")
print(f"Average Recall across {num_iterations} iterations: {average_recall:.2f}")

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Initialize and train the Naive Bayes model
nb_model = GaussianNB()

# Set the number of iterations
num_iterations = 3
accuracies = []
recalls = []

for iteration in range(num_iterations):
    #Choose different data for training and testing in every iteration
    X_train_chosen, y_train_chosen = chooseData(train_data, num_training_points)
    X_test_chosen, y_test_chosen = chooseData(test_data, num_testing_points)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_chosen)
    X_test_scaled = scaler.transform(X_test_chosen)

    # train the model
    nb_model.fit(X_train_scaled, y_train_chosen)

    # Make predictions
    y_pred = nb_model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test_chosen, y_pred)
    accuracies.append(accuracy)

    # Calculate recall
    recall = recall_score(y_test_chosen, y_pred)
    recalls.append(recall)

    print(f"Iteration {iteration+1} - Accuracy: {accuracy:.2f}, Recall: {recall:.2f}")

average_accuracy = np.mean(accuracies)
average_recall = np.mean(recalls)

print(f"Average Accuracy across {num_iterations} iterations: {average_accuracy:.2f}")
print(f"Average Recall across {num_iterations} iterations: {average_recall:.2f}")
