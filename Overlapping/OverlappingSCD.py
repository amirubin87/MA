__author__ = 't-amirub'
'''
t(node,nodes) = amount of triangles node closes with nodes
T(node) = t(node,allnodes)
WCC(node, comm) = t(node,comm)/(|comm|+|nodes|(T(node) -t(node,comm)))
'''
__author__ = 't-amirub'

import networkx as nx
import operator
from SCDGraphMetaData import *

def FindCommunities(G,metaData, betta):
    isDone = 0
    n = len(G.nodes())
    numOfIterations= 0
    while isDone < n and numOfIterations < n:
        numOfIterations +=1
        print "numOfIterations {0}".format(numOfIterations)
        for nodeS in G.nodes():
            node = int(nodeS)
            c_v_original = metaData.node2coms[node].copy()
            metaData.ClearComms(node)
            comms_inc = []
            neighborComms = Find_Neighbor_Comms(nodeS, metaData, G)
            for neighborComm in neighborComms:
                inc= Calc_WCC(neighborComm,nodeS,metaData, G, n)
                comms_inc.append([neighborComm, inc])
            c_v_new =Keep_Best_Communities(comms_inc, betta)
            metaData.SetCommsForNode(node, c_v_new)
            if set(c_v_new) == set(c_v_original):
                isDone += 1
            else:
                isDone = 0
    return PrepareOutput(metaData.com2nodes)

def GetFirstPartition(G):
    CC = nx.clustering(G)
    sorted_CC = sorted(CC.items(), key=operator.itemgetter(1), reverse=True)
    comm2Nodes= dict()

    commID=0
    sortedNodes = [i[0] for i in sorted_CC]
    isVisited = []
    for v in sortedNodes:
        if v not in isVisited:
            isVisited.append(v)
            comm2Nodes[commID] = {int(v)}
            for neigh in G.neighbors(str(v)):
                if neigh not in isVisited:
                    isVisited.append(neigh)
                    comm2Nodes[commID].add(int(neigh))
            commID+=1
    return PrepareOutput(comm2Nodes)




def PrepareOutput(dictionary):
    """Will keep only keys with values"""
    ans = dict()
    i = 0
    for v in dictionary.values():
        if not len(v) == 0:
            ans[i] = v
            i+=1
    return ans

def Find_Neighbor_Comms(nodeS, metaData, g):
    neighborComms = set()
    for neighbor in g.neighbors(nodeS):
        neighborComms= neighborComms.union(metaData.node2coms[int(neighbor)])
    return list(neighborComms)

def Initialize_MetaData(G,p):
    metaData = SCDMetaData()
    metaData.init(G, p)
    return metaData


def Calc_WCC(comm, nodeS, metaData, G, n):
    commMembers = set(metaData.com2nodes[comm])
    t = calcT(commMembers, nodeS, G)
    divesor = float(len(commMembers) + n*((metaData.T[nodeS] - t)))
    if divesor==0:
        return 0
    WCC = t/divesor
    return WCC

def calcT(commMembers,nodeS, G):
    t= 0
    neigh = map(int,set(G.neighbors(nodeS)))
    neighInComm = commMembers.intersection(neigh)
    for v in neighInComm:
        for u in neighInComm:
            if u > v and G.has_edge(str(u),str(v)):
                t += 1
    return t;

def Keep_Best_Communities(comms_imps,  betta):
    if len(comms_imps) == 0:
        return {}
    bestImp = max(comm_imp[1] for comm_imp in comms_imps)
    if bestImp == 0 :
        return {}
    bestComs =[comm_imp[0] for comm_imp in comms_imps if comm_imp[1]*betta >= bestImp]
    return bestComs


def RunOverlappingSCD(input, outputDir, bettas):
    file = open(input, "rb")
    g=nx.read_edgelist(file)
    file.close()
    firstPartition = GetFirstPartition(g)
    metaData = Initialize_MetaData(g, firstPartition)

    for betta in bettas:
        tmpMetaData = metaData.copy()
        ans= FindCommunities(g, tmpMetaData, betta)
        output = outputDir + "betta{0}.dat".format(betta)
        out = open(output,'w')
        for nodes in ans.values():
            for node in nodes:
                out.write("%s " % node)
            out.write('\n')
        out.close()

bettas = [1.01,1.02,1.3]
RunOverlappingSCD('network.dat', 'out/', bettas)