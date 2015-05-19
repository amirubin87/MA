'''
Created on Apr 18, 2015

@author: t-amirub
'''
from __future__ import division
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

dir = "C:/cygwin64/home/t-amirub/binary_networks/"
inputFileDirName = ""#"-N 5000 -k 10 -maxk 50 -mut 0.3 -minc 10 -maxc 20 -on 500 -om 5 -muw 0.1 -t1 2 -t2 1"#input()
print("Om = 2 On =500")
file = open(dir+inputFileDirName+"network.dat", "rb")
G=nx.read_edgelist(file)
    #.read_weighted_edgelist(file)
file.close()
groundTruthFile = open(dir+inputFileDirName+"/community.dat" , "r")
groundTruth = convertFileToPartition(groundTruthFile)
groundTruthFile.close()


# My Louvain:
for mod_t_h in (1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.1,1.2,1.3,1.4,1.5):
    dendo = generate_dendrogram(G, mod_t_h, None,True,True)
    #for level in range(0,len(dendo)):
    level = 0
    part = partition_at_level(dendo,level)
    #convert all string to int
    louvainOutput  = {int(k):v for k,v in part.items()}
    print ("mod_t_h: {1} level:{2} OmegaIndex:   {0}".format(OmegaIndex(groundTruth,louvainOutput), mod_t_h, level))
    print ("")

#SLPA:
for t_h in (0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5):
    SLPAOutput = readSLPAFile("C:/Users/t-amirub/SkyDrive/MA/Code/GANXiS_v3.0.2/output/SLPAw_network_run1_r", t_h)
    print ("SLPA t_h: {1}  OmegaIndex:   {0}".format(OmegaIndex(groundTruth,SLPAOutput), t_h))
    print ("")
