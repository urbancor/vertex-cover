import networkx as nx
from scipy import optimize as opt
import os

### NAVODILA ZA POGANJANJE ###
# v direktoriju, kjer imamo to datoteko mora obstajati mapa tests, v kateri so grafi
# grafi morajo biti imenovani g01.graph, g02.graph, ..., g20.graph (enako kot so bili podani testi)
# poženemo z ukazom python3 vertex_cover.py
# rezultati se izpišejo v datoteko results.txt
# ustvarili se bosta tudi dve datoteki lp.lp in lp.out, ki sta potrebni za reševanje LP problema
# lp.lp je datoteka, ki jo pošljemo solverju, lp.out pa je datoteka, ki jo solver ustvari

def my_round(x):
    if x < 0.5:
        return 0
    else:
        return 1

def read_graph(path):
    G = nx.read_edgelist(path, nodetype=int)
    return G

def read_results(path):
    results = []
    with open(path, "r") as f:
        line = f.readline() #empty line
        line = f.readline() #value of the minimizing function
        split = line.split(" ")
        value = float(split[len(split)-1])
        line = f.readline() #empty line
        line = f.readline() #text line
        while line:
            line = f.readline()
            if line:
                split = line.split(" ")
                var_value = float(split[len(split)-1])
                results.append(var_value)
                #print(line)
    return (results, value) 

# 2apx algorithm for vertex cover problem
def apx_vc(path):
    #read the graph
    G = read_graph(path)
    #then do the naive vertex cover algorithm
    #initialize the vertex cover set
    vertex_cover = set()
    #initialize the uncovered edges
    uncovered_edges = set(G.edges())
    #while there are uncovered edges
    while uncovered_edges:
        #pick an uncovered edge
        edge = uncovered_edges.pop()
        #add the two vertices of the edge to the vertex cover set
        vertex_cover.add(edge[0])
        vertex_cover.add(edge[1])
        #remove all edges covered by the two vertices
        uncovered_edges = [e for e in uncovered_edges if e[0] not in vertex_cover and e[1] not in vertex_cover]
    return vertex_cover

#naive algorithm for vertex cover problem
def naive_vc(path):
    #read the graph
    G = read_graph(path)
    #then do the vertex cover:
    #initialize the vertex cover set
    vertex_cover = set()
    #initialize the uncovered edges
    uncovered_edges = set(G.edges())
    #nodes = set(G.nodes())
    #take an edge and add node to the vertex cover set
    while uncovered_edges:
        node = uncovered_edges.pop()[0]
        vertex_cover.add(node)
        uncovered_edges = [e for e in uncovered_edges if e[0] not in vertex_cover and e[1] not in vertex_cover]
    return vertex_cover

#greedy algorithm for vertex cover problem: on each step take the vertex with the highest degree and add it to a vertex cover set, then remove all edges covered by this vertex
def greedy_vc(path):
    #read the graph
    G = read_graph(path)
    #then do the vertex cover:
    #initialize the vertex cover set
    vertex_cover = set()
    #initialize the uncovered edges
    uncovered_edges = G.edges()
    nodes = set(G.nodes())
    #take an edge and add node to the vertex cover set
    while uncovered_edges:
        #take the node with the highest degree
        degrees = sorted(G.degree, key=lambda x: x[1], reverse=True)
        node = degrees[0][0]
        #remove node from the graph G
        G.remove_node(node)
        vertex_cover.add(node)
        uncovered_edges = [e for e in uncovered_edges if e[0] not in vertex_cover and e[1] not in vertex_cover]
    
    return vertex_cover

def lp_vc(path):
    #read the graph
    G = read_graph(path)
    nodes = set(G.nodes())
    edges = set(G.edges())
    no_of_nodes = len(nodes)

    #c = [1] * no_of_nodes
    #A = []
    lines = []
    minimizing_function = "x1 "
    for i in range(2, no_of_nodes+1):
        minimizing_function += " + x" + str(i)
    lines.append("min: "+minimizing_function+";\n")

    for i in range(no_of_nodes):
        #A.append([0] * no_of_nodes)
        #A[i][i] = -1
        lines.append("x" + str(i+1) + " >= 0;\n")
        lines.append("x" + str(i+1) + " <= 1;\n")
    b = [0] * no_of_nodes
    for edge in edges:
        #new_entry = [0] * no_of_nodes
        #new_entry[edge[0]-1] = -1
        #new_entry[edge[1]-1] = -1
        #A.append(new_entry)
        lines.append("x" + str(edge[0]) + " + x" + str(edge[1]) + " >= 1;\n")
    
    #for i in range(len(edges)):
    #    b.append(-1)

    with open("lp.lp", "w") as f:
        for line in lines:
            f.write(line)
        f.close()
    print("finished writing to file")

    #send the lp.lp file to the solver
    os.system("lp_solve lp.lp > lp.out")

    #read the results
    (results, value) = read_results("lp.out")
    rounded_results = [my_round(x) for x in results]

    return (value, sum(rounded_results))

def main():
    print_lines = []

    for i in range(1,21):
        #print(i)
        path = "./tests/g" + str(i).zfill(2) + ".graph"
        #print(path)
        #G = read_graph(path)

        apx = len(apx_vc(path))
        #print("apx: ", apx)
        naive = len(naive_vc(path))
        #print("naive: ", naive)
        greedy = len(greedy_vc(path))
        #print("greedy: ", greedy)
        lp = lp_vc(path)
        #print("lp: ", lp)
        print_lines.append(path + " | " + str(lp[0]) + " | " + str(lp[1]) + " | " + str(naive) + " | " + str(greedy) + " | " + str(apx) + "\n")

    #write lines to .txt file
    with open("results.txt", "w") as f:
        for line in print_lines:
            f.write(line)


main()
