# -*- coding: utf-8 -*-
"""Supervised Learning for Fall detection SisFall Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cCdjHzpDiuASawiv7OGupV0YYJ2ZohVH
"""

import numpy as np
import random

# Function to randomly select required number of data points
def chooseData(org_data, no_of_points):
    # Create a copy of the original data to avoid modifying it
    shuffled_data = org_data.copy()

    # Randomly shuffle the data
    np.random.shuffle(shuffled_data)
    shuffled_data = shuffled_data.tolist()

    # Sample required number of points
    reduced_data = random.sample(shuffled_data, no_of_points)

    # Split the data and labels
    data, labels = np.array(reduced_data)[:, :-1], np.array(reduced_data)[:, -1]

    return data, labels

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

!pip install psutil
!pip install codecarbon
import psutil
from codecarbon import EmissionsTracker

# Get the initial memory usage before loading the dataset
memory_before=psutil.virtual_memory().used

# Initialize the emissions tracker for tracking carbon emissions
emissions_tracker=EmissionsTracker()
emissions_tracker.start()

# Load the dataset
data = pd.read_csv("SisFall_dataset.csv")

# Separate features and labels
data_final = data[["ADXL345_x",	"ADXL345_y",	"ADXL345_z",	"ITG3200_x",	"ITG3200_y",	"ITG3200_z",	"MMA8451Q_x",	"MMA8451Q_y",	"MMA8451Q_z"]].values
# Map labels to binary values (1 for "Fall" and 0 for "Not Fall")
labels = data["Situation"].map({"Fall": 1, "Not Fall": 0})

labels

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

num_training_points = 8000
num_testing_points = 2000

# Combine data and labels into a single array for easy shuffling
data_with_labels = np.column_stack((data_final, labels))

# Split the data into training and testing sets with an 80:20 ratio
split = int(0.8 * len(data_with_labels))
train_data = data_with_labels[:split]
test_data = data_with_labels[split:]

import matplotlib.pyplot as plt

# Setup for experiment with different training data sizes
training_data_sizes = np.arange(0.1, 1.1, 0.3)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score
import numpy as np


# Initialize the model
model = RandomForestClassifier(random_state=42)

# Set the number of iterations
num_iterations = 3

avg_accuracies_rf=[]
avg_recalls_rf=[]

for size in training_data_sizes:
  #Choose appropriate training data size
  num_samples = int(num_training_points * size)
  print("Training data size : " + str(num_samples))
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
  avg_accuracies_rf.append(average_accuracy)
  avg_recalls_rf.append(average_recall)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(training_data_sizes, avg_accuracies_rf, label='Accuracy')
plt.plot(training_data_sizes, avg_recalls_rf, label='Recall')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Effect of Training Data Size on Model Performance')
plt.legend()
plt.show()

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score
import numpy as np


# Initialize the logistic regression model
logreg_model = LogisticRegression(random_state=42)

# Set the number of iterations
num_iterations = 3

avg_accuracies_lr=[]
avg_recalls_lr=[]

for size in training_data_sizes:
  #Choose appropriate training data size
  num_samples = int(num_training_points * size)
  print("Training data size : " + str(num_samples))
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
  avg_accuracies_lr.append(average_accuracy)
  avg_recalls_lr.append(average_recall)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(training_data_sizes, avg_accuracies_lr, label='Accuracy')
plt.plot(training_data_sizes, avg_recalls_lr, label='Recall')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Effect of Training Data Size on Model Performance')
plt.legend()
plt.show()

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, recall_score



# Initialize and train the KNN model
k = 5  # Number of neighbors
knn_model = KNeighborsClassifier(n_neighbors=k)

# Set the number of iterations
num_iterations = 3

avg_accuracies_knn=[]
avg_recalls_knn=[]

for size in training_data_sizes:
  #Choose appropriate training data size
  num_samples = int(num_training_points * size)
  print("Training data size : " + str(num_samples))
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
  avg_accuracies_knn.append(average_accuracy)
  avg_recalls_knn.append(average_recall)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(training_data_sizes, avg_accuracies_knn, label='Accuracy')
plt.plot(training_data_sizes, avg_recalls_knn, label='Recall')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Effect of Training Data Size on Model Performance')
plt.legend()
plt.show()

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, recall_score


# Initialize and train the Naive Bayes model
nb_model = GaussianNB()

# Set the number of iterations
num_iterations = 3

avg_accuracies_nb=[]
avg_recalls_nb=[]

for size in training_data_sizes:
  #Choose appropriate training data size
  num_samples = int(num_training_points * size)
  print("Training data size : " + str(num_samples))
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
  avg_accuracies_nb.append(average_accuracy)
  avg_recalls_nb.append(average_recall)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(training_data_sizes, avg_accuracies_nb, label='Accuracy')
plt.plot(training_data_sizes, avg_recalls_nb, label='Recall')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Effect of Training Data Size on Model Performance')
plt.legend()
plt.show()

# Measure final memory usage
memory_after=psutil.virtual_memory().used

# Calculate energy consumption
emissions: float = emissions_tracker.stop()
print("Energy Consumption :",emissions)

# Calculate memory used in MB
memory_used= (memory_after - memory_before)/(1024*1024)
print("Total memory used for processing in MB : ",memory_used)

avg_accuracies_CL=[0.8733333333333332, 0.8785833333333333, 0.8881666666666667, 0]
avg_recalls_CL=[0.14155829550566393, 0.13419172736950905, 0.2566781463889553, 0]

import matplotlib.pyplot as plt

classifiers = ['Random Forest', 'Logistic Regression', 'KNN', 'Naive Bayes', 'SimCLR based classifier']
x = list(range(len(training_data_sizes)))
width = 0.15  # Width of each bar
training_data_size_labels = ['10% of Data','40% of Data', '70% of Data', 'Complete Data']
plt.figure(figsize=(10, 6))
plt.bar(x, avg_accuracies_rf, width=width, label='Random Forest')
plt.bar([i + width for i in x], avg_accuracies_lr, width=width, label='Logistic Regression')
plt.bar([i + width * 2 for i in x], avg_accuracies_knn, width=width, label='KNN')
plt.bar([i + width * 3 for i in x], avg_accuracies_nb, width=width, label='Naive Bayes')
plt.bar([i + width * 4 for i in x], avg_accuracies_CL, width=width, label='SimCLR based classifier')

plt.xlabel('Classifiers')
plt.ylabel('Average Accuracy')
plt.title('Average Accuracies by Classifier and Training Data Size')
plt.xticks([i + 2 * width for i in x], training_data_size_labels)
plt.legend(loc ='lower right')
plt.tight_layout()

# Add grid lines and set background color
plt.grid(axis='y', linestyle='-', alpha=0.7)
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(x, avg_recalls_rf, width=width, label='Random Forest')
plt.bar([i + width for i in x], avg_recalls_lr, width=width, label='Logistic Regression')
plt.bar([i + width * 2 for i in x], avg_recalls_knn, width=width, label='KNN')
plt.bar([i + width * 3 for i in x], avg_recalls_nb, width=width, label='Naive Bayes')
plt.bar([i + width * 4 for i in x], avg_recalls_CL, width=width, label='SimCLR based classifier')

plt.xlabel('Classifiers')
plt.ylabel('Average Recall')
plt.title('Average Recalls by Classifier and Training Data Size')
plt.xticks([i + 2 * width for i in x], training_data_size_labels)
plt.legend(loc ='lower right')
plt.tight_layout()

# Add grid lines and set background color
plt.grid(axis='y', linestyle='-', alpha=0.7)
plt.show()