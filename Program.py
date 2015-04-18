'''
Created on Mar 24, 2015

@author: t-amirub
'''

import networkx as nx
import Louvain as community_package
file = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/network.dat" , "rb")

G=nx.read_weighted_edgelist(file)
part = community_package.best_partition(G)
for keys,values in part.items():
    print(keys)
    print(values)
    
print(community_package.modularity(part, G))