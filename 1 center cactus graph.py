# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 16:43:35 2014

@author: mehdirifai
"""


### The purpose of this algorithm is to find the 1-center of a cactus graph


### This algortihm only works for cactus graph with hinge centroid

### The graph we used are dictionnaries with vertices and edges 
### as attributes. The edges are tuples. The first value of the 
### tuple is the starting node, the second value is the ending 
### node of the edge and the third value is the weigth of the edge
 


## Number of vertex

def initGraph(vertices=[],edges=[]):
        
#### Initiate an oriented dictionnary-shaped graph  
        
        return {"vertices":vertices,"edges":edges}



### Return the number of nodes of a graph
def nbVertex(graph):
        return len(vertices(graph))

def vertices(graph):
        
### Return the list of nodes
        
        return graph["vertices"]
        
def edges(graph):
        
### Return the list of edges
        
        return graph["edges"]
        
## list of successors

def successors(graph,vertex):
        
### Return the list of successors of a node.
        
        l = []
        if vertex in vertices(graph):
                for edge in edges(graph):
                        if edge[0]==vertex:
                                l=l+[edge[1]]
        return l

## find the max and min element and its index in a list
####
def max_element(L):
    m=L[0]
    for i in L:
        if i>m:
            m=i
    return m

def min_element(L):
    m=L[0]
    for i in L:
        if i<m:
            m=i
    return m

def max_index(L):
    m = L[0]
    s = 0
    for i in range(len(L)):
        if L[i]>m:
            m = L[i]
            s = i
    return s
######            
            
#### find the shortest path between 2 nodes           
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in vertices(graph):
        return None
    shortest = None
    for node in successors(graph,start):
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest
    
    
## find the centroid of a graph
## the centroid of a graph is defined as the node that minimize the maximum distance between 2 nodes
def find_centroid(g):
    path={}
    for source in vertices(g):
        s=[]
        path_length = []
        for nodes in vertices(g):
            if nodes != source:
                path_length = path_length + [len(find_shortest_path(g, source, nodes))]
        if len(path_length)>0:
            for i in path_length:
                s = s + [i]
                path[source] = max_element(s)
    nb = nbVertex(g)
    centroid = vertices(g)[0]
    for elm in path:
        if path[elm] < nb:
            nb = path[elm]
            centroid = elm
    return centroid 



## find all the successors of a centroid in a subgraph    
def find_successors(G,centroid,node):
    list_successors=[]
    s = 0
    if s < nbVertex(G):
        for successor in successors(G,node):
            if successor not in list_successors:
                s=s+1            
                list_successors = list_successors +[successor]
                if centroid in list_successors:              
                    list_successors.remove(centroid)
            for i in list_successors :
                find_successors(G,centroid,i)
    else : 
        return [node] + list_successors
    return [node] + list_successors

## find all the lists of the nodes that make all the subgraphs of a centroid
def node_subgraph(G,centroid):
    nodes = []
    for vertex in successors(G,centroid):
        nodes = nodes +[find_successors(G,centroid,vertex)]
    return nodes
    
## find all the subgraphs of a node 
## Input : graph and a node 
## Output : list of nodes of the subgraph             
def subgraph(g,vertex):
    node =[vertex]
    if successors(g,vertex)==centroid:
        return [centroid] + node 
    if vertex != centroid:
        for i in successors(g,vertex):
            if vertex != centroid:
                if i not in node and i!= centroid:
                    node = node + [i]
                node = node + subgraph(g,i)
    return list(set(node)) 
            
 
### generate a subgraph using the list of nodes of the subgraph
## Input: list of nodes of a sugbraph
## Output: subgraph
def extract_graph(vertices):
    edges = []
    for i in vertices:
        for elm in p:
            if elm[0]==i and elm[1] in vertices and elm not in edges:
                edges = edges + [elm]
    return initGraph(vertices,edges)          


### find all the subgraphs of a centroid

def find_subgraph(g,centroid):
    p= edges(g)
    subvertices = []
    sub_graphs =[] 
    for elm in successors(g,centroid):
        subvertices = subvertices + [subgraph(g,elm)]
    for subvert in subvertices:
        sub_graphs = sub_graphs + [extract_graph(subvert)]
    return sub_graphs
        
        
### find all the path between 2 nodes        
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in vertices(graph):
            return []
        paths = []
        for node in successors(graph,start):
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

### find the minimum cost of a path between 2 nodes 
def cost_function(graph, start, end):
    L= []
    for i  in find_all_paths(graph, start, end):
        s=0
        for j in range(len(i)-1):
            for edge in p:
                if edge[0]==i[j] and edge[1]==i[j+1]:
                    s = s + edge[2]
        L=L+[s]
    return min_element(L)

### find the cost of a path between the centroid and all the vertices
def cost_graph(graph,centroid):
    L=[]
    for vertex in vertices(graph):
        if vertex!= centroid:
            L=L+ [cost_function(graph,centroid,vertex)]
    return max_element(L)
                
## find the 1-center of the graph  
### Input : graph
### Output : center
def find_center(g):
    k=0
    p= edges(g)
    cost = []
    centroid = find_centroid(g)    
    subgraphs = find_subgraph(g,centroid)
    if len(subgraphs)>1:
        for i in subgraphs:
            cost = cost + [cost_graph(i, centroid)] 
            k = max_element(cost)  
        if cost.count(k) == 2:
            return centroid
        if cost.count(k) == 1:
            new_graph = subgraphs[max_index(cost)]
            p = edges(new_graph)
            centroid = find_centroid(new_graph)
            return find_center(new_graph)
    else:
        return centroid


g1 = initGraph([1,2,3,4,5,6,7,8,9,10],[(10,2,25),(3,10,1),(3,4,10),(3,1,6),(3,5,8),(2,6,25),(1,7,1),(4,8,4),(5,9,1),(6,3,1),(7,3,1),(8,3,1),(9,3,1)])
p = edges(g1)
centroid = find_centroid(g1)
find_center(g1) 

g2 = initGraph([1,2,3,4,5],[(3,4,10),(3,2,10),(2,3,1),(4,3,1),(1,3,2),(5,3,1),(3,1,6),(3,5,8)])
p = edges(g2)
centroid = find_centroid(g2)
find_center(g2) 








        
    
            
