__author__ = 't-amirub'
import networkx as nx
#from GraphMetaData import *
#from OverlappingLouvain import *


import os

def RunOverlappingLouvain(input, output, betta):
    file = open(input, "rb")
    line =file.readline()
    if os.stat(input).st_size == 0:
        print ("GOTIT")

    file.close()
    '''
    g=nx.read_edgelist(file)
    myLouvain = FindCommunities(g, betta)
    out = open(output,'w')
    for nodes in myLouvain.values():
        for node in nodes:
            out.write("%s " % node)
        out.write('\n')
    out.close()
    '''
RunOverlappingLouvain('C:/Temp/output.txt', '', 1)#C:/cygwin64/home/t-amirub/binary_networks/network.dat', 'C:/cygwin64/home/t-amirub/binary_networks/res.dat', 1.05)
