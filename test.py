import multiple_shortest_distance as msd

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


count = 0
f = "paths_table.txt"
with open(f, "w") as path_file:
    path_file.write("Words".ljust(25) + "Paths".rjust(8) + "Length".rjust(10) + "Nodes".rjust(8))
for t in test_words:
    start = t[0]
    end = t[1]

    min = 1000
    max = 0
    shortest_path = None
    longest_path = None
    path_dict = msd.get_shortest_paths(start, end, True)

    # Calculating nodes of graph in which all synset nodes are
    # traversed via the shortest paths
    nodes = []
    for d in path_dict:
        if path_dict[d][0]!= None and path_dict[d][0] < min:
            min = path_dict[d][0]
            shortest_path = path_dict[d]
        if path_dict[d][0]!= None and path_dict[d][0] > max:
            max = path_dict[d][0]
            longest_path = path_dict[d]

        for p in path_dict[d][2]:
            if p != None:
                for node in p:
                    if node not in nodes:
                        nodes.append(node)
            else:
                ws = d.split("<-->")
                print(ws)
                # To add a word that may be disconnected
                for w in ws:
                    if w not in nodes:
                        nodes.append(w)


    c = len(nodes)
    print("Shortest Path:", shortest_path)
    print("Nodes: ", c)
    print("All paths:", path_dict)

    with open(f, "a") as path_file:
        path_file.write("\n" + (t[0] + "<-->" + t[1]).ljust(25))
        path_file.write(str(shortest_path[1]).rjust(8))
        path_file.write(str(shortest_path[0]).rjust(10) )
        path_file.write(str(c).rjust(8))
    count += 1
