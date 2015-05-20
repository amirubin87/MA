__author__ = 'amirrub'


from CompareUtils import *
from OmegaIndex import *
from py4j.java_gateway import JavaGateway
from py4j.java_gateway import GatewayClient

gateway = JavaGateway(GatewayClient(port=25335))
gateway.entry_point.runSLPA()
'''
#TODO- understand directed. currently SLPA is called with -Sym 1 to double the edges
def readSLPAFile(t_h):
    f= open("C:/Users/t-amirub/SkyDrive/MA/Code/GANXiS_v3.0.2/output/SLPAw_network_run1_r" + str(t_h) +"_v3_T100.icpm"  , "r")#
    output = dict()
    lines = f.readlines()

    comm = 0

    for line in lines:
        nodes =map(int, line.split())
        for node in nodes:
            if output.get(node) == None:
                output[node] = set()
            output[node].add(comm)
        comm = comm+1
    f.close()
    return output

groundTruthFile = open("C:/cygwin64/home/t-amirub/binary_networks//community.dat" , "r")
groundTruth = convertFileToPartition(groundTruthFile)
groundTruthFile.close()


for t_h in (0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5):
    SLPAOutput = readSLPAFile(t_h)
    print ("SLPA t_h: {1}  OmegaIndex:   {0}".format(OmegaIndex(groundTruth,SLPAOutput), t_h))
    print ("")
'''