#import arff;
import random;

class arff_generator:
    
    def CreateNewArff(self, file_path, number_of_instances):
        ### relation => abstract_binary
        ### feature set => F1....F5
        ### classLabel => bitwise = (F1 | F2) && (F3 | (~F4 && F5))
        
        relation = "abstract_binary"
        attributes = ['F1','F2','F3','F4','F5']
        instance = []
        
        arff_file=open(file_path,'w')
        
        #define arff relation
        arff_file.write('@RELATION '+ relation + '\n\n\n')
        
        #define arff attributes
        #feature set first
        for att in attributes:
            arff_file.write('@ATTRIBUTE ' + att + ' {\'0\',\'1\'}\n')
        
        #now the class label
        arff_file.write('@ATTRIBUTE class {\'0\',\'1\'}\n\n\n')
        
        
        #write arff data
        arff_file.write('@DATA\n')
        while number_of_instances>0:
            instance=[]
            for i in range(0,5):
                instance.append(random.randint(0,1))
            classLabel = (instance[0] | instance[1]) & (instance[2] | (~instance[3] & instance[4]))
            arff_file.write(str(instance)[1:-1]+', '+str(classLabel)+'\n')
            number_of_instances-=1
            
    
    def CreateNewArffWithMissingValues(self, file_path, number_of_instances, missingValueFactor):
        ### relation => abstract_binary
        ### feature set => F1....F5
        ### classLabel => bitwise = (F1 | F2) && (F3 | (~F4 && F5))
        
        relation = "abstract_binary"
        attributes = ['F1','F2','F3','F4','F5']
        instance = []
        
        arff_file=open(file_path,'w')
        
        #define arff relation
        arff_file.write('@RELATION '+ relation + '\n\n\n')
        
        #define arff attributes
        #feature set first
        for att in attributes:
            arff_file.write('@ATTRIBUTE ' + att + ' {\'0\',\'1\'}\n')
        
        #now the class label
        arff_file.write('@ATTRIBUTE class {\'0\',\'1\'}\n\n\n')
        
        
        #write arff data
        arff_file.write('@DATA\n')
        while number_of_instances>0:
            instance=[]
            for i in range(0,5):
                instance.append(random.randint(0,1))
            classLabel = (instance[0] | instance[1]) & (instance[2] | (~instance[3] & instance[4]))
            
            #introducing missing values
            for i in range(0,5):
                if(random.randint(0,100) % missingValueFactor == 0):
                    instance[i] = '?'
            
            arff_file.write((str(instance)[1:-1]).replace('\'', '')+', '+str(classLabel)+'\n')
            number_of_instances-=1

    def CreateNewArffWithIrrelevantAttirbutes(self, file_path, number_of_instances, noOfIrrelevantAttributes):
        ### relation => abstract_binary
        ### feature set => F1....F5
        ### classLabel => bitwise = (F1 | F2) && (F3 | (~F4 && F5))
        
        relation = "abstract_binary"
        attributes = ['F1','F2','F3','F4','F5']
        for i in range(0, noOfIrrelevantAttributes):
            attributes.append('F'+str(5+i+1))
        instance = []
        
        arff_file=open(file_path,'w')
        
        #define arff relation
        arff_file.write('@RELATION '+ relation + '\n\n\n')
        
        #define arff attributes
        #feature set first
        for att in attributes:
            arff_file.write('@ATTRIBUTE ' + att + ' {\'0\',\'1\'}\n')
        
        #now the class label
        arff_file.write('@ATTRIBUTE class {\'0\',\'1\'}\n\n\n')
        
        
        #write arff data
        arff_file.write('@DATA\n')
        while number_of_instances>0:
            instance=[]
            for i in range(0,5+noOfIrrelevantAttributes):
                instance.append(random.randint(0,1))
            classLabel = (instance[0] | instance[1]) & (instance[2] | (~instance[3] & instance[4]))
            arff_file.write(str(instance)[1:-1]+', '+str(classLabel)+'\n')
            number_of_instances-=1
            

gen=arff_generator()
#gen.CreateNewArffWithMissingValues('selfGenMissingVal_1in30_1.arff',4,50)
gen.CreateNewArffWithIrrelevantAttirbutes('selfGen_irrelevanceTest_1.arff', 64, 1)
gen.CreateNewArffWithIrrelevantAttirbutes('selfGen_irrelevanceTest_2.arff', 64, 2)
gen.CreateNewArffWithIrrelevantAttirbutes('selfGen_irrelevanceTest_3.arff', 64, 3)
gen.CreateNewArffWithIrrelevantAttirbutes('selfGen_irrelevanceTest_4.arff', 64, 4)
gen.CreateNewArffWithIrrelevantAttirbutes('selfGen_irrelevanceTest_5.arff', 64, 5)
gen.CreateNewArffWithIrrelevantAttirbutes('selfGen_irrelevanceTest_6.arff', 64, 6)