'''
@author: t-amirub
'''
from CompareUtils import *
from OmegaIndex import *
from AverageF1Score import *
import networkx as nx
#from OriginalLouvain import *


'''-------------------------------------------
                    MAIN
-------------------------------------------'''

RealNetworkDir = "C:/Users/t-amirub/SkyDrive/MA/DB/Amazon/"

print("Amazon Original Louvain")
file = open(RealNetworkDir+"com-amazon.ungraph.txt", "rb")
G=nx.read_edgelist(file)
file.close()
print(len(G.nodes()))
groundTruthFile = open(RealNetworkDir + "com-amazon.all.cmty.txt" , "r")
groundTruth = convertStanfordCommFileToPartition(groundTruthFile)
groundTruthFile.close()
groundTruthSetsOfNodes = ConvertPartitionToSetsOfNodes(groundTruth)
# For NMI
OutputSetOfNodes(groundTruthSetsOfNodes, RealNetworkDir + "Output/AmazonSetOfNodes.txt")

print("Amazon Original Louvain read all input")


#Originl Louvain

from OriginalLouvain import *
dendo = generate_dendrogram(G)
print("Amazon Original Louvain is done")

level = 0
part = partition_at_level(dendo,level)
#convert all string to int
OriginalLouvainOutput  = {int(k):{v} for k,v in part.items()}

#print (" level:{1} OmegaIndex:   {0}".format(OmegaIndex(groundTruth,OriginalLouvainOutput), level))

OriginalLouvainSetsOfNodes = ConvertPartitionToSetsOfNodes(OriginalLouvainOutput)

# For NMI
OutputSetOfNodes(OriginalLouvainSetsOfNodes, RealNetworkDir + "Output/OriginalLouvain.txt")
#
print("Amazon Original Louvain calcF1")

print (" level:{1} AverageF1:   {0}".format(AverageF1(OriginalLouvainSetsOfNodes,groundTruthSetsOfNodes), level))
print ("")




# My Louvain:
'''
from MyLouvain import *

i=0
for mod_t_h in (1.009,1.01,1.011,1.012,1.015,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.1,1.2,1.3,1.4,1.5):
    dendo = generate_dendrogram(G, mod_t_h, None,True,False)
    #for level in range(0,len(dendo)):
    level = 0
    part = partition_at_level(dendo,level)
    print ("                      Louvain with t_h {0}  done".format(mod_t_h))
    #convert all string to int
    louvainOutput  = {int(k):v for k,v in part.items()}

    #print ("mod_t_h: {1} level:{2} OmegaIndex:   {0}".format(OmegaIndex(groundTruth,louvainOutput), mod_t_h, level))

    louvainSetsOfNodes = ConvertPartitionToSetsOfNodes(louvainOutput)

    # For NMI
    OutputSetOfNodes(louvainSetsOfNodes, RealNetworkDir + "Output/Louvain" + str(i) + ".txt")
    #i = i+1
    #
    print ("mod_t_h: {1} level:{2} AverageF1:   {0}".format(AverageF1(louvainSetsOfNodes,groundTruthSetsOfNodes), mod_t_h, level))
    print ("")

'''



#SLPA
'''
i=0
for t_h in (0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5):
    SLPAOutput = readSLPAFile("C:/Users/t-amirub/SkyDrive/MA/Code/GANXiS_v3.0.2/outputTest/SLPAw_network_run1_r", t_h)
    print ("SLPA t_h: {1}  OmegaIndex:   {0}".format(OmegaIndex(groundTruth,SLPAOutput), t_h))

    SLPAsetsOfNodes = ConvertPartitionToSetsOfNodes(SLPAOutput)
    # For NMI
    OutputSetOfNodes(SLPAsetsOfNodes, "c:\Temp\MA\SLPA" + str(i) + ".txt")
    i = i+1
    #
    print ("SLPA t_h: {1}  AverageF1:   {0}".format(AverageF1(SLPAsetsOfNodes,groundTruthSetsOfNodes), t_h))
    print ("")
'''