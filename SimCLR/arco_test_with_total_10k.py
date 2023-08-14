# -*- coding: utf-8 -*-
"""Arco-test-version 2 without timestamp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wm_tJtfv7jY3EyHc7lwPpQqiCXdjt-lF
"""

import pandas as pd
import zipfile
import glob
import numpy as np
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

!pip install psutil
!pip install codecarbon
import psutil
from codecarbon import EmissionsTracker

# Get the initial memory usage before loading the dataset
memory_before=psutil.virtual_memory().used

# Initialize the emissions tracker for tracking carbon emissions
emissions_tracker=EmissionsTracker()
emissions_tracker.start()

# Load and preprocess the sensor data
def load_and_preprocess_data():
    zip_path = 'fall-dataset-all.zip'

    # Extract the CSV files from the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        csv_files = [file for file in zip_ref.namelist() if file.endswith('.csv')]
        zip_ref.extractall(members=csv_files)

    # Read and concatenate the extracted CSV files into a DataFrame
    data = pd.concat([pd.read_csv(file, encoding='latin-1') for file in csv_files], ignore_index=True)
    accelerometer_data = data[["Acc(X)", "Acc(Y)", "Acc(Z)", "Rot(X)", "Rot(Y)", "Rot(Z)", "Pitch", "Roll", "Yaw"]].values

    # Standardize the data
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(accelerometer_data)

    return standardized_data

# Define the augmentation function
def augment_function(sample):
    augmented_sample = apply_augmentation(sample)
    return augmented_sample

# Define augmentation functions
def apply_augmentation(sample):
    augmented_sample = sample.copy()

    # Noise Injection
    noise = np.random.normal(loc=0, scale=0.1, size=augmented_sample.shape)
    augmented_sample += noise

    # Time Shifting
    shift_amount = np.random.randint(low=1, high=len(augmented_sample))
    augmented_sample = np.roll(augmented_sample, shift_amount, axis=0)

    # Magnitude Scaling
    scaling_factor = np.random.uniform(low=0.8, high=1.2)
    augmented_sample *= scaling_factor

    return augmented_sample

# Define dataset class for accelerometer data
class AccelerometerDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        sample = self.data[index]
        augmented_sample_1 = augment_function(sample)
        augmented_sample_2 = augment_function(sample)
        return augmented_sample_1, augmented_sample_2

    def __len__(self):
        return len(self.data)

# Load and preprocess sensor data
data = load_and_preprocess_data()

# Create the dataset
dataset = AccelerometerDataset(data)

# Create the data loader
batch_size = 64
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Define the SimCLR model architecture
class SimCLRModel(nn.Module):
    def __init__(self, num_steps):
        super(SimCLRModel, self).__init__()
        self.embedding_size = 128
        self.num_steps = num_steps

        self.backbone = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.fc = nn.Linear(128 * (num_steps // 4), self.embedding_size)

    def forward(self, x):
        x = self.backbone(x)
        x = x.view(x.size(0), -1)
        embedding = self.fc(x)
        return embedding

# Define the contrastive loss function
class ContrastiveLoss(nn.Module):
    def __init__(self, temperature=1.0):
        super(ContrastiveLoss, self).__init__()
        self.temperature = temperature

    def forward(self, embeddings_1, embeddings_2):
        # Normalize the embeddings
        embeddings_1 = nn.functional.normalize(embeddings_1, dim=1)
        embeddings_2 = nn.functional.normalize(embeddings_2, dim=1)

        # Calculate cosine similarity between the embeddings
        similarities = torch.matmul(embeddings_1, embeddings_2.T) / self.temperature

        # Generate target labels (1 for positive pairs, 0 for negative pairs)
        labels = torch.arange(embeddings_1.size(0)).to(embeddings_1.device)

        # Calculate contrastive loss
        loss = nn.CrossEntropyLoss()(similarities, labels)

        return loss

# Initialize the SimCLR model, contrastive loss, and optimizer
num_steps = dataset[0][0].shape[0]
model = SimCLRModel(num_steps).double()
criterion = ContrastiveLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(num_epochs):
    for batch in data_loader:
        # Clear the gradients
        optimizer.zero_grad()

        # Get the batch of augmented samples
        augmented_samples_1, augmented_samples_2 = batch

        # Reshape the input data to include the num_channels dimension
        augmented_samples_1 = augmented_samples_1.unsqueeze(1)
        augmented_samples_2 = augmented_samples_2.unsqueeze(1)

        # Forward pass
        embeddings_1 = model(augmented_samples_1.to(device).double())
        embeddings_2 = model(augmented_samples_2.to(device).double())

        # Calculate the contrastive loss
        loss = criterion(embeddings_1, embeddings_2)

        # Backward pass
        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}")

# Save the trained SimCLR model
torch.save(model.state_dict(), 'simclr_model.pth')

# Define the fall detection model
class FallDetectionModel(nn.Module):
    def __init__(self, input_size, num_classes):
        super(FallDetectionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, num_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# Specify the number of classes for fall detection
num_classes = 2

# Create an instance of the fall detection model
fall_model = FallDetectionModel(input_size=128, num_classes=num_classes)

# Define the fall detection loss function
fall_loss_function = nn.CrossEntropyLoss()

# Define the fall detection optimizer
fall_optimizer = optim.SGD(fall_model.parameters(), lr=0.001)

# Load the saved SimCLR model and extract learned embeddings
simclr_model = SimCLRModel(num_steps)
simclr_model.load_state_dict(torch.load('simclr_model.pth'))
simclr_model.eval()

# Load and preprocess the sensor data
def load_and_preprocess(zip_path):
    # Extract the CSV files from the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        csv_files = [file for file in zip_ref.namelist() if file.endswith('.csv')]
        zip_ref.extractall(members=csv_files)

    # Read and concatenate the extracted CSV files into a DataFrame
    data = pd.concat([pd.read_csv(file, encoding='latin-1') for file in csv_files], ignore_index=True)

    #Separate features and labels
    accelerometer_data = data[["Acc(X)", "Acc(Y)", "Acc(Z)", "Rot(X)", "Rot(Y)", "Rot(Z)", "Pitch", "Roll", "Yaw"]].values
    labels = list(data["Fall"])

    # Standardize the data
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(accelerometer_data)

    return standardized_data,labels

class AccelerometerDataset(torch.utils.data.Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __getitem__(self, index):
        sample = self.data[index]
        augmented_sample_1 = augment_function(sample)
        augmented_sample_2 = augment_function(sample)
        label = self.labels[index]  # Get the label for this sample
        return augmented_sample_1, augmented_sample_2, label  # Return augmented samples and label

    def __len__(self):
        return len(self.data)

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

import random

# Load the fall-dataset-raw csv files
raw_files = "fall-dataset-raw.zip"
raw_data, labels = load_and_preprocess(raw_files)

# Combine raw_data and labels into a single array for easy shuffling
data_with_labels = np.column_stack((raw_data, labels))

# Split the data into training and testing sets with an 80:20 ratio
split = int(0.8 * len(data_with_labels))
train_data = data_with_labels[:split]
test_data = data_with_labels[split:]

num_training_points = 8000
num_testing_points = 2000

import matplotlib.pyplot as plt

# Setup for experiment with different training data sizes
training_data_sizes = np.arange(0.1, 1.1, 0.3)

def run(train_data, num_training_points):
    #Choose data points for training and testing
    train_raw_data, train_labels = chooseData(train_data, num_training_points)
    test_raw_data, test_labels = chooseData(test_data, num_testing_points)

    # Define the train and test datasets
    train_dataset = AccelerometerDataset(train_raw_data,train_labels)
    test_dataset = AccelerometerDataset(test_raw_data,test_labels)

    # Define the batch size
    batch_size = 64

    # Create the data loaders
    train_data_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_data_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    simclr_model.to(device)

    # Create lists to hold the embeddings and labels for each batch
    train_embeddings = []
    train_labels_list = []

    # Generate embeddings for training data using SimCLR model
    for batch in train_data_loader:

        augmented_samples_1, augmented_samples_2, labels = batch

        augmented_samples_1 = augmented_samples_1.unsqueeze(1).to(device)
        augmented_samples_2 = augmented_samples_2.unsqueeze(1).to(device)

        embeddings_1 = simclr_model(augmented_samples_1.to(device).float())
        embeddings_2 = simclr_model(augmented_samples_2.to(device).float())

        train_embeddings.append(embeddings_1)
        train_embeddings.append(embeddings_2)

        train_labels_list.extend(labels)
        train_labels_list.extend(labels)


    # Concatenate and convert to tensors
    train_embeddings = torch.cat(train_embeddings, dim=0)
    train_labels = np.array(train_labels_list)

    # Similar changes for test_data_loader and test_labels
    test_embeddings = []
    test_labels_list = []  # New list to store labels
    for batch in test_data_loader:
        augmented_samples_1, augmented_samples_2, t_labels = batch
        augmented_samples_1 = augmented_samples_1.unsqueeze(1).to(device)
        augmented_samples_2 = augmented_samples_2.unsqueeze(1).to(device)
        embeddings_1 = simclr_model(augmented_samples_1.to(device).float())
        embeddings_2 = simclr_model(augmented_samples_2.to(device).float())
        test_embeddings.append(embeddings_1)
        test_embeddings.append(embeddings_2)

        test_labels_list.extend(t_labels)
        test_labels_list.extend(t_labels)

    # Concatenate the embeddings and labels lists into tensors
    test_embeddings = torch.cat(test_embeddings, dim=0)
    test_labels = np.array(test_labels_list)

    train_labels = torch.tensor(train_labels)
    test_labels = torch.tensor(test_labels)

    # Move the fall detection model to the same device as the embeddings
    global fall_model
    fall_model = fall_model.to(device)

    # Training loop for the fall detection model
    num_epochs = 10

    for epoch in range(num_epochs):
        fall_model.train()
        total_loss = 0.0  # Track the total loss for the epoch

        for i in range(len(train_embeddings)):
            # Get the embeddings and labels for the current batch
            embeddings = train_embeddings[i].unsqueeze(0)
            labels = train_labels[i].unsqueeze(0)

            # Move embeddings and labels to the same device as the model
            embeddings = embeddings.to(device)
            labels = labels.to(device)

            # Convert the inputs and labels to torch.float32
            embeddings = embeddings.float()
            labels = labels.float()

            # Forward pass through the fall detection model
            outputs = fall_model(embeddings)

            # Calculate the fall detection loss
            fall_loss = fall_loss_function(outputs, labels.to(torch.int64))
            total_loss += fall_loss.item()

            # Zero the gradients
            fall_optimizer.zero_grad()

            # Backward pass and optimization
            fall_loss.backward(retain_graph=True)
            fall_optimizer.step()

        # Calculate the average loss for the epoch
        avg_loss = total_loss / len(train_embeddings)
        print(f"Epoch [{epoch+1}/{num_epochs}], Fall Detection Loss: {avg_loss}")


    # Evaluation phase after all epochs are completed
    fall_model.eval()
    with torch.no_grad():
        total_correct = 0
        total_samples = 0
        true_positives = 0
        actual_positives = 0

        for i in range(len(test_embeddings)):
            # Get the embeddings and labels for the current batch
            embeddings = test_embeddings[i].unsqueeze(0)
            labels = test_labels[i].unsqueeze(0)

            # Move embeddings and labels to the same device as the model
            embeddings = embeddings.to(device)
            labels = labels.to(device)

            # Convert the inputs and labels to torch.float32
            embeddings = embeddings.float()
            labels = labels.float()

            # Forward pass through the fall detection model
            outputs = fall_model(embeddings)

            # Calculate accuracy for this batch
            predicted = torch.argmax(outputs, 1)
            total_correct += (predicted == labels).sum().item()
            total_samples += labels.size(0)

            # Calculate recall for this batch
            for j in range(labels.size(0)):
                if labels[j] == 1:  # Positive class
                    actual_positives += 1
                    if predicted[j] == 1:
                        true_positives += 1

        accuracy = total_correct / total_samples
        recall = true_positives / actual_positives if actual_positives > 0 else 0
        print(f"Test Accuracy: {accuracy:.4f}")
        print(f"Test Recall: {recall:.4f}")
        return accuracy, recall

#Lists to hold average accuracies and average recalls for different training data sizes
avg_accuracies=[]
avg_recalls=[]
for size in training_data_sizes:
  num_samples = int(num_training_points * size)
  print("Training data size : " + str(num_samples))
  accuracy_sum = 0
  recall_sum = 0
  for i in range(3):
      print("Test Run - " + str(i+1))
      acc, recall = run(train_data, num_samples)
      accuracy_sum+=acc
      recall_sum+=recall
  #Calculate average accuracy and average recall over the three iterations
  avg_accuracy = accuracy_sum/3
  avg_recall = recall_sum/3
  #Append to list
  avg_accuracies.append(avg_accuracy)
  avg_recalls.append(avg_recall)
  print("Average accuracy obtained across the three runs - " + str(avg_accuracy))
  print("Average recall obtained across the three runs - " + str(avg_recall))

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(training_data_sizes, avg_accuracies, label='Accuracy')
plt.plot(training_data_sizes, avg_recalls, label='Recall')
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