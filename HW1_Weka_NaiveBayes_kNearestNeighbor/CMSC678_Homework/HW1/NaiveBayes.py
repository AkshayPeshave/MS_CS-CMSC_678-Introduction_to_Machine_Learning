from string import split

class NaiveBayes:
    
    def __init__(self):
        self.featureProbabilityMatrix={}
        
        self. featureSet={1:['vhigh','high','med','low'],
                           2:['vhigh','high','med','low'],
                           3:['2','3','4','5more'],
                           4:['2','4','more'],
                           5:['small','med','big'],
                           6:['low','med','high']}
        self.classLabels=['unacc','acc','good','vgood']
        for x in range(1, 7):
            self.featureProbabilityMatrix[x]={a:{b:0.0 for b in self.classLabels} for a in self.featureSet[x]}
            
        self.totalTrainingInstances=0
    
    
    def Train(self):                 
        self.classLabelsCount={x:0 for x in self.classLabels}
        
        dataSet=open('carTraining.data')
        instance = dataSet.readline()
    
        while(instance != ''):
            instance_features = split(instance.rstrip(),',')
            
            for feature in range(0,len(instance_features)-1):
                self.featureProbabilityMatrix[feature+1][str(instance_features[feature])][str(instance_features[len(self.featureSet)])]+=1
            self.classLabelsCount[str(instance_features[len(self.featureSet)])] += 1
            self.totalTrainingInstances+=1
            instance = dataSet.readline()
            
        print 'Total Training Instances: ' + str(self.totalTrainingInstances)
        print 'Class Label Distribution in Training Set: ' + str(self.classLabelsCount)
        print '\nFeatures-vs-Class Count Matrix:\n' + str(self.featureProbabilityMatrix)
        
        
    
    def Test(self):
        #calculate prior probability for all class labels
        priors={}
        for classLabel in iter(self.classLabelsCount):
            priors[classLabel]=(float(self.classLabelsCount[classLabel])+1)/(float(self.totalTrainingInstances)+len(self.classLabels))
        
        #initialize accuracy matrix    
        accuracyMatrix={'totalTestInstances':0,
                        'correctPredictions':0,
                        'incorrectPredictions':0}
        
        #output headers
        print '\nFeatures\t\t\t\tActual\tPredicted\tProbability\tPrior\t\tLikelihood\t\t\tEvidence'
        
        
        testDataSet=open('carTesting.data')
        testingInstance = testDataSet.readline()
        
        #predict for each test instance
        while(testingInstance!=''):
            testingInstanceFeatures=split(testingInstance.rstrip(),',')
            
            argmax={'classLabel':'x', 'posterior':0.0, 'prior':0.0, 'likelihood':0.0, 'evidence':0.0}
            evidence=0
                
            for classLabel in self.classLabels:
                likelihood=1
                for feature in range(0,len(self.featureSet)):
                    #calculate probabilities
                    likelihood *= (self.featureProbabilityMatrix[feature+1][testingInstanceFeatures[feature]][classLabel] + 1) / (self.classLabelsCount[classLabel] + len(self.featureSet[feature+1]))
            
                #update argmax if posterior probability for new class label exceeds that of the older class label
                if argmax['posterior'] < (priors[classLabel] * likelihood):
                    argmax['classLabel']=classLabel
                    argmax['posterior']=(priors[classLabel] * likelihood)
                    argmax['likelihood']=likelihood
                
                #cumulate the evidence probability for test instance
                evidence += (priors[classLabel] * likelihood)
            
            #re-caliberate posterior probability by considering evidence probability
            argmax['evidence'] = evidence
            argmax['posterior'] /= evidence
            print (str(testingInstanceFeatures[0:len(self.featureSet)-1])).replace('\'','') +'\t'+ testingInstanceFeatures[len(self.featureSet)] + '\t' + str(argmax['classLabel']) + '\t\t' + str(argmax['posterior']) +'\t' + str(priors[argmax['classLabel']]) +'\t' + str(argmax['likelihood']) +'\t' + str(argmax['evidence'])
            
            #update accuracy matrix
            accuracyMatrix['totalTestInstances'] += 1
            
            if(argmax['classLabel'] == testingInstanceFeatures[len(self.featureSet)]):                                                            
                accuracyMatrix['correctPredictions'] += 1
            else:
                accuracyMatrix['incorrectPredictions'] += 1
            
            testingInstance = testDataSet.readline()
                
        print '\n\nACCURACY MATRIX : \n' + str(accuracyMatrix)
        print '\nACCURACY: ' + str((float(accuracyMatrix['correctPredictions'])/accuracyMatrix['totalTestInstances']) * 100) + '%'
        
        

classifier=NaiveBayes()
classifier.Train()
classifier.Test()