from nltk.corpus import wordnet as wn


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
        

def get_graph(a,b):
    graph = {}
    hyp = lambda s:s.hypernyms()
    a_tree = a.tree(hyp)
    b_tree = b.tree(hyp)

    #print(a_tree)
    #print(b_tree)
    
    unwind_tree(a_tree, graph)
    unwind_tree(b_tree, graph)

    return graph

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

def get_shortest_paths(graph, start_node, end_node):
    # print("Original Graph: ", graph)
    shortest_paths = []
    shortest_paths.append(find_shortest_path(graph, start_node, end_node))
    # print(shortest_paths)
    
    # for shortest path found, remove node and search for shortest path again
    directed = True
    maybe_still = True
    index = 0
    G = graph.copy()
    while(maybe_still):
        #print("G: ",G)
        
        maybe_still = False
        if shortest_paths[index] == None:
            break
        sp_copy = shortest_paths[index].copy()
        for i in range(0,len(sp_copy)-1):
            g_copy = G.copy()
            
            #print("Initial: ", g_copy)
            #print("Node 1: ", sp_copy[i])
            #print("Node 2: ", sp_copy[i+1])
            #print("Node 1 connections: ", g_copy[sp_copy[i]])
            #print("Node 2 connections: ", g_copy[sp_copy[i+1]])
            
            t = g_copy[sp_copy[i]].copy()
            t.remove(sp_copy[i+1])
            g_copy[sp_copy[i]] = t
            
            if directed == False:
                t = g_copy[sp_copy[i+1]].copy()
                t.remove(sp_copy[i])
                g_copy[sp_copy[i+1]] = t
            
            #print("After removal: ", g_copy)
            shortest_path = find_shortest_path(g_copy, start_node, end_node)
            # print("Shortest Path: ", shortest_path)
            #print("*******************************************")
            if shortest_path != None and shortest_path not in shortest_paths and len(sp_copy) >= len(shortest_path):
                shortest_paths.append(shortest_path)
                index += 1
                maybe_still = True
                G = g_copy
                break
        #print("**************************************")

    return shortest_paths


test_words = [
    ('car', 'automobile'),
    ('gem', 'jewel'),
    ('journey', 'voyage'),
    ('boy', 'lad'),
    ('coast', 'shore'),
    ('asylum', 'madhouse'),
    ('magician', 'wizard'),
    ('midday', 'noon'),
    ('furnace', 'stove'),
    ('food', 'fruit'),
    ('bird', 'cock'),
    ('bird', 'crane'),
    ('tool', 'implement'),
    ('brother', 'monk'),
    ('lad', 'brother'),
    ('crane', 'implement'),
    ('journey', 'car'),
    ('monk', 'oracle'),
    ('cemetery', 'woodland'),
    ('food', 'rooster'),
    ('coast', 'hill'),
    ('forest', 'graveyard'),
    ('shore', 'woodland'),
    ('monk', 'slave'),
    ('coast', 'forest'),
    ('lad', 'wizard'),
    ('chord', 'smile'),
    ('glass', 'magician'),
    ('rooster', 'voyage'),
    ('noon', 'string')
]

"""
list_shortest_paths = []
count = 0
for t in test_words:
    print("****************")
    print(count, ': ', t[0], ', ', t[1])
    with open("paths.txt","a") as path_file:
        path_file.write("****************\n"+ str(count) +": " + t[0] + ", " + t[1] + "\n")
    try:
        start = wn.synset(t[0]+'.n.01')
        end = wn.synset(t[1]+'.n.01')
        start_node = start.lemma_names()[0]
        end_node = end.lemma_names()[0]
        graph = get_graph(start, end)
        shortest_paths = get_shortest_paths(graph, start_node, end_node)
        print("Path: ", shortest_paths)
        print("No. of Paths: ", len(shortest_paths))
        if shortest_paths[0] == None:
            distance = 0
        else:
            distance = len(shortest_paths[0])-1
        print("Distance: ", distance)
        with open("paths.txt","a") as path_file:
            path_file.write("Path: " + str(shortest_paths) + "\nNo. of Paths: " + str(len(shortest_paths)) + "\nDistance: " + str(distance) + "\n")
        list_shortest_paths.append(list_shortest_paths)
        count += 1
    except AttributeError:
        count += 1
        continue
    
"""
dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')
start_node = dog.lemma_names()[0]
end_node = cat.lemma_names()[0]
graph = get_graph(dog, cat)
print(graph)
shortest_paths = get_shortest_paths(graph, start_node, end_node)
print(shortest_paths)
