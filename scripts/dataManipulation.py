import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from random import randint


def prepareData(fileName, numberOfLines):
        l = []
        l.append(fileName)
        l.append(".sample")
        sampleFileName = ''.join(l)


        #create a sample of the file
        with open(fileName) as myfile:
            head = [next(myfile) for x in range(numberOfLines)]
        with open(sampleFileName, 'w') as f:
            f.writelines(head)

        #add in the weights
        with open(sampleFileName, 'r') as f:
            file_lines = [''.join([x.strip(), " " , str(randint(0,9)), '\n']) for x in f.readlines()]
        with open(sampleFileName, 'w') as f:
            f.writelines(file_lines)

        return sampleFileName



def printGraphDetails(Graph):
    print("Number of nodes is : ", Graph.number_of_nodes())
    myList = Graph.edges()
    anEdge = myList.pop()
    print("The weight assigned to edge ", anEdge, " is: ", Graph.get_edge_data(anEdge[0],anEdge[1] ))
