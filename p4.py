from math import *
# Add any relevant import statements up here.


# Programming Assignment 4:
# Follow the instuctions in comments throughout this file.
# You might consider doing the assignment in this order: 1, 2, 5, 6a, 3, 4, 6b.

class WeightedAdjacencyMatrix :

    # I didn't show you __slots__  yet in Python.
    # Although technically you do not need to declare variables, including object attributes
    # prior to first use, a consequence of that is that Python must allocate more memory than
    # actually needed because it has no way of knowing how much you will need.
    # __slots__ offers a way of being more memory efficient.  It tells Python exactly what
    # attributes this class will have.  In this case, only a field named _W.  So Python will
    # only allocate enough memory for the attributes specified in __slots__ (just separate by commas
    # if you need more than one).
    # If you try to specify an attribute that is not included in this list you will get a runtime
    # exception.
    __slots__ = ['_W']

    # 1) Implement the initializer, which should create a matrix with
    # number of rows and columns both equal to size (i.e., number of nodes).
    # Initially there are no edges, which means that the weights should all initially
    # be infinity (inf in Python).
    #
    # Name your matrix _W (see comment above that explains __slots__.
    # Remember to use self for an object attribute (i.e., self._W )
    def __init__(self, size) :
        """Initializes a weighted adjacency matrix for a graph with size nodes.

        Graph is initialized with size nodes and 0 edges.
        
        Keyword arguments:
        size -- Number of nodes of the graph.
        """

        self._W = [[inf for x in range(size)] for y in range(size)]

    # 2) Implement this method (see the provided docstring)
    def add_edge(self, u, v, weight) :
        """Adds a directed edge from u to v with the specified weight.

        Keyword arguments:
        u -- source vertex id (0-based index)
        v -- target vertex id (0-based index)
        weight -- edge weight
        """
        self._W[u][v] = weight

    # 5) Implement this method (see the provided docstring)
    def floyd_warshall(self) :
        """Floyd Warshall algorithm for all pairs shortest paths.

        Returns a matrix D consisting of the weights of the shortest paths between
        all pairs of vertices.  This method does not change the weight matrix of the graph itself.

        Extra Credit version: Returns a tuple (D, P) where D is a matrix consisting of the
        weights of the shortest paths between all pairs of vertices, and P is the predecessors matrix.
        """
        dist = [i[:] for i in self._W]
##        dist = []
##        pred = []
##        for i in range (self._W):
##            dist.append([])
##            pred.append([])
##            dist[i][i] = 0
##            for j in range (self._W) :
##                dist[i].append(inf)
##                pred[i].append(0)
                
        for k in range(len(dist)) :
            for u in range(len(dist)) :
                for v in range(len(dist)):
                    if(u == v):
                        dist[u][v] = 0
                    dist[u][v] = min(dist[u][v], dist[u][k] + dist[k][v])
        return dist

# 3) Implement this function.  First note the lack of indentation.  This is not a method of the above class.
# It is a function.
# You can find the relevant equation for haversine distance at this link (and others):
# https://www.movable-type.co.uk/scripts/latlong.html
# That link also includes javascript for computing haversine distance.
# It should be straightforward to translate this to Python.
# See documentation of Python's math functions for any needed trig functions as well as degree
# to radian conversion: https://docs.python.org/3/library/math.html
def haversine_distance(lat1, lng1, lat2, lng2) :
    """Computes haversine distance between two points in latitude, longitude.

    Keyword Arguments:
    lat1 -- latitude of point 1
    lng1 -- longitude of point 1
    lat2 -- latitude of point 2
    lng2 -- longitude of point 2

    Returns haversine distance.
    """

    R = 6372.8 # Earth radius in kilometers
 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
     
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
 
    return R * c



# 4) Implement this function.  First note the lack of indentation.  This is not a method of the above class.
# It is a function.
#
# Specifically, it should be able to parse a file of the format from this set of graphs: http://tm.teresco.org/graphs/
# Details of the format itself can be found here: http://courses.teresco.org/metal/graph-formats.shtml
# Only worry about the "simple" format (and NOT the "collapsed" format).
# You might start by looking at one of the smaller graphs to see what the format looks like, such as Andora.
# First line of all files is: TMG 1.0 simple
# Second line tells you number of vertices and number of edges: V E
# The next V lines provide one vertex per line of the form: StringID  latitude  longitude
# You only really need the latitude and longitude values, and simply use 0 to V-1 as the vertex ids instead of the given
# strings.
# The next E lines provide the edges, one per line, of the form: from to aValueYouDontNeedForThisAssignment.
# You only need the from and to values, and not the 3rd value on the line.
# The from and to tell you the endpoints of an edge (0 based indices into the list of vertices).
# For each edge in this list add two directed edges to the WeightedAdjacencyMatrix (one in each direction).
# The weight for the edge should be the so-called haversine distance (which you implemented a function to
# compute in Step 3.
#
# HINTS (for parsing input file):
# You can find Python file IO examples here: https://docs.python.org/3/tutorial/inputoutput.html
# Scroll to 7.2 and look at examples of open. Specifically, see example that uses "with" which
# has the advantage that Python will automatically close the file for you at the end of the with block.
#
# The call to read() in that example, however, reads the entire file at once as a String.
# You will find it useful, to instead iterate over the lines of the file.  You can either use the readline
# method directly for this.  Or, see the example on that same page that uses a loop of the form:
# for line in f (each iteration of this loop will automatically call readline to get the next line of
# the file and loop will iterate over entire file).
#
# Useful methods for parsing the input graph file:
# The split method for Strings: https://docs.python.org/3/library/stdtypes.html#string-methods
#
# Converting String that is a number to a number type:
# float(s) will convert a string s that contains a floating-point number to a floating point number.
# For example, 
# s = "101.25"  # s is a string that happens to look like a floating-point number.
# v = float(s)  # v will now have the floating-point value 101.25
# Likewise, int(s) will do the same but for integer values.
#
def parseHighwayGraphData(filename) :
    """Parses a highway graph file and returns a WeightedAdjacencyMatrix.

    Keyword arguments:
    filename -- name of the file.

    Returns a WeightedAdjacencyMatrix object.
    """

    class VertexData:
        pass
    v, e = 0
    with open(filename) as f:
        f.readline()
        split = f.readline().split()
        v = int(split[0])
        e = int(split[0])
        vertices = [VertexData() for i in range(v)]
        graph = WeightedAdjacencyMatrix(v)
        for i in range(v):
            word = f.readline().split()
            word.pop(0)
            vertices[i].lat = float(words[0])
            vertices[i].lng = float(words[1])
        for i in range(v):
            word = f.readline().split()
            u = int(words[0])
            v = int(words[1])
            weight = haverstine_distance( vertices[u].lat, vertices[u].lng, vertices[v].lat, vertices[v].lng )
            graph.add_edge(u,v,weight)
    return graph
        


# 6a) This function should construct a WeightedAdjacencyMatrix object with the vertices and edges of your choice
# (small enough that you can verify that your Floyd Warshall implementation is correct).
# After constructing the WeightedAdjacencyMatrix object, call your floyd_warshall method, and then
# output the D matrix it returns using print statements (one row of matrix per line, columns separated by tabs).
# If you also computed the predecessor matrix, then output that as well (print a blank line between the matrices).
def testWithYourOwnGraphs() :
    g = WeightedAdjacencyMatrix(5)
    g.add_edge(0, 3, 4)
    g.add_edge(1, 2, 5)
    g.add_edge(2, 3, 3)
    g.add_edge(2, 4, 1)
    g.add_edge(1, 3, 4)
    d = g.floyd_warshall()

    for i in d:
        for j in i :
            print(j, end = "\t")
        print()



# 6b) This function should use your parseHighwayGraphData to get a WeightedAdjacencyMatrix object corresponding
# to the graph of your choice from http://tm.teresco.org/graphs/ (I recommend starting with one of the small graphs).
# Then use your floyd_warshall method to compute all pairs shortest paths.
# Don't output the entire matrix since that would be a bit large (even for the smaller graphs).
# Instead, the parameter to the function below is a list of 2-tuples.  For each 2-tuple, of the form (from, to)
# in this list, print on one line (in this order): from to distance
# If you implemented the extra credit part (the predecessors), then each line of output should be of the form:
# from to distance pathTaken
# You should do this with at least one graph from the linked site, but I recommend trying it with multiple.
# In what you submit, have this function work with one graph (of your choice).
# Upload that graph when you submit your assignment (in case the page updates the data, this way I'll have the exact
# graph that you used).
def testWithHighwayGraph(L) :

    g = parseHighwayGraphData('LIE-region-simple.tmg.txt')
    d = g.floyd_warshall()
    print("Form", "\t" , "To", "\t", "Distance", "\t", "Path Taken")
    for i in L:
        vertex_u = i[0]
        vertex_v = i[1]
        print(vertex_u, "\t", vertext[v], "\t", d[vertex_u][vertex_v], "\t", end="\t")
        pathTaken(p, vertex_u, vertex_v)
        print()
def pathTaken (p, u, v) :
    path = []
    if u == v:
        path.append(u)
        print(u, end ="\t")
    elif p[u][v] == 0:
        print("No Path", end "\t")
    else:
        pathTaken(p,u,p[u],p[v])
        path.append(v)
        print(v, end ="\t")
