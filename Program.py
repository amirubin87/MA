'''
Created on Mar 24, 2015

@author: t-amirub
'''
'''
import GenerateGraph
import Communities

a = GenerateGraph.generateGraph()
print('    eventsDicts')
print(a[0])
print('')
print('')
print('    spammers')
print(a[1])
print('')
print('')
print('    senders')
print(a[2])

comms = Communities.superSophisticatedPartition(a[0],"1")
'''
import networkx as nx
import Louvain as community_package
file = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/network.dat" , "rb")

G=nx.read_weighted_edgelist(file)
part = community_package.best_partition(G)
for keys,values in part.items():
    print(keys)
    print(values)
    
print(len(part.items()))
print(community_package.modularity(part, G))