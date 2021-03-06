__author__ = 't-amirub'

import networkx as nx
from GraphMetaData import *


def FindCommunities(G, betta, alpha):
    metaData = Initialize_Weights(G)
    isDone = 0
    amountOfScans = 0
    n = len(G.nodes())
    while isDone < n and amountOfScans < n:
        amountOfScans += 1
        for node in G.nodes():
            c_v_original = metaData.node2coms[node].copy()
            Update_Weights_Remove(c_v_original, node, metaData, G)
            metaData.ClearComms(node)
            comms_inc = []
            neighborComms = Find_Neighbor_Comms(node, metaData, G)
            for neighborComm in neighborComms:
                inc= Calc_Modularity_Improvement(neighborComm, node, metaData)
                comms_inc.append([neighborComm, inc])
            c_v_new =Keep_Best_Communities(comms_inc, betta)
            Update_Weights_Add(c_v_new,node,metaData,G)
            commsCouplesIntersectionRatio = metaData.SetCommsForNode(node, c_v_new)
            haveMergedComms = FindAndMergeComms(commsCouplesIntersectionRatio, alpha, metaData, G)
            if not haveMergedComms and set(c_v_new) == set(c_v_original):
                isDone += 1
            else:
                isDone = 0
    if amountOfScans == n:
        print("NOTICE - THE ALGORITHM HASNT STABLED. IT STOPPED AFTER SCANNING ALL NODES FOR N TIMES.")
    return RenumberComms(metaData.node2coms)

def RenumberComms(dictionary):
    """Renumber the comms in the values of the dictionary from 0 to n
    """
    count = 0
    ret = dictionary.copy()
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
        metaData.Sigma_c[c] = metaData.Sigma_c[c] + metaData.K_v[node] - metaData.K_v_c[node][c]
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
        Update_Weights_Add([c2], node, metaData, g)
        metaData.RemoveCommForNode(node,c1)
    return