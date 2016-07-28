#!/usr/bin/env python

# Author: Sami Ahmad Khan
# Course: CS 597 
# Laboratory: DataSys, Illinois Institute of Technology, Chicago, US
# Email: skhan75@hawk.iit.edu
# Description: Logistic Regression in Apache Spark using both SGD and LBGF Models

# API Documentation: http://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.mllib.classification.LogisticRegressionModel
# API Source Code: https://github.com/apache/spark/tree/master/mllib/src/main/scala/org/apache/spark/mllib/classification
# Also refer: https://spark.apache.org/docs/latest/ml-classification-regression.html





# First import packages and classes that we will need throughout
from pyspark import SparkContext, SparkConf
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.classification import LogisticRegressionWithSGD
import sys
from timeit import default_timer as timer
from time import time

global globalModel

# Getting locations for Input and Output directory from user
inputDir = ''
outputDir = ''
modelSelection = ''
cmdargs = str(sys.argv)
inputDir = str(sys.argv[1])
outputDir = str(sys.argv[2])
modelSelection = str(sys.argv[3])

# Load the data set into a Spark RDD
sc = SparkContext(appName="LogisticRegression")
data = sc.textFile(inputDir)

print data.count()

def line_parser(line):
    tokens = line.split(',')
    label = float(tokens[-1])
    features = map(lambda t: float(t), tokens[:-1])
    return LabeledPoint(label, features)

# Map the data set into a data set of `LabeledPoint`s
parsedData = data.map(line_parser)

# Split the data into training and test (we're missing the validation set)
trainingData, testData = parsedData.randomSplit([0.6, 0.4], seed = 11L)


# Train two logistic regression models with two different optimizers (LBFGS and SGD).
if modelSelection == 'lbfgs':
    start = timer()
    model1 = LogisticRegressionWithLBFGS.train(trainingData, iterations = 50, intercept = True, numClasses = 2)
    end = timer()
    elapsed = end - start
    gloabalModel = model1
    print '\nClassifier trained in ', elapsed,' seconds with LBFGS'
    
    # Evaluate the training and test errors
    trainingLabelAndPreds1 = trainingData.map(lambda point: (point.label, model1.predict(point.features)))

    #Test the accuracy of predicition and print the time taken
    start = timer()
    test_accuracy = trainingLabelAndPreds1.filter(lambda (v, p): v == p).count() / float(testData.count())
    end = timer()
    elapsed = end - start
    print '\nPrediction made in: ', elapsed, 'seconds with LBFGS'
    print '\nTest Accuracy is: ', round(test_accuracy,4)
    trainingError1 = trainingLabelAndPreds1.map(lambda (r1, r2): float(r1 != r2)).mean()
    print '\nLBFGS training error: ', trainingError1


elif modelSelection == 'sgd':
    start = timer()
    model2 = LogisticRegressionWithSGD.train(trainingData, iterations = 50, intercept = True)
    end = timer()
    elapsed = end - start
    globalModel = model2
    print '\nClassifier trained in ', elapsed, ' seconds with SGD'

    # Evaluate the training and test errors
    trainingLabelAndPreds2 = trainingData.map(lambda point: (point.label, model2.predict(point.features)))

    #Test the accuracy of predicition and print the time taken
    start = timer()
    test_accuracy = trainingLabelAndPreds2.filter(lambda (v, p): v == p).count() / float(testData.count())
    end = timer()
    elapsed = end - start
    print '\nPrediction made in: ', elapsed, 'seconds with SGD'
    print '\nTest Accuracy is: ', round(test_accuracy,4)
    trainingError2 = trainingLabelAndPreds2.map(lambda (r1, r2): float(r1 != r2)).mean()
    print '\nSGD training error: ', trainingError2, '\n'

# Save Model
globalModel.save(sc, outputDir)
print '\nOutput Saved Successfully at ', outputDir
