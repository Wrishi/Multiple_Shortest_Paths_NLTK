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
with open("paths.txt","w") as path_file:
        path_file.write("SHORTEST PATHS:\n=======================\n")
for t in test_words:
    print("****************")
    print(count, ': ', t[0], ', ', t[1])
    with open("paths.txt","a") as path_file:
        path_file.write("****************\n"+ str(count) +": " + t[0] + ", " + t[1] + "\n")
    try:
        start = t[0]
        end = t[1]
        d, n, shortest_paths = msd.get_shortest_paths(start, end)
        print("Path: ", shortest_paths)
        print("No. of Paths: ", n)
        print("Distance: ", d)
        with open("paths.txt","a") as path_file:
            path_file.write("Path: " + str(shortest_paths) + "\nNo. of Paths: " + str(n) + "\nDistance: " + str(d) + "\n")
        count += 1
    except AttributeError:
        print("AttributeError!")
        count += 1
        continue
