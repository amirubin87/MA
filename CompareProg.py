'''
Created on Apr 18, 2015

@author: t-amirub
'''
from CompareUtils import *

import networkx as nx
import MyLouvain as community_package

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

'''-------------------------------------------
                    MAIN
-------------------------------------------'''

print("inputFileDirName(no extension):")
inputFileDirName = input()
print("louvainOutputFileName(no extension):")
louvainOutputFileName = input()

file = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/"+inputFileDirName+"/network.dat" , "rb")
G=nx.read_weighted_edgelist(file)


#New
part = community_package.best_partition(G,True)
#for keys,values in part.items():
#    print(keys)
#    print(values)

print("     MyLouvain.modularity {0}".format(community_package.modularity(part, G)))
print("     ")


output = open("MyLouvainOutput" + louvainOutputFileName + ".txt",'w')
for keys,values in part.items():
    output.write(keys)
    output.write('\t')
    for val in values :
        output.write(str(val))
        output.write(" ")
    output.write('\n')
output.close()



groundTruthFile = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/"+inputFileDirName+"/community.dat" , "r")
groundTruth = convertFileToPartition(groundTruthFile)
louvainOutputFile = open("C:/LiClipse Workspace/MA/MA/MyLouvainOutput" + louvainOutputFileName + ".txt" , "r")
louvainOutput = convertFileToPartition(louvainOutputFile)

print("groundTruth:   {0}".format(groundTruth))
# print louvainOutput BOLD when not the same
print("louvainOutput: {", end="")

for key in louvainOutput.keys() :
    val = louvainOutput[key]
    if groundTruth[key] != val :
        print (color.RED + " {0}: {1},".format(key,val) + color.END , end="")
    else:
        print (" {0}: {1},".format(key,val), end="")
print ("}")

groundTruthComms = com2Nodes(groundTruth)
louvainOutputComms = com2Nodes(louvainOutput)
print("groundTruthComms amount of comms:   {0}, {1}".format(len(groundTruthComms), groundTruthComms))
print("louvainOutputComms amountof comms : {0}, {1}".format(len(louvainOutputComms), louvainOutputComms))

