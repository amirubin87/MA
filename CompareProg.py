'''
Created on Apr 18, 2015

@author: t-amirub
'''
from CompareUtils import *
from OmegaIndex import *

import networkx as nx
from MyLouvain import *

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

dir = "C:/cygwin64/home/t-amirub/weighted_networks/"
inputFileDirName = ""#"-N 5000 -k 10 -maxk 50 -mut 0.3 -minc 10 -maxc 20 -on 500 -om 5 -muw 0.1 -t1 2 -t2 1"#input()
louvainOutputFileName = inputFileDirName#"-N 5000 -k 5 -maxk 20 -mut 0.3 -minc 10 -maxc 50 -on 100 -om 5 -muw 0.1"#input()

file = open(dir+inputFileDirName+"network.dat", "rb")
G=nx.read_weighted_edgelist(file)

# Checks Omega Index per level in the dendogram
mod_t_h = 1.3
print("mod_t_h: {0}".format(mod_t_h))

dendo = generate_dendrogram(G, mod_t_h, None,True)

groundTruthFile = open(dir+inputFileDirName+"/community.dat" , "r")
groundTruth = convertFileToPartition(groundTruthFile)

for level in range(0, len(dendo)):
    part = partition_at_level(dendo,level)
    print ("Level: {1}       MyLouvain.modularity {0}".format(modularity(part, G), level))

    output = open("MyLouvainOutput" + louvainOutputFileName + ".txt",'w')
    for keys,values in part.items():
        output.write(keys)
        output.write('\t')
        for val in values :
            output.write(str(val))
            output.write(" ")
        output.write('\n')
    output.close()

    louvainOutputFile = open("C:/LiClipse Workspace/MA/MA/MyLouvainOutput" + louvainOutputFileName + ".txt" , "r")
    louvainOutput = convertFileToPartition(louvainOutputFile)
    print ("Level: {1}       Omega:   {0}".format(OmegaIndex(groundTruth,louvainOutput), level))
    print("     ")


'''
#Old version - only checks the best partition
part = best_partition(G,True)
#for keys,values in part.items():
#    print(keys)
#    print(values)

print("     MyLouvain.modularity {0}".format(modularity(part, G)))
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

print ("Omega:   {0}".format(OmegaIndex(groundTruth,louvainOutput)))



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

'''