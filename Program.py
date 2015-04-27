'''
Created on Mar 24, 2015

@author: t-amirub
'''

import networkx as nx
import MyLouvain as community_package
import OriginalLouvain
print("inputFileDirName(no extension):")
inputFileDirName = input()
print("outputFileName(no extension):")
outputFileName = input()
file = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/"+inputFileDirName+"/network.dat" , "rb")
G=nx.read_weighted_edgelist(file)


#New
part = community_package.best_partition(G)
#for keys,values in part.items():
#    print(keys)
#    print(values)

print("     MyLouvain.modularity {0}".format(community_package.modularity(part, G)))
print("     ")


output = open("MyLouvainOutput" + outputFileName + ".txt",'w')
for keys,values in part.items():
    output.write(keys)
    output.write('\t')
    for val in values :
        output.write(str(val))
        output.write(" ")
    output.write('\n')
output.close()


#Original
part = OriginalLouvain.best_partition(G)
#for keys,values in part.items():
#    print(keys)
#    print(values)

print("     OriginalLouvain.modularity {0}".format(OriginalLouvain.modularity(part, G)))
