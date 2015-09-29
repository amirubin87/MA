__author__ = 't-amirub'
import networkx as nx
import copy

class SCDMetaData :
    T = dict()
    com2nodes= dict()
    node2coms = dict()

    def __str__(self) :
        return ( " T : " + str(self.T)
            + " com2nodes : " + str(self.com2nodes)
            + " node2coms : " + str(self.node2coms))


    def copy(self) :
        new_MetaData = SCDMetaData()
        new_MetaData.T = copy.deepcopy(self.T)
        new_MetaData.com2nodes = copy.deepcopy(self.com2nodes)
        new_MetaData.node2coms = copy.deepcopy(self.node2coms)
        return new_MetaData

    def init(self, graph, initPart):
        """Initialize the SCDMetaData of a graph with every node in one community"""
        self.T = nx.triangles(graph)
        self.com2nodes = dict()
        self.node2coms = dict()
        for comm, nodes in initPart.items():
            self.com2nodes[comm] = nodes
            for node in nodes:
                self.node2coms[node] = set([comm])

    def ClearComms(self, node):
        comms = self.node2coms[node]
        for comm in comms:
            self.com2nodes[comm].remove(node)
        self.node2coms[node] = set()


    def AddCommForNode(self, node, c1):
        self.node2coms[node].add(c1)
        self.com2nodes[c1].add(node)

    def SetCommsForNode(self, node, c_v_new):
        for c in c_v_new:
            self.AddCommForNode(node,c)