
__author__ = 't-amirub'
import networkx as nx
import itertools
import copy

class SCDMetaData :
    T = dict()
    com2nodes= dict()
    node2coms = dict()
    Intersection_c1_c2 = dict()


    def __str__(self) :
        return ( " T : " + str(self.T)
            + " com2nodes : " + str(self.com2nodes)
            + " node2coms : " + str(self.node2coms)
            + " Intersection_c1_c2 : " + str(self.Intersection_c1_c2))


    def copy(self) :
        new_MetaData = SCDMetaData()
        new_MetaData.T = copy.deepcopy(self.T)
        new_MetaData.com2nodes = copy.deepcopy(self.com2nodes)
        new_MetaData.node2coms = copy.deepcopy(self.node2coms)
        new_MetaData.Intersection_c1_c2 = self.Intersection_c1_c2.copy()
        return new_MetaData

    def init(self, graph, initPart):
        """Initialize the SCDMetaData of a graph with every node in one community"""
        self.T = nx.triangles(graph)
        self.com2nodes = dict()
        self.node2coms = dict()
        self.Intersection_c1_c2 = dict()
        for comm, nodes in initPart.items():
            self.com2nodes[comm] = nodes
            self.Intersection_c1_c2[comm] = dict([])
            for node in nodes:
                self.node2coms[node] = set([comm])

    def ClearComms(self, node):
        comms = self.node2coms[node]
        for comm in comms:
            self.com2nodes[comm].remove(node)
        self.node2coms[node] = set()
        for pairComms in itertools.combinations(comms,2):
            self.Intersection_c1_c2[min(pairComms)][max(pairComms)] -= 1


    def AddCommForNode(self, node, c1):
        comms = self.node2coms[node]
        for comm in comms:
            lowComm = min(comm, c1)
            highComm = max(comm, c1)
            if self.Intersection_c1_c2.get(lowComm) == None:
                self.Intersection_c1_c2[lowComm] = dict([])
            if self.Intersection_c1_c2[lowComm].get(highComm) == None:
                self.Intersection_c1_c2[lowComm][highComm] = 0
            self.Intersection_c1_c2[lowComm][highComm] += 1
        self.node2coms[node].add(c1)
        self.com2nodes[c1].add(node)


    def RemoveCommForNode(self, node,c1):
        self.node2coms[node].remove(c1)
        self.com2nodes[c1].remove(node)
        for comm in self.node2coms[node]:
            self.Intersection_c1_c2[min(comm, c1)][max(comm,c1)] -= 1

    def SetCommsForNode(self, node, comms):
        commsCouplesIntersectionRatio = []

        for pairComms in itertools.combinations(comms, 2):
            lowComm = min(pairComms)
            highComm = max(pairComms)
            if self.Intersection_c1_c2.get(lowComm) == None:
                self.Intersection_c1_c2[lowComm] = dict([])
            if self.Intersection_c1_c2[lowComm].get(highComm) == None:
                self.Intersection_c1_c2[lowComm][highComm] = 0
            intersectionSize = self.Intersection_c1_c2[lowComm][highComm] + 1
            #self.Intersection_c1_c2[lowComm][highComm] = intersectionSize will be increased in AddCommForNode
            intersectionRatio = intersectionSize/min(len(self.com2nodes[lowComm]), len(self.com2nodes[highComm]))
            commsCouplesIntersectionRatio.append((lowComm, highComm, intersectionRatio))
        for comm in comms:
            self.AddCommForNode(node, comm)
        return commsCouplesIntersectionRatio
