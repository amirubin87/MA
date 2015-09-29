
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

def FindCommunities(G,metaData, betta, alpha):
    isDone = 0
    n = len(G.nodes())
    numOfIterations= 0
    while isDone <= n and numOfIterations < 30:
        print "numOfIterations: {0}".format(numOfIterations)

        numOfIterations +=1
    #    raw_input("Press Enter to continue...")
        for node in G.nodes():
            c_v_original = metaData.node2coms[node].copy()
            metaData.ClearComms(node)
            comms_inc = []
            neighborComms = Find_Neighbor_Comms(node, metaData, G)
            for neighborComm in neighborComms:
                inc= Calc_WCC(neighborComm,node,metaData, G, n)
                comms_inc.append([neighborComm, inc])
            c_v_new =Keep_Best_Communities(comms_inc, betta)
            commsCouplesIntersectionRatio = metaData.SetCommsForNode(node, c_v_new)
            haveMergedComms = FindAndMergeComms(commsCouplesIntersectionRatio, alpha, metaData, G)
            if not haveMergedComms and set(c_v_new) == set(c_v_original):
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
            comm2Nodes[commID] = {v}
            for neigh in G.neighbors(v):
                if neigh not in isVisited:
                    isVisited.append(neigh)
                    comm2Nodes[commID].add(neigh)
            commID+=1
    return PrepareOutput(comm2Nodes)

def GetPartitionFromFile(partFile):
    file = open(partFile, "rb")
    part = file.readlines()
    file.close()
    comm2Nodes= dict()

    commID=0
    for comm in part:
        if len(comm)>2:
            comm2Nodes[commID] = set(map(int, comm.replace(" \n", "").replace("\n", "").split(" ")))
            commID +=1
#    raw_input("Press Enter to see first partition...")
#    print PrepareOutput(comm2Nodes)
#    raw_input("Press Enter to go on...")

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

def Find_Neighbor_Comms(node, metaData, g):
    neighborComms = set()
    for neighbor in g.neighbors(node):
        neighborComms= neighborComms.union(metaData.node2coms[neighbor])
    return list(neighborComms)

def Initialize_MetaData(G,p):
    metaData = SCDMetaData()
    metaData.init(G, p)
    return metaData


def Calc_WCC(comm, node, metaData, G, n):
    commMembers = set(metaData.com2nodes[comm])

    t = calcT(commMembers, node, G)
    divesor = float(len(commMembers) + n*((metaData.T[node] - t)))
    if divesor==0:
        return 0
    WCC = n*t/divesor
    return WCC

def calcT(commMembers,node, G):
    t= 0
    neigh = set(G.neighbors(node))
    neighInComm = commMembers.intersection(neigh)
    for v in neighInComm:
        for u in neighInComm:
            if u > v and G.has_edge(u,v):
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
    g=nx.read_edgelist(file, nodetype = int)
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

def RunOverlappingSCDWithPart(input, partFile, outputDir, bettas):
    file = open(input, "rb")
    g=nx.read_edgelist(file, nodetype = int)
    file.close()
    firstPartition = GetPartitionFromFile(partFile)
    metaData = Initialize_MetaData(g, firstPartition)

    for betta in bettas:
        print "betta: {0}".format(betta)
        tmpMetaData = metaData.copy()
        ans= FindCommunities(g, tmpMetaData, betta)
        output = outputDir + "betta{0}.dat".format(betta)
        out = open(output,'w')
        for nodes in ans.values():
            for node in nodes:
                out.write("%s " % node)
            out.write('\n')
        out.close()

def FindAndMergeComms(commsCouplesIntersectionRatio, criticalIntersectionRate, metaData, g):
    haveMergedComms = False
    for c1c2intersectionRate in filter(lambda x: x[2] > criticalIntersectionRate, commsCouplesIntersectionRatio):
        MergeComms(c1c2intersectionRate[0], c1c2intersectionRate[1], metaData, g)
        haveMergedComms = True
    return haveMergedComms

def MergeComms(c1, c2, metaData, g):
    nodes = list(metaData.com2nodes[c1])
    for node in nodes:
        metaData.RemoveCommForNode(node,c1)
        if node not in metaData.com2nodes[c2]:
            metaData.AddCommForNode(node, c2)
    return

