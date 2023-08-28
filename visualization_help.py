# -*- coding: utf-8 -*-
"""Visualization_Help.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZWGRTNiYZ1IDhv0lYfdzGl2Jvtmibgza
"""

import pandas as pd
data =pd.read_csv('raw182_Training_Relabeled_Auto_25.csv', encoding='latin-1')

data

from collections import Counter

d= Counter(data['outcome'])

d

import matplotlib.pyplot as plt

plt.bar(d.keys(), d.values())

plt.show()

"""**Dataset: MSBAND SmartFall**"""

#Table of performance values
import pandas as pd
it1_acc=[0.8712,  0.8832, 0.8830, 0.8958]
it1_rec=[0.1154, 0.1102, 0.1989, 0.3197]
it2_acc=[0.8702, 0.8740, 0.8910, 0.8845]
it2_rec=[0.2070, 0.1620, 0.2752, 0.2364]
it3_acc=[0.8785, 0.8785, 0.8905, 0.8828]
it3_rec=[0.1023, 0.1304, 0.2960, 0.1629]
avg_acc=[0.8733333333333332, 0.8785833333333333, 0.8881666666666667, 0.8876666666666667]
avg_rec=[0.14155829550566393, 0.13419172736950905, 0.2566781463889553, 0.23967183287880098]

data = {
    'Training Data Size': [800, 3200, 5600, 8000],
    'Iteration 1 Accuracy': it1_acc,
    'Iteration 1 Recall': it1_rec,
    'Iteration 2 Accuracy': it2_acc,
    'Iteration 2 Recall': it2_rec,
    'Iteration 3 Accuracy': it3_acc,
    'Iteration 3 Recall': it3_rec,
    'Average Accuracy': avg_acc,
    'Average Recall': avg_rec
}

df = pd.DataFrame(data)

df

import matplotlib.pyplot as plt
training_data_size = [800,3200,5600,8000]
# Line graph of Accuracies over Different Training Data Sizes
plt.figure(figsize=(10, 6))
plt.plot(training_data_size, it1_acc, marker='o', label='Iteration 1')
plt.plot(training_data_size, it2_acc, marker='o', label='Iteration 2')
plt.plot(training_data_size, it3_acc, marker='o', label='Iteration 3')
plt.plot(training_data_size, avg_acc, marker='o', label='Average Accuracy')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Training Data Size vs Accuracies')
plt.xticks(training_data_size)
plt.legend()
plt.grid(True)
plt.show()

# Line graph of Recalls over Different Training Data Sizes
plt.figure(figsize=(10, 6))
plt.plot(training_data_size, it1_rec, marker='o', label='Iteration 1')
plt.plot(training_data_size, it2_rec, marker='o', label='Iteration 2')
plt.plot(training_data_size, it3_rec, marker='o', label='Iteration 3')
plt.plot(training_data_size, avg_rec, marker='o', label='Average Recall')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Training Data Size vs Recalls')
plt.xticks(training_data_size)
plt.legend()
plt.grid(True)
plt.show()

"""**Dataset: Fall Detection Dataset by ARCO**"""

#Table of performance values
import pandas as pd
it1_acc=[0.8375, 0.8645, 0.8695, 0.8655 ]

it1_rec=[0.8579, 0.8764, 0.8673, 0.8562 ]
it2_acc=[0.8592, 0.8712, 0.8775, 0.8745 ]
it2_rec=[0.8819, 0.8864, 0.8959, 0.8935]
it3_acc=[0.8822, 0.8628, 0.8678, 0.8745 ]
it3_rec=[0.9098, 0.9197, 0.8956, 0.8806]

avg_acc=[0.8596666666666666, 0.8661666666666666, 0.8715833333333333, 0.8715000000000002]
avg_rec=[0.8831807234077073, 0.8941910102626883, 0.8862835070276232, 0.876756004183349]

data = {
    'Training Data Size': [800, 3200, 5600, 8000],
    'Iteration 1 Accuracy': it1_acc,
    'Iteration 1 Recall': it1_rec,
    'Iteration 2 Accuracy': it2_acc,
    'Iteration 2 Recall': it2_rec,
    'Iteration 3 Accuracy': it3_acc,
    'Iteration 3 Recall': it3_rec,
    'Average Accuracy': avg_acc,
    'Average Recall': avg_rec
}

df = pd.DataFrame(data)

df

import matplotlib.pyplot as plt
training_data_size = [800,3200,5600,8000]
# Line graph of Accuracies over Different Training Data Sizes
plt.figure(figsize=(10, 6))
plt.plot(training_data_size, it1_acc, marker='o', label='Iteration 1')
plt.plot(training_data_size, it2_acc, marker='o', label='Iteration 2')
plt.plot(training_data_size, it3_acc, marker='o', label='Iteration 3')
plt.plot(training_data_size, avg_acc, marker='o', label='Average Accuracy')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Training Data Size vs Accuracies')
plt.xticks(training_data_size)
plt.legend()
plt.grid(True)
plt.show()

# Line graph of Recalls over Different Training Data Sizes
plt.figure(figsize=(10, 6))
plt.plot(training_data_size, it1_rec, marker='o', label='Iteration 1')
plt.plot(training_data_size, it2_rec, marker='o', label='Iteration 2')
plt.plot(training_data_size, it3_rec, marker='o', label='Iteration 3')
plt.plot(training_data_size, avg_rec, marker='o', label='Average Recall')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Training Data Size vs Recalls')
plt.xticks(training_data_size)
plt.legend()
plt.grid(True)
plt.show()

"""**Dataset: SisFall**"""

#Table of performance values
import pandas as pd
it1_acc=[0.5685, 0.5202, 0.4288, 0.5432 ]

it1_rec=[0.0, 0.0, 0.0, 0.0 ]
it2_acc=[0.3995,0.4945, 0.5823, 0.6962 ]
it2_rec=[0.0, 0.0, 0.0, 0.0 ]
it3_acc=[0.5565,0.6418, 0.6544, 0.6308 ]
it3_rec=[0.0, 0.0, 0.0, 0.0 ]

avg_acc=[0.50816667, 0.55216667, 0.55516667, 0.6234]
avg_rec=[0.0, 0.0, 0.0, 0.0 ]



data = {
    'Training Data Size': [800, 3200, 5600, 8000],
    'Iteration 1 Accuracy': it1_acc,
    'Iteration 1 Recall': it1_rec,
    'Iteration 2 Accuracy': it2_acc,
    'Iteration 2 Recall': it2_rec,
    'Iteration 3 Accuracy': it3_acc,
    'Iteration 3 Recall': it3_rec,
    'Average Accuracy': avg_acc,
    'Average Recall': avg_rec
}

df = pd.DataFrame(data)

df

import matplotlib.pyplot as plt
training_data_size = [800,3200,5600,8000]
# Line graph of Accuracies over Different Training Data Sizes
plt.figure(figsize=(10, 6))
plt.plot(training_data_size, it1_acc, marker='o', label='Iteration 1')
plt.plot(training_data_size, it2_acc, marker='o', label='Iteration 2')
plt.plot(training_data_size, it3_acc, marker='o', label='Iteration 3')
plt.plot(training_data_size, avg_acc, marker='o', label='Average Accuracy')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Training Data Size vs Accuracies')
plt.xticks(training_data_size)
plt.legend()
plt.grid(True)
plt.show()

# Line graph of Recalls over Different Training Data Sizes
plt.figure(figsize=(10, 6))
plt.plot(training_data_size, it1_rec, marker='o', label='Iteration 1')
plt.plot(training_data_size, it2_rec, marker='o', label='Iteration 2')
plt.plot(training_data_size, it3_rec, marker='o', label='Iteration 3')
plt.plot(training_data_size, avg_rec, marker='o', label='Average Recall')
plt.xlabel('Training Data Size')
plt.ylabel('Score')
plt.title('Training Data Size vs Recalls')
plt.xticks(training_data_size)
plt.legend()
plt.grid(True)
plt.show()

"""**Comparison Across Datasets**"""

#Table of performance values across the three datasets
import pandas as pd
avg_acc_smart=[0.8733333333333332, 0.8785833333333333, 0.8881666666666667, 0.8876666666666667]
avg_rec_smart=[0.14155829550566393, 0.13419172736950905, 0.2566781463889553, 0.23967183287880098]
avg_acc_arco=[0.8596666666666666, 0.8661666666666666, 0.8715833333333333, 0.8715000000000002]
avg_rec_arco=[0.8831807234077073, 0.8941910102626883, 0.8862835070276232, 0.876756004183349]
avg_acc_sis=[0.50816667, 0.55216667, 0.55516667, 0.6234]
avg_rec_sis=[0.0, 0.0, 0.0, 0.0 ]

data = {
    'Training Data Size': [800, 3200, 5600, 8000],
    'MSBAND Dataset Accuracy': avg_acc_smart,
    'MSBAND Dataset Recall': avg_rec_smart,
    'ARCO Dataset Accuracy': avg_acc_arco,
    'ARCO Dataset Recall': avg_rec_arco,
    'Sisfall Dataset Accuracy': avg_acc_sis,
    'Sisfall Dataset Recall': avg_rec_sis
}

df = pd.DataFrame(data)

df

