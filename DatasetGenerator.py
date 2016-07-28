"""
    Code for generating Dataset for Classification Problem using Logistic Regression
    Author: Shalin Chopra
"""
from sklearn.datasets import make_classification
import os

#Change the number of samples (n_samples) parameter according to canary (1 Billion or Dataset size of 160 GB)
x,y = make_classification(n_samples=100,n_features=20,n_repeated=0, n_classes=2)

# Write the data generated to a file
# change the path accordingly, where to Save the Dataset
with open("G:/datasetGenerated.data",mode='w') as fp:
    for idx, sample in enumerate(x):
        for ele in sample:
            fp.write(str(ele)+",")
        fp.write(str(y[idx])+"\n")

print("File size: ",os.stat("datasetGenerated.data").st_size)