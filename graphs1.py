from math import *
from collections import deque

# Undirected graph as adjacency lists
class Graph :
    
    # constructor
    # n is number of vertices
    def __init__(self,n=10,edges=[]) :
        self._adj = [[] for x in range(n)]
        for e in edges :
            self.addEdge(e[0],e[1])

    # adds an edge from a to be
    def addEdge(self,a,b) :
        self._adj[a].append(b)
        self._adj[b].append(a)

    # gets number of vertices
    def numVertices(self) :
        return len(self._adj)

    # gets degree of vertex v
    def degree(self,v) :
        return len(self._adj[v])

    # BFS: s is index of starting node
    # Returns a list of VertexData objects, containing
    # distance from s (in field d) and backpointer (pred)
    def BFS(self,s) :
        class VertexData :
            pass
        vertices = [VertexData() for i in range(len(self._adj))]
        for i in range(len(vertices)) :
            vertices[i].d = inf
            vertices[i].pred = -1
        vertices[s].d = 0
        Q = deque()
        Q.append(s)
        while len(Q) > 0 :
            u = Q.popleft()
            for v in self._adj[u] :
                if vertices[v].d == inf :
                    vertices[v].d = vertices[u].d + 1
                    vertices[v].pred = u
                    Q.append(v)
        return vertices

    # DFS: Returns a list of VertexData objects containing fields for
    # discovery time (d) and finish time (f) and backpointer (pred).
    def DFS(self) :
        class VertexData :
            pass
        vertices = [VertexData() for i in range(len(self._adj))]
        for i in range(len(vertices)) :
            vertices[i].d = 0
            vertices[i].pred = -1
        time = 0
        def visit(self,u) :
            nonlocal time
            nonlocal vertices
            time = time + 1
            vertices[u].d = time
            for v in self._adj[u] :
                if vertices[v].d == 0 :
                    vertices[v].pred = u
                    visit(self,v)
            time = time + 1
            vertices[u].f = time
        
        for u in range(len(vertices)) :
            if vertices[u].d == 0 :
                visit(self,u)
        return vertices
                       
    # print graph (for testing)
    def printGraph(self) :
        print("Graph has", len(self._adj), "vertices.")
        for i, L in enumerate(self._adj) :
            print(i, "->", end="\t")
            for j in L :
                print(j, end="\t")
            print()
                

# Directed graph as adjacency lists
class Digraph(Graph) :

    # adds an edge from a to be
    def addEdge(self,a,b) :
        self._adj[a].append(b)

    # Topological Sort of the directed graph (Section 22.4 from textbook).
    # Returns the topological sort as a list of vertex indices.
    #
    #       Homework Hints/Suggestions/Etc:
    #           1) Textbook indicates to use a Linked List.  Python doesn't have
    #               one in the standard library.  Instead, use a deque (don't simply use
    #               a python list since adding at the front is O(N) for a python list,
    #               while it is O(1) for a deque).
    #           2) From the pseudocode, you will be tempted to (a) call DFS, and then (b) sort
    #               vertices by the finishing times.  However, don't do that since the sort will
    #               cost O(V lg V) unnecessarily.
    #           3) So, how do you do it without sorting?
    #               A) Option A: Start by copying and pasting DFS code to start of topologicalSort, and
    #                   where finishing time is set, add the vertex index to front of list.
    #               B) Option B: Add an optional parameter to DFS method that is a
    #                   function that is called upon finishing a vertex.
    #                   Give it a default that does nothing (i.e., just a pass). Your topologicalSort would then
    #                   call DFS passing a function that adds the vertex index to the front of a list.
    #               C) Option C: any other way you can come up with that doesn't change what DFS currently does logically 
    def topologicalSort(self) :
        class VertexData :
            pass
        vertices = [VertexData() for i in range(len(self._adj))]
        for i in range(len(vertices)) :
            vertices[i].d = 0
            vertices[i].pred = -1
        topoSort = deque()
        time = 0
        def visit(self,u) :
            nonlocal time
            nonlocal vertices
            time = time + 1
            vertices[u].d = time
            for v in self._adj[u] :
                if vertices[v].d == 0 :
                    vertices[v].pred = u
                    visit(self,v)
            time = time + 1
            vertices[u].f = time
            topoSort.appendleft(u)
            
        for u in range(len(vertices)) :
            if vertices[u].d == 0 :
                visit(self,u)
        #return vertices
        return list(deque(topoSort))
    
    # Computes the transpose of a directed graph. (See textbook page 616 for description of transpose).
    # Does not alter the self object.  Returns a new Digraph that is the transpose of self.
    def transpose(self) :
        transList = []
        for i in range(len(self._adj)) :
            L = self._adj[i]
            for j in range(len(L)) :
                transList.append((L[j],i))
        transG = Digraph(len(self._adj), transList)
        return transG.printGraph()

    # Computes the strongly connected components of a digraph.
    # Returns a list of lists, containing one list for each strongly connected component, which is simply
    # a list of the vertices in that component.
    #
    #       Homework Hints/Suggestions/Etc: See algorithm on page 617.
    #           1) Take a look at steps 1 and 2 before you do anything.  Notice that Step 1 computes finishing times with DFS,
    #               and step 3 uses vertices in order of decreasing finishing times.  As in the topological sort, don't actually sort
    #               by finishing time (to avoid O(V lg v) step).  However, this is easier than in the topological sort as you already
    #               have a method that will get you what you need.  For step 1 of algorithm you can simply call your topological sort.
    #               That will give you the vertices in decreasing order by finishing time, which is really the intention of line 1.
    #           2) Line 2 is just the transpose and you implemented a method to compute this above.
    #           3) The DFS in line 3 can be done in a couple ways.  As above, if you change DFS, make sure it will still function in the basic
    #               version.  The simplest way to do that would be to leave it alone, and just start by copying and pasting the code.
    #               You'll need to then alter it to have the outer loop use the vertex ordering obtained from algorithm line 1 (to implement line 3).
    #               And to do line 4, you'll need to further alter it to generate the list of lists for the return value.
    def stronglyConnectedComponents(self) :
        topoVertices = self.topologicalSort()
        transGraph = self.transpose()
        list1 = []
        tempList =[]
        class VertexData :
            pass
        vertices = [VertexData() for i in range(len(self._adj))]
        for i in range(len(vertices)) :
            vertices[i].d = 0
            vertices[i].pred = -1
        time = 0
        
        def visit(transGraph,u) :
            nonlocal time
            nonlocal vertices
            time = time + 1
            vertices[u].d = time
            tempList.append(u)
            
            for v in self._adj[u] :
                if vertices[v].d == 0 :
                    vertices[v].pred = u
                    visit(self,v)
            time = time + 1
            vertices[u].f = time
            
        for u in topoVertices:
            u = topoVertices.pop()
            if vertices[u].d == 0:
                visit(transGraph, u)
                list1.append(tempList)
                tempList = []
        return list1




# Implement any code necessary to test your topological sort, transpose, and strongly connected components methods.
#  E.g., construct graphs for the tests, figure out what the results should be, use your methods, write any code necessary to
#  output results, and check if your algorithms worked correctly.

G = Graph(7, [(0,5),(0,1),(1,3),(5,2),(5,3),(5,4),(3,6)])
H = Digraph(7, [(5,0),(0,1),(1,3),(2,5),(3,5),(5,4),(3,6)])
I = Digraph(8, [(2,4),(0,5),(0,1),(1,3),(5,2),(5,3),(5,4),(3,6)])

