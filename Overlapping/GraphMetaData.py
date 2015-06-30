__author__ = 't-amirub'
import itertools
import networkx as nx

class MetaData :

    m = 0
    K_v = dict()
    K_v_c = dict()
    Intersection_c1_c2 = dict()
    Sigma_c = dict()
    Size_c = dict()
    com2nodes= dict()
    node2coms = dict()

    def __str__(self) :
        return ( " total_weight : " + str(self.m)
            + " K_v : " + str(self.K_v)
            + " K_v_c : " + str(self.K_v_c)
            + " Intersection_c1_c2 : " + str(self.Intersection_c1_c2)
            + " Sigma_c : " + str(self.Sigma_c)
            + " Size_c : " + str(self.Size_c)
            + " com2nodes : " + str(self.com2nodes)
            + " node2coms : " + str(self.node2coms))

    def copy(self) :
        new_MetaData = MetaData()
        new_MetaData.m = self.m
        new_MetaData.K_v = self.K_v.copy()
        new_MetaData.K_v_c = self.K_v_c.copy()
        new_MetaData.Intersection_c1_c2 = self.Intersection_c1_c2.copy()
        new_MetaData.Sigma_c = self.Sigma_c.copy()
        new_MetaData.Size_c = self.Size_c.copy()
        new_MetaData.com2nodes = self.com2nodes.copy()
        new_MetaData.node2coms = self.node2coms.copy()

    def VerifyNodesNumbers(self,graph):
        numOfNodes= graph.number_of_nodes()
        nodes = graph.nodes()
        for i in range(0,numOfNodes -1):
            if i not in nodes:
                raise ValueError("Bad graph - node ids must be all numbers between 0 and |v| -1")

    def init(self, graph):
        """Initialize the MetaData of a graph with every node in one community"""
        self.VerifyNodesNumbers(graph)
        count = 0
        self.m = 0.0
        self.K_v = dict()
        self.K_v_c = dict()
        self.Intersection_c1_c2 = dict()
        self.Sigma_c = dict()
        self.Size_c = dict()
        self.com2nodes = dict()
        self.node2coms = dict()
        self.m = graph.size(weight = 'weight')
        for node in graph.nodes():
            self.Intersection_c1_c2[node] = dict([])
            self.com2nodes[count] = [node]
            self.node2coms[node] = [count]
            nodeWeight = float(graph.degree(node, weight = 'weight'))
            if nodeWeight < 0 :
                raise ValueError("Bad graph type, use positive weights")
            self.K_v[count] = nodeWeight
            self.Sigma_c[count] = nodeWeight
            self.Size_c[count] = 1
            count = count + 1

        for node in graph.nodes() :
            if self.K_v_c.get(node) == None :
                self.K_v_c[node] = dict([])
            for neighbour in graph.neighbors(node):
                comm = self.node2coms[neighbour][0]
                weight = float(graph.get_edge_data(node, neighbour,{"weight":0}).get("weight", 1))
                self.K_v_c[node][comm] = weight

    def ClearComms(self, node):
        comms = self.node2coms[node]
        for pairComms in itertools.combinations(comms,2):
            self.Intersection_c1_c2[min(pairComms)][max(pairComms)] -= 1

        for comm in comms:
            print(self.com2nodes[comm])
            self.com2nodes[comm].remove(node)
            print(self.com2nodes[comm])
            self.Size_c[comm] -= 1

        self.node2coms[node] = []

    def SetCommsForNode(self, node, comms):
        commsCouplesIntersectionRatio = []

        for comm in comms:
            self.com2nodes[comm].append(node)
            self.Size_c[comm] += 1

        for pairComms in itertools.combinations(comms, 2):
            lowComm = min(pairComms)
            highComm = max(pairComms)
            if self.Intersection_c1_c2.get(lowComm) == None:
                self.Intersection_c1_c2[lowComm] = dict([])
            if self.Intersection_c1_c2[lowComm].get(highComm) == None:
                self.Intersection_c1_c2[lowComm][highComm] = 0
            intersectionSize = self.Intersection_c1_c2[lowComm][highComm] + 1
            self.Intersection_c1_c2[lowComm][highComm] = intersectionSize
            intersectionRatio = intersectionSize/min(self.Size_c[lowComm], self.Size_c[highComm])
            commsCouplesIntersectionRatio.append((lowComm, highComm, intersectionRatio))
        self.node2coms[node] = comms
        return commsCouplesIntersectionRatio

    def RemoveCommForNode(self, node, c1):
        self.node2coms[node].remove(c1)
        self.com2nodes[c1].remove(node)

