# -*- coding: utf-8 -*-
"""Supervised Learning for Fall detection SmartFall Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rz0jS3wGBP3nB4jU-cblvIbeteTHmPZr
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

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load your dataset
train_data = pd.read_csv("raw182_Training_Relabeled_Auto_25.csv")

# Separate features and labels
X_train = train_data[[" ms_accelerometer_x", " ms_accelerometer_y", " ms_accelerometer_z"]].values
y_train = train_data["outcome"]

# X_train = X_train[:8000]
# y_train = y_train[:8000]

# Split data into training and testing sets
test_data = pd.read_csv("raw91_Testing_Relabeled_Auto_25.csv")

X_test = test_data[[" ms_accelerometer_x", " ms_accelerometer_y", " ms_accelerometer_z"]].values
y_test = test_data["outcome"]

# X_test = X_test[:2000]
# y_test = y_test[:2000]

num_training_points = 8000
num_testing_points = 2000

train_data = np.column_stack((X_train, y_train))
test_data = np.column_stack((X_test, y_test))

print(train_data)
print(test_data)

y_train

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
