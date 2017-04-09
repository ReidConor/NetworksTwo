import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from random import randint
from dataManipulation import *


if __name__ == "__main__":
    dataFile = "../data/roadNet-CA.txt" #the full data file
    numberOfLines = 100 #the number of lines we want in the sample data file
    preparedDataFile = prepareData(dataFile, numberOfLines) #prepare the data
    G = nx.read_weighted_edgelist(preparedDataFile) #read it in to a graph
    printGraphDetails(G) #print some details on the graph
