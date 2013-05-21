import random
from random import randint
class ValueIteration:
    def __init__(self):
        self.Actions=['N','S','E','W']
        self.gamma=0.9
        self.epsilon=1.0
        self.learningRate = 0.1
        self.gridWorld=[[0.0 for row in range(0,15)] for column in range(0,15)]
#        for row in range(1,15):
#            for column in range(1,15):
#                self.gridWorld[row][column]=0
                
        self.maxEpisodes=100
        
    def SelectEpsilonGreeyNeighbor(self, row, column):
        maxQ=-99999.99;
        maxQMove=[]
        possibleMoves=[]
        
        if row>0:
            possibleMoves.append('N')
            if maxQ<self.gridWorld[row-1][column]:
                maxQ=self.gridWorld[row-1][column]
                maxQMove=['N']
            elif maxQ==self.gridWorld[row-1][column]:
                maxQMove.append('N')
                
        if row<14:
            possibleMoves.append('S')
            if maxQ<self.gridWorld[row+1][column]:
                maxQ=self.gridWorld[row+1][column]
                maxQMove=['S']
            elif maxQ==self.gridWorld[row+1][column]:
                maxQMove.append('S')
        
        if column>0:
            possibleMoves.append('W')
            if maxQ<self.gridWorld[row][column-1]:
                maxQ=self.gridWorld[row][column-1]
                maxQMove=['W']
            elif maxQ==self.gridWorld[row][column-1]:
                maxQMove.append('W')
                
        if column<14:
            possibleMoves.append('E')
            if maxQ<self.gridWorld[row][column+1]:
                maxQ=self.gridWorld[row][column+1]
                maxQMove=['E']
            elif maxQ==self.gridWorld[row][column+1]:
                maxQMove.append('E')
                
        explorationProbability=random.randint(1,10)
        if explorationProbability/10.0 > self.epsilon:
            for move in maxQMove:
                possibleMoves.remove(move)
                
            if possibleMoves==[]:
                return [random.choice(maxQMove),maxQ]
            
            randomMove=random.choice(possibleMoves)
            
            if randomMove=='N':
                QVal=self.gridWorld[row-1][column]
            elif randomMove=='S':
                QVal=self.gridWorld[row+1][column]
            elif randomMove=='E':
                QVal=self.gridWorld[row][column+1]
            else:
                QVal=self.gridWorld[row][column-1]
            return [randomMove,QVal]
        
        return [random.choice(maxQMove),maxQ]
        #return [maxQMove[0],maxQ]
                        
                        
    def EpsilonGreedyLearn(self):
        episode=1
        while episode<=self.maxEpisodes:
            row=1
            column=1
            steps=0
            while True:
                nextState = self.SelectEpsilonGreeyNeighbor(row,column)
                                
                steps+=1
                
                if nextState[0]=='N':
                    newRow= row-1
                    newColumn=column
                elif nextState[0]=='S':
                    newRow=row+1
                    newColumn=column
                elif nextState[0]=='E':
                    newColumn=column+1
                    newRow=row
                else:
                    newColumn=column-1
                    newRow=row
                
                    
                if newRow<0:
#                    row+=1
                    self.gridWorld[row][column] = self.gridWorld[row][column] + self.learningRate * -1
#                    continue
                elif newRow>14:
#                    row-=1
                    self.gridWorld[row][column] = self.gridWorld[row][column] + self.learningRate * -1
#                    continue
                
                elif newColumn<0:
#                    column+=1
                    self.gridWorld[row][column] = self.gridWorld[row][column] + self.learningRate * -1
#                    continue
                elif newColumn>14:
#                    column-=1
                    self.gridWorld[row][column] = self.gridWorld[row][column] + self.learningRate * -1
#                    continue
                else:  
                    if newRow == 14 and newColumn==14:
                        self.gridWorld[row][column] = self.gridWorld[row][column] + self.learningRate * (10 - self.gridWorld[row][column])
                        break
                    
                    futureMove=self.SelectEpsilonGreeyNeighbor(newRow,newColumn)
                    
                    self.gridWorld[row][column] = self.gridWorld[row][column] + self.learningRate * (-1 + (self.gamma*futureMove[1]) - self.gridWorld[row][column])
                    row=newRow
                    column=newColumn
            print steps
#            print self.gridWorld
            episode+=1

learner=ValueIteration()
learner.EpsilonGreedyLearn()
print learner.gridWorld