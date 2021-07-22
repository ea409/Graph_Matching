import numpy as np
import sys

class Graph():
    def __init__(self,Adjacency):
        if sum(sum(np.abs(Adjacency-np.transpose(Adjacency))))!=0: sys.exit('not a symmetric adjacency matrix')
        self.make_graph(Adjacency)

    def make_graph(self, Adjacency):
        graph_dict = {}
        for vertex in range(0, len(Adjacency)):
            graph_dict[vertex]= set(np.where(Adjacency[vertex]==1)[0])
        self.graph_dict = graph_dict

class BipartiteGraph(Graph):
    def __init__(self,*args, **kargs):
        super().__init__(*args, **kargs)
        self.check_bipartite()

    def check_bipartite(self):
        X, Y=set([]),set([])
        while len(X.union(Y))< len(self.graph_dict.keys()):
            new_vertex = (set(self.graph_dict.keys()) - X.union(Y)).pop()
            X.add(new_vertex)
            for adj_vertex in self.graph_dict[new_vertex]:
                Y.add(adj_vertex)
        if len(X.intersection(Y)) !=0: sys.exit('not a bipartite graph')
        self.X, self.Y = X, Y

    def find_matching(self):
        if len(self.X)!=len(self.Y): raise  ValueError("no matching possible because X and Y are mismatched or blocking set size s", np.abs(len(self.Y)-len(self.X)))
        self.intialise_matching()
        while len(self.matching)!=len(self.X):
            unmatched_vertex = (self.X-set(self.matching.keys())).pop()
            rv = self.find_reachable_vertices(unmatched_vertex)
            available_rv = set(rv.fromkeys(self.Y, self.X).keys()) - set(self.matching.keys())
            if len(available_rv)==0: raise ValueError("Blocking set found of size ",len(self.matching)+1)
            self.agumentation(unmatched_vertex, rv, available_rv.pop())

    def find_reachable_vertices(self, unmatched_vertex):
        reachable_vertices = dict()
        newly_reachable_vertices = set([unmatched_vertex])
        while len(newly_reachable_vertices) > 0 :
            curr_newly_reachable_vertices = set()
            for vertex in newly_reachable_vertices:
                sub_vertices = (self.graph_dict[vertex] - reachable_vertices.keys())
                if len(sub_vertices)==0: continue
                for sub_vertex in sub_vertices:
                    curr_newly_reachable_vertices.add(sub_vertex)
                    reachable_vertices[sub_vertex]=vertex
            newly_reachable_vertices=curr_newly_reachable_vertices.copy()
        return reachable_vertices

    def intialise_matching(self):
        self.matching = dict()
        used_vertices = set()
        for vertex in self.X:
            available_vertices = (self.graph_dict[vertex]-used_vertices)
            if len(available_vertices)==0: continue
            partner = available_vertices.pop()
            self.matching[vertex]=partner
            used_vertices.add(partner)

    def agumentation(self, start, rv, end):
        x = rv[end]
        self.matching[x] = end
        while x != start:
            y = rv[x]
            x = rv[y]
            self.matching[x] = y

if __name__ == "__main__":
c=453
XY = np.random.randint(2, size=(c, c))
Adjacency = np.concatenate([np.concatenate([np.zeros([c,c]), np.transpose(XY)], axis=0),  np.concatenate([XY, np.zeros([c,c])], axis=0)], axis=1)
BG=BipartiteGraph(Adjacency)
BG.find_matching()
BG.matching