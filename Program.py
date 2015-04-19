'''
Created on Mar 24, 2015

@author: t-amirub
'''

import networkx as nx
import Louvain as community_package
print("fileName(no extension):")
fileName = input()
file = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/network"+ fileName+ ".dat" , "rb")

G=nx.read_weighted_edgelist(file)
part = community_package.best_partition(G)
for keys,values in part.items():
    print(keys)
    print(values)
    
print(community_package.modularity(part, G))

output = open("output" + fileName + ".txt",'w')
for keys,values in part.items():
    output.write(keys)
    output.write('\t')
    for val in values :
        output.write(str(val))
        output.write(" ")
    output.write('\n')
output.close() 