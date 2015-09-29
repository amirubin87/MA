
__author__ = 't-amirub'

import networkx as nx
from MetaDataV2 import *

# TODO - merge communities with high amount of shared comms.
# Implementation idea- when a node is added to two comm, add 1 in the right places ( amount of nodes in comm, amount of shared comms)
# Keep in a different list the couples of comms who has more than (optional: 1/betta) shared nodes.
# Merge the comms in the list.
def FindCommunitiesWithPart(G, part, betta, alpha =1.0):
    print (" start find comm ")
    metaData = Initialize_WeightsWithPart(G,part)
    return OL(G, betta, metaData, alpha)


def FindCommunities(G, betta, alpha = 1.0):
    print (" start find comm ")
    metaData = Initialize_Weights(G)
    return OL(G, betta, metaData, alpha)

def OL(G, betta, metaData, alpha) :
    isDone = 0
    n = len(G.nodes())
    numOfRuns = 0
    while isDone < n and numOfRuns < n :
        print ("        in while numOfRuns {0}".format(numOfRuns))
        numOfRuns += 1
        for node in G.nodes():
            c_v_original = metaData.node2coms[node][:]
            Update_Weights_Remove(c_v_original, node, metaData, G)
            metaData.ClearComms(node)
            comms_inc = []
            neighborComms = Find_Neighbor_Comms(node, metaData, G)
            for neighborComm in neighborComms:
                inc= Calc_Modularity_Improvement(neighborComm,node,metaData)
                comms_inc.append([neighborComm, inc])
            c_v_new =Keep_Best_Communities(comms_inc, betta)
            Update_Weights_Add(c_v_new,node,metaData,G)
            commsCouplesIntersectionRatio = metaData.SetCommsForNode(node, c_v_new)
            haveMergedComms = FindAndMergeComms(commsCouplesIntersectionRatio, alpha, metaData, G)
            if not haveMergedComms and set(c_v_new) == set(c_v_original):
                isDone += 1
            else:
                isDone = 0
    if numOfRuns == n :
        print ("                         PROBLEM , more than n runs")
    return PrepareOutput(metaData.com2nodes)

def PrepareOutput(dictionary):
    """Will keep only keys with values"""
    ans = dict()
    i = 0
    for v in dictionary.values():
        if not len(v) == 0:
            ans[i] = v
            i+=1
    return ans

def RenumberComms(dictionary):
    """Renumber the comms in the values of the dictionary from 0 to n
    """
    count = 0
    ret = dictionary[:]
    new_values = dict([])
    for key in dictionary.keys() :
        newSet = set()
        comms = dictionary[key]
        for comm in comms:
            new_value = new_values.get(comm, -1)
            if new_value == -1 :
                new_values[comm] = count
                new_value = count
                count = count + 1
            newSet.add(new_value)
        ret[key] = newSet

    return ret



def Find_Neighbor_Comms(node, metaData, g):
    neighborComms = set()
    for neighbor in g.neighbors(node):
        neighborComms= neighborComms.union(metaData.node2coms[neighbor])
    return list(neighborComms)

def Initialize_Weights(G):
    metaData = MetaData()
    metaData.init(G)
    return metaData

def Initialize_WeightsWithPart(G, part):
    metaData = MetaData()
    metaData.initWithPart(G, part)
    return metaData


def Calc_Modularity_Improvement(comm, node, metaData):
    return metaData.K_v_c[node][comm]-metaData.Sigma_c[comm]*metaData.K_v[node]/(2*metaData.m)


def Keep_Best_Communities(comms_imps,  betta):
    bestImp = max(comm_imp[1] for comm_imp in comms_imps)
    bestComs =[comm_imp[0] for comm_imp in comms_imps if comm_imp[1]*betta >= bestImp]
    return bestComs

def Update_Weights_Remove(c_v, node, metaData, g):
    neighbors = g.neighbors(node)
    for c in c_v:
        metaData.Sigma_c[c] = metaData.Sigma_c[c] - metaData.K_v[node] + metaData.K_v_c[node].get(c,0)
        for neighbour in neighbors:
            weight = float(g.get_edge_data(node, neighbour).get("weight", 1))
            metaData.K_v_c[neighbour][c] -= weight
    metaData.m -= metaData.K_v[node]*(len(c_v) - 1)



def Update_Weights_Add(c_v, node, metaData, g):
    neighbors = g.neighbors(node)
    for c in c_v:
        metaData.Sigma_c[c] = metaData.Sigma_c[c] + metaData.K_v[node] - metaData.K_v_c[node].get(c, 0.0)
        for neighbour in neighbors:
            weight = float(g.get_edge_data(node, neighbour).get("weight", 1))
            metaData.K_v_c[neighbour][c] = metaData.K_v_c[neighbour].get(c,0) + weight
    metaData.m += metaData.K_v[node]*(len(c_v) - 1)

def FindAndMergeComms(commsCouplesIntersectionRatio, criticalIntersectionRate, metaData, g):
    haveMergedComms = False
    for c1c2intersectionRate in filter(lambda x: x[2] > criticalIntersectionRate, commsCouplesIntersectionRatio):
        MergeComms(c1c2intersectionRate[0], c1c2intersectionRate[1], metaData, g)
        haveMergedComms = True
    return haveMergedComms

def MergeComms(c1, c2, metaData, g):
    for node in metaData.com2nodes[c1]:
        Update_Weights_Remove([c1], node, metaData, g)
        if node not in metaData.com2nodes[c2]:
            Update_Weights_Add([c2], node, metaData, g)
        metaData.RemoveCommForNode(node,c1)
    return


def dedupEdges(inF, outF):
    file = open(inF, "r")
    lines =file.readlines()
    file.close()
    file = open(outF, "w")
    for line in lines:
        nodes = line.split('\t')
        f = nodes[0]
        t=nodes[1]
        if t<f:
            file.write(f + " " + t)
            #file.write("\n")
    file.close()

dedupEdges("C:/Users/t-amirub/SkyDrive/MA/DB/email-Enron.txt/email-Enron.txt", "C:/Users/t-amirub/SkyDrive/MA/DB/email-Enron.txt/email-EnronUD.txt")