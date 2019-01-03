# -*- coding: utf-8 -*-

class Node():

    def __init__ (self,attName,left,right):
        self.left = left
        self.right = right
        self.attName = attName
		
        
    def report (self, indent):
        print(indent,self.attName,"= True:")
        self.left.report(indent+"    ")
        print(indent,self.attName,"= false:")
        self.right.report(indent+"    ")
        

class LeafNode(Node):
    
    def __init__(self,className,prob):
        self.className=className
        self.prob=prob
        
    def report(self,indent):
        count = 1
        if (count==0):
            print(indent,"Unknown\n")
        else:
            print(indent,"Class",self.className,", prob =",self.prob)
            
