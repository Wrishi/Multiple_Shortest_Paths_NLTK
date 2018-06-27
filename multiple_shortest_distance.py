from nltk.corpus import wordnet as wn


# Converts Tree provided by synsets to Graphs using recursion
# Input Parameters: tree, graph
# Eg: [a,[b,[c]],[d,[e]]] ==> {a:[b,d], b:[a,c], c:[b], d:[a,e], e:[d]}
def unwind_tree(a_tree, graph):
    inc = []
    inc = a_tree
    index = inc[0].lemma_names()[0]
    if len(inc) > 1:
        for i in range(1,len(inc)):
            value = inc[i][0].lemma_names()[0]
            try:
                graph[index]
            except KeyError:
                graph[index] = []
            
            if value not in graph[index]:
                graph[index].append(value)
            
            try:
                graph[value]
            except KeyError:
                graph[value] = []
            
            if index not in graph[value]:
                graph[value].append(index)

            unwind_tree(inc[i], graph)
    else:
        return
        

# Takes to words and builds a graph connecting 
# the two words using their synsets
# Input Parameters: Two words
def get_graph(a,b):
    # Extended graph for all synsets
    a_syns = wn.synsets(a)
    b_syns = wn.synsets(b)
    
    graph = {}
    hyp = lambda s:s.hypernyms()
    for syn in a_syns:
        a_tree = syn.tree(hyp)
        
        # For synsets whose lemma name does not match with word
        # it is attached to the graph at the node for the given word
        # using an edge
        if syn.lemma_names()[0] != a:
            a_tree = [wn.synset(a+'.n.01'), a_tree]
        
        unwind_tree(a_tree, graph)
    
    for syn in b_syns:
        b_tree = syn.tree(hyp)
        
        # For synsets whose lemma name does not match with word
        # it is attached to the graph at the node for the given word
        # using an edge
        if syn.lemma_names()[0] != b:
            b_tree = [wn.synset(b+'.n.01'), b_tree]
            
        unwind_tree(b_tree, graph)
        
    return graph


# Looks for the shortest path between two nodes in a graph
# Input Parameters: graph, start node, end node
# Returns: shortest path
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    
    return shortest


# Looks for shortest paths between given words from graph built from
# synsets of the word.
# Input Parameters: Two words and binary var indicating 
#                   whether the paths should have any common nodes
# Returns: shortest distance, number of shortest paths 
#          & array of multiple shortest paths
def get_shortest_paths(start_node, end_node, allow_common_nodes=False):
    # Get graph connecting the words from their synsets
    graph = get_graph(start_node, end_node)
    
    shortest_paths = []
    shortest_paths.append(find_shortest_path(graph, start_node, end_node))
    
    # Strategy: For shortest path found, remove node and search for shortest path again
    directed = True     # Whether we want a directed graph. We always do!
    maybe_still = True  # Whether there is a possibility of finding more paths
    index = 0           # Index of shortest_paths array
    G = graph.copy()
    
    while(maybe_still):
        maybe_still = False
        
        # if there are no shortest path found
        if shortest_paths[index] == None:
            break
        sp_copy = shortest_paths[index].copy()
        for i in range(0,len(sp_copy)-1):
            g_copy = G.copy()
            
            t = g_copy[sp_copy[i]].copy()
            t.remove(sp_copy[i+1])
            g_copy[sp_copy[i]] = t
            
            if directed == False:
                t = g_copy[sp_copy[i+1]].copy()
                t.remove(sp_copy[i])
                g_copy[sp_copy[i+1]] = t
            
            shortest_path = find_shortest_path(g_copy, start_node, end_node)
            if shortest_path != None and shortest_path not in shortest_paths and len(sp_copy) >= len(shortest_path):
                shortest_paths.append(shortest_path)
                index += 1
                maybe_still = True
                G = g_copy
                break

    
    # if common nodes are not allowed, such paths are removed from the list
    allowed_shortest_paths = shortest_paths.copy()
    if allow_common_nodes == False and len(allowed_shortest_paths) > 1:
        index = 0
        while index < len(allowed_shortest_paths)-1:
            path = allowed_shortest_paths[index]
            i = index + 1
            while i < len(allowed_shortest_paths):
                if len(list(set(path) & set(allowed_shortest_paths[i]))) > 2:
                    allowed_shortest_paths.remove(allowed_shortest_paths[i])
                else:
                    i += 1
            
            index += 1
            
    num_shortest_paths = len(allowed_shortest_paths)
    if allowed_shortest_paths[0] == None:
        distance = 0
    else:
        distance = len(allowed_shortest_paths[0]) - 1       

    return distance, num_shortest_paths, allowed_shortest_paths


