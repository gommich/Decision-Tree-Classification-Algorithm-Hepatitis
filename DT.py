import pandas as pd
import sys
import random

from TreeNodes import Node, LeafNode
            
   

class DecisionTree():
    
    def __init__ (self,dataset,classes):
        self.dataset = dataset
        self.classes = classes
        self.baseline = self.baselinePred()
        
        
        
    #Get The Baseline Prediction
    def baselinePred(self):
        classA=self.classes[0]
        classB=self.classes[1]
       
        total_A=0
        total_B=0 
        total = len(self.dataset)
        
        for index, row in self.dataset.iterrows():
            
            if (row[0]==classA):
                total_A=total_A+1
            elif(row[0]==classB):
                total_B=total_B+1
        
        if (total_A>total_B):
            
            T=(classA,total_A/total)
            
            return T
        elif (total_A<total_B):
            T=(classB,total_B/total)
            
            return T
        
    
    
    #Get Weighted Average Purity
    def calcWeightedPurity(self, purity_true, purity_false, true_instances, false_instances):
        
         numtrue = len(true_instances)
         numfalse = len(false_instances)
         tot_true_false = numtrue+numfalse
         probtrue = numtrue/tot_true_false
         probfalse = numfalse/tot_true_false
         
         
         weighted_average_purity = (probtrue*purity_true)+(probfalse*purity_false)
         
         return weighted_average_purity
    
    #Calculates the purity of a node. 
    def calcPurity(self, instances):
        classA = self.classes[0]
        classB = self.classes[1]
        
        numinstances = len(instances)
        
        if (numinstances>0):
        
            total_A=0
            total_B=0
        
        
            for index, row in instances.iterrows():
                if (row[0]==classA):
                    total_A = total_B+1
                elif (row[0]==classB):
                    total_A = total_B+1
        
            
            gini = 2*(((total_A)/numinstances)*((total_B)/numinstances))
            return gini
        else:
            return 0
        
        
      
    # Return true if all instances
    # Have the same Class
    def countMajority(self, instances):
        classA = self.classes[0]
        classB = self.classes[1]
        
        classes = []
        numclasses = len(instances)
        total_A=0
        total_B=0
        for index, row in instances.iterrows():
            classes.append(row[0])
            
        for c in classes:
            if (c==classA):
                total_A=total_A+1
                
            elif (c==classB):
                total_B=total_B+1
        
        
        if (total_A>total_B):
            class_name = classA
            probability = total_A/numclasses
            T = (class_name, probability)
            
            return T
        
        elif (total_A<total_B):
            class_name = classB
            probability = total_B/numclasses
            T = (class_name, probability)
            
            return T
        
        elif (total_A==total_B):
            L=[]
            T1 = (classA, 0.50)
            T2 = (classB, 0.50)
            L.append(T1)
            L.append(T2)
            rand = random.SystemRandom()
            
            random_selection = rand.choice(L)
            
            return random_selection
            
            
    #Checks if a node is pure
    def purityCheck(self,instances):
        
        classA = self.classes[0]
        classB = self.classes[1]
        
        classes = []
        num_classes = len(instances)
        total_A=0
        total_B=0
        
        for index, row in instances.iterrows():
            classes.append(row[0])
        
        
        for c in classes:
            if (c==classA):
                total_A=total_A+1
            elif (c==classB):
                total_B=total_B+1
                
        if (total_A==num_classes):
            return True
        elif (total_B==num_classes):
            return True
        else:
            return False
        
        
      
    def BuildTree(self, instances, attributes):
        
        if (len(instances)==0):
            
            return LeafNode(self.baseline[0],self.baseline[1]) 
        
        elif (self.purityCheck(instances)):
            pure_class = instances.iloc[0,0]
            probability = 1
            return LeafNode(pure_class, probability)
        
        elif (len(attributes)==0):
            
            T = self.countMajority(instances)
            return LeafNode(T[0],T[1])
        
    
        else: 
            
            bestAtt=""
            bestInstsTrue=pd.DataFrame()
            bestInstsFalse=pd.DataFrame()
            maxpurity=0
            for a in attributes:
                true_instances=[]
                false_instances=[]
                
                for index, row in instances.iterrows():
                    if(row[a] is True):
     
                        true_instances.append(row)
                    elif (row[a] is False):
                        false_instances.append(row)
                
               ## convert to dataframe for ease of use
                true_instances=pd.DataFrame(true_instances)
                false_instances=pd.DataFrame(false_instances)
                
                #Get purity for each set
                purity_true = self.calcPurity(true_instances)
                
                
                purity_false = self.calcPurity(false_instances)
                
                
                #Get average weighted purity
                weighted_average_purity = self.calcWeightedPurity(purity_true, purity_false, true_instances, false_instances)
                
                
                if (weighted_average_purity>=maxpurity):
                    
                    maxpurity=weighted_average_purity
                    bestAtt = a
                    bestInstsTrue = true_instances
                    bestInstsFalse = false_instances
            
         
            attributes.remove(bestAtt)
            left = self.BuildTree(bestInstsTrue, attributes)
            right = self.BuildTree(bestInstsFalse, attributes)
            
            return Node(bestAtt,left,right)
            
                

if __name__ == "__main__":
    # DATA PREPROCESSING
    names = []
    classes = []
    attributes = []
    with open('hepatitis-training.dat') as f:
        first_line = f.readline()
        second_line = f.readline()
        
        classes = [x for x in first_line.split()]
        attributes = [x for x in second_line.split()]
    
        names = ["CLASS"] + attributes #for pandas to use (important)
        
    training_data = pd.read_csv(sys.argv[1],delim_whitespace=True, names = names, skiprows=[0,1])
    test_data = pd.read_csv(sys.argv[2],delim_whitespace=True, names = names, skiprows=[0,1])
    
    DT = DecisionTree (training_data,classes)
    Tree = DT.BuildTree(training_data,attributes)
    
    
    def predict (T,row):
        current_node_type = T.__class__.__name__
        true = None
        false = None
        
        
        if(current_node_type=="LeafNode"):
            return T.className
        
        elif(current_node_type=="Node"):
            true = T.left
            false = T.right
            
            if(row[T.attName]==True):
                return predict (true,row)
            elif(row[T.attName]==False):
                return predict (false,row)
                
        
    
    predictions=[]
    actual = []
    for index, row in test_data.iterrows():
        predictions.append(predict(Tree,row))
        
    
    for index, row in test_data.iterrows():
        actual.append(row[0])
        
    count = 0
    for i in range(len(predictions)):
        if(predictions[i]==actual[i]):
            count=count+1
    
    
    print("\n -----RESULTS-----\n")
    accuracy = count/len(predictions)
    print("Accuracy:", accuracy,"With",count,"/",len(predictions),"correct predictions \n")
    print("Baseline prediction:", DT.baseline,"\n")    
    Tree.report("  ")
    
    
    


    
    

    





        
    






    
    
    
    
    
    
    
        
    








  

            
            

            
        
        
