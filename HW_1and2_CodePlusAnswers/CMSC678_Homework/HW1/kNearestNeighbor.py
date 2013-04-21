from string import split
import random
from random import randrange
class kNearestNeighbor:
    def __init__(self, trainingDataFile, testDataFile):
        self.featureSet={1:['vhigh','high','med','low'],
                           2:['vhigh','high','med','low'],
                           3:['2','3','4','5more'],
                           4:['2','4','more'],
                           5:['small','med','big'],
                           6:['low','med','high']}
        self.classLabels=['unacc','acc','good','vgood']
        self.trainingDataFile = trainingDataFile
        self.testDataFile = testDataFile
    
    def ComputeDistance(self, trainingInstance, testInstance):
        trainingInstanceFeatures = split(str(trainingInstance).rstrip(),',')
        testInstanceFeatures = split(str(testInstance).rstrip(),',')
        distance=0
        
        for feature in range(0,len(self.featureSet)):
            if(trainingInstanceFeatures[feature]!=testInstanceFeatures[feature]):
                distance += 1
        
        return [distance,trainingInstanceFeatures[len(self.featureSet)]]
    
    def InitialiseDistanceMatrix(self):
        matrix={}
        for distance in range(0,len(self.featureSet)+1):
            matrix[distance]={classLabel : 0 for classLabel in self.classLabels}
        return matrix
        
    def TestKNearestGroup(self,k):
        trainingDataSet = open(self.trainingDataFile)
        testDataSet = open(self.testDataFile)
        
        testInstance = testDataSet.readline()
        
        accuracyMatrix={'totalTestInstances':0,
                        'correctPredictions':0,
                        'incorrectPredictions':0}
        
        while(testInstance != ''):
            trainingDataSet.seek(0)
            trainingInstance = trainingDataSet.readline()
            
            distanceMatrix = self.InitialiseDistanceMatrix()
            distanceCumulation = [0,0,0,0,0,0,0]
            
            while(trainingInstance != ''):
                [distance,classLabel] = self.ComputeDistance(trainingInstance, testInstance)
                distanceMatrix[distance][classLabel] += 1
                distanceCumulation[distance]+=1
                trainingInstance = trainingDataSet.readline()
            
            #find the majority class label amongst k-nearest neighbors
            kNNMatrix={classLabel:0 for classLabel in self.classLabels}
            
            kCount=k
            for distance in range(0,len(distanceCumulation)):
                if(kCount>0):
                    if(distanceCumulation[distance]!=0):
                        kCount-=1
                        for classLabel in self.classLabels:
                            kNNMatrix[classLabel]+=float(distanceMatrix[distance][classLabel]) * (1/(float(distance)+1))
            
            argmax={'classLabel':'x','posterior':0}
            for classLabel in self.classLabels:
                if(argmax['posterior']<kNNMatrix[classLabel]):
                    argmax['classLabel']=classLabel
                    argmax['posterior']=kNNMatrix[classLabel]
            
            print 'predicted -> '+str(argmax)+' , Actual -> '+ split(testInstance.rstrip(),',')[len(self.featureSet)]
            
            
            #update accuracy matrix
            accuracyMatrix['totalTestInstances'] += 1
            
            if(argmax['classLabel'] == split(testInstance.rstrip(),',')[len(self.featureSet)]):                                                            
                accuracyMatrix['correctPredictions'] += 1
            else:
                accuracyMatrix['incorrectPredictions'] += 1
            
            testInstance = testDataSet.readline()
            
        print '\n\nACCURACY MATRIX : \n' + str(accuracyMatrix) + '\nAccuracy: ' + str((float(accuracyMatrix['correctPredictions'])/accuracyMatrix['totalTestInstances']) * 100)

            
    def TestKNearestNeighbor(self,k, testTrainingSet):
        trainingDataSet = open(self.trainingDataFile)
        testDataSet = open(self.testDataFile)
        
        testInstance = testDataSet.readline()
        
        accuracyMatrix={'totalTestInstances':0,
                        'correctPredictions':0,
                        'incorrectPredictions':0}
        
        while(testInstance != ''):
            trainingDataSet.seek(0)
            trainingInstance = trainingDataSet.readline()
            
            distanceMatrix = self.InitialiseDistanceMatrix()
            distanceCumulation = [0,0,0,0,0,0,0]
            
            leaveInstance=testTrainingSet
            while(trainingInstance != ''):
                if(trainingInstance==testInstance and leaveInstance==1):
                    leaveInstance=0
                else:
                    [distance,classLabel] = self.ComputeDistance(trainingInstance, testInstance)
                    distanceMatrix[distance][classLabel] += 1
                    distanceCumulation[distance]+=1
                trainingInstance = trainingDataSet.readline()
            
            #find the majority class label amongst k-nearest neighbors
            kNNMatrix={classLabel:0 for classLabel in self.classLabels}
            
            kCount=k
            
            for distance in range(0,len(distanceCumulation)):
                if(kCount>0):
                    if(distanceCumulation[distance]!=0):
                        if(distanceCumulation[distance]<=kCount):
                            kCount-=distanceCumulation[distance]
                            for classLabel in self.classLabels:
                                kNNMatrix[classLabel]+=float(distanceMatrix[distance][classLabel]) * (1/(distance+1)) #float(k)-kCount
                        else:
                            classLabelList=[]
                            for classLabel in self.classLabels:
                                for i in range(0,distanceMatrix[distance][classLabel]):
                                    classLabelList.append(classLabel)
                             
                            addList=random.sample(classLabelList,kCount)       
                            
                                
                            while(kCount>0):
                                kCount-=1
                                kNNMatrix[addList[kCount]]+=(1/(float(distance)+1)) 
                            
            
            argmax={'classLabel':'x','posterior':0}
            for classLabel in self.classLabels:
                if(argmax['posterior']<kNNMatrix[classLabel]):
                    argmax['classLabel']=classLabel
                    argmax['posterior']=kNNMatrix[classLabel]
            
            #print 'predicted -> '+str(argmax)+' , Actual -> '+ split(testInstance.rstrip(),',')[len(self.featureSet)]
            
            
            #update accuracy matrix
            accuracyMatrix['totalTestInstances'] += 1
            
            if(argmax['classLabel'] == split(testInstance.rstrip(),',')[len(self.featureSet)]):                                                            
                accuracyMatrix['correctPredictions'] += 1
            else:
                accuracyMatrix['incorrectPredictions'] += 1
            
            testInstance = testDataSet.readline()
            
        print '\n\nACCURACY MATRIX : k='+ str(k) +'\n' + str(accuracyMatrix) + '\nAccuracy: ' + str((float(accuracyMatrix['correctPredictions'])/accuracyMatrix['totalTestInstances']) * 100)
        
classifier = kNearestNeighbor('carTraining.data','carTesting.data')
for k in range(1,21):
    classifier.TestKNearestNeighbor(k,0)           