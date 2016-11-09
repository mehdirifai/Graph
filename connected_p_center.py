# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 18:09:32 2014

@author: mehdirifai
"""

import networkx as nx

G = nx.Graph()
for i in range(7):
    G.add_edge(i,5,weight = 4)

G.remove_edge(5,5)   
G.add_edge(1,8,weight = 1)
G.add_edge(8,147,weight = 9)
G.add_edge(8,146,weight = 19)
G.add_edge(8,145,weight = 6)
G.add_edge(0,455,weight = 7)
nx.draw(G)




def findFartherPair(G):
    
    mat = nx.all_pairs_dijkstra_path_length(G)
    maxDist = 0
    farther = [0,0]
    for i in G.nodes():
        for j in G.nodes():
            if mat[i][j] > maxDist:
                farther = [i,j]
                maxDist = mat[i][j]
    return {'fartherPair': farther , 'maxDist': maxDist ,
            'path':nx.dijkstra_path(G,farther[0],farther[1])}
    
   
def findMiddle(G, path ,dist_path):
    # input: a path = a list of vertces , dist_path = length of the path
    d = 0
    for i in range(len(path)-1):
        v1 = path[i]
        v2 = path[i+1]
        w = G.edge[v1][v2]['weight']
        d = d + w
        if d > dist_path/2:
            return {'v1':i,'d1':d-w,'v2':i+1,'d2':d }
    return -1
    
def findNearestVertexToMiddle(G):

    fartherPair = findFartherPair(G)
    path = fartherPair['path']
    dist_path = fartherPair['maxDist']      
    mid = findMiddle(G, path ,dist_path)
    d1 = mid['d1']
    d2 = mid['d2']
    if dist_path/2 - d1 <= d2 - dist_path/2 :
        return { 'root': mid['v1'] , 'd1':d1 , 'd2':d2 , 'dist_path' : dist_path}
    else:
        return { 'root': mid['v2'] , 'd1':d1 , 'd2':d2 , 'dist_path' : dist_path}
    
    
def categories(G):
    
    leaves = []
    root = findNearestVertexToMiddle(G)['root']
    innerNodes = []
    degrees = G.degree()
    for n,d in degrees.items():
        if d == 1 and n != root:
            leaves.append(n)
        if d > 1 and n!=root:
            innerNodes.append(n)
    return {'leaves':leaves , 'root':root, 'innerNodes':innerNodes}
 
def findChildrenAndPar(G,node):
    root = findNearestVertexToMiddle(G)['root']
    if node == root :
        parent = -1 # no parent
        children = G.neighbors(node)
        return {'children':children , 'parent':parent}
    neighbors = G.neighbors(node)
    d = nx.shortest_path_length(G,source=root,target=node)
    children = []
    parent = -1 
    if len(neighbors) == 1:
        parent = neighbors[0] 
        return {'children':children , 'parent':parent}
    else:
        for neighb in neighbors:
            if nx.shortest_path_length(G,source=root,target=neighb) >d :
                children.append(neighb)
            else: 
                parent = neighb
        return {'children':children , 'parent':parent}
            
def computeMu(G):
     categ = categories(G)
     mu_nodes = {}
     print categ['leaves']
     print categ['innerNodes']
     print categ['root']
     for leaf in categ['leaves']:
         parent_leaf = findChildrenAndPar(G,leaf)['parent']
         mu_nodes[leaf] = G.edge[leaf][parent_leaf]['weight']
     #print mu_nodes
     innerSorted = sortByDistToRoot(G, categ['root'], categ['innerNodes'])
     #print innerSorted
     for inner in reversed(innerSorted):
         #print ('inner' + str(inner))
         parent_inner = findChildrenAndPar(G,inner)['parent']
         children_inner = findChildrenAndPar(G,inner)['children'] 
         w = G.edge[inner][parent_inner]['weight']
         maxi = 0
         for child in children_inner:
            # print child
             if mu_nodes[child] > maxi:
                 maxi = mu_nodes[child] 
         mu_nodes[inner] = maxi + w
     children_root = findChildrenAndPar(G,categ['root'])['children']
     maxx = 0
     for child in children_root:
         if mu_nodes[child] > maxx:
                 maxx = mu_nodes[child] 
     mu_nodes[categ['root']] = maxx
     return mu_nodes
     
     
def sortByDistToRoot(G, root, innerNodes):
    innerSorted = []
    for inner in innerNodes:
        innerSorted.append((inner,nx.shortest_path_length(G,source=root,target=inner)))
    innerSorted = sorted(innerSorted , key = lambda x: x[1])     
    innerSorted = [inner[0] for inner in innerSorted]
    return innerSorted
    #sorted from the farthest to the root to the closest
    

cat = categories(G)    
print sortByDistToRoot(G, cat['root'], cat['innerNodes'])  
#print cat['innerNodes']
    
def connectedPCenter(G , p):
    nbNodes = G.number_of_nodes()
    print nbNodes
    print p 
    dic = computeMu(G)
    list_tuple = []
    for n,mu in dic.items():
        list_tuple.append((n,mu))
    
    list_tuple = sorted(list_tuple,key = lambda x : x[1])
    print list_tuple
    p_centers = []
    i = 0
    for tup in list_tuple:
        if i >nbNodes-p-1:        
            p_centers.append(tup[0])
        i = i+1
    
    '''
    for pc in p_centers:        
        if i > nbNodes-p:            
            res.append(pc)
            i = i+1
    '''
    return p_centers