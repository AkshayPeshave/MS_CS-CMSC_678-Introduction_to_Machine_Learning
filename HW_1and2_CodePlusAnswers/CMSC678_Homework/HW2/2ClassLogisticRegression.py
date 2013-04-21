'''
Created on Mar 5, 2013

@author: akshaypeshave
'''

from string import *
import decimal
import math

class logisticRegression_2Class:
    def __init__(self, trainingDataFile, testDataFile, numberOfFeatures):
        self.number_of_features=numberOfFeatures
        self.trainingDataFile = trainingDataFile
        self.testDataFile = testDataFile
        
        #initialize weight vector
        self.weightVector = []
            
        for index in range(0, self.number_of_features):
            self.weightVector.append(0.0)
        
        
    def VectorDotProduct(self, w, x):
        dotProduct = 0.0
        for component in range(0,len(w)):
            dotProduct += float(w[component]) * float(x[component])
        
        return dotProduct

    def VectorSum(self, vector1, vector2):
        vectorSum = []
        
        for component in range(0,len(vector1)):
            vectorSum.append(float(vector1[component]) + (0.01* float(vector2[component])))
        
        return vectorSum
        
    def LearnWeightVector(self):        
        for i in range(0,5000):
            #initialize gradient vector
            gradientVector=[]
            for index in range(0, self.number_of_features):
                gradientVector.append(0.0)
            
            #iterate over all samples from training set
            trainingDataSet=open(self.trainingDataFile)
            trainingInstance = split(str(trainingDataSet.readline()).rstrip(),',')

            while trainingInstance[0] != '' :
                w_dot_instance=self.VectorDotProduct(self.weightVector,trainingInstance)
                
                class1_instance_probability= 1/(1 + decimal.Decimal(-w_dot_instance).exp())
                class1_instance_probability=float(class1_instance_probability)
                instance_error = float(trainingInstance[self.number_of_features]) - class1_instance_probability
                
                for vectorComponent in range(0,self.number_of_features):
                    gradientVector[vectorComponent] += (instance_error * float(trainingInstance[vectorComponent]))
                
                trainingInstance = split(str(trainingDataSet.readline()).rstrip(),',')

            trainingDataSet.close()
            self.weightVector=self.VectorSum(self.weightVector, gradientVector)
            
        print 'Weight Vector = ' + str(self.weightVector)
        
    def TestWeightVector(self):
        testDataSet=open(self.testDataFile)
        
        testInstance=split(str(testDataSet.readline()).rstrip(),',')
        
        totalTestInstances=0
        totalIncorrectPredictions=0
        
        while testInstance[0] != '' :
            totalTestInstances+=1
            w_dot_instance = self.VectorDotProduct(self.weightVector, testInstance)
            
            if w_dot_instance > 0 and testInstance[self.number_of_features]=='0':
                totalIncorrectPredictions+=1
            elif w_dot_instance < 0 and testInstance[self.number_of_features]=='1':
                totalIncorrectPredictions+=1
            
            testInstance=split(str(testDataSet.readline()).rstrip(),',')
                
        print 'Test Instances \t: '+str(totalTestInstances)
        print 'Correct Predictions\t: '+str(totalTestInstances-totalIncorrectPredictions)
        print 'Accuracy \t\t: ' + str((float(totalTestInstances)-totalIncorrectPredictions)*100/totalTestInstances)
        

classifier=logisticRegression_2Class('training', 'test', 30)
#classifier=logisticRegression_2Class('cmc_training.data', 'cmc_test.data', 9)
classifier.LearnWeightVector()
classifier.TestWeightVector()
        
            
