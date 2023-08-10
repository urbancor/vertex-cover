# Vertex cover

I implemented 4 different approximation algorithms for the vertex cover problem:
* **Naive Algorithm**: It takes an edge one by one and adds one vertex to the vertex cover. Then removes all edges with this vertex.
* **Greedy Algorithm**: On each step it takes the vertex with the highest degree. Then removes all edges with this vertex.
* **2-APX Algorithm**: It adds both vertices of an edge to the vertex cover. Then removes all edges with one of the vertices.
* **Linear Programming**: I translate the problem in a form for linear programming solver. Then use installed lp solver to solve the problem. Then I read the output of the solver to construct a valid solution.

In the pdf file you can see how many vertices are in a vertex cover for each algorithm.