__author__ = 't-amirub'
import networkx as nx
from GraphMetaData import *
from OverlappingLouvain import *

'''
dir = "C:/cygwin64/home/t-amirub/binary_networks/"
file = open(dir+"network.dat", "rb")
print ("on = 2500 om =5")
g=nx.read_edgelist(file)

g= nx.convert_node_labels_to_integers(g)
'''
g = nx.Graph()
g.add_edge(0,4)
g.add_edge(0,5)
g.add_edge(1,4)
g.add_edge(1,5)
g.add_edge(2,4)
g.add_edge(2,5)
g.add_edge(3,4)
g.add_edge(3,5)



metaData = Initialize_Weights(g)

betta = 1.1
print(betta)

myLouvain = FindCommunities(g, betta)
print(myLouvain)
'''
from OriginalLouvain import *

dendo = generate_dendrogram(g)
originalLouvain = partition_at_level(dendo, 0)
print(originalLouvain)

i = 0
for node in myLouvain.keys():
    if originalLouvain[node] not in myLouvain[node]:
        i += 1
        print("not good. node {0} is in {1} in my, but in {2} in original..".format(node, myLouvain[node],originalLouvain[node]))
print("done i = {0}".format(i))
'''

'''
mi = Calc_Modularity_Improvement(1, node, metaData)

print(mi)

betta = 2
comms_imps = [[8,22],[9,50],[10,100],[1,10],[2,11], [3,13]]
print (Keep_Best_Communities(comms_imps,  betta))
'''