import argparse

from MaxCut import MaxCut
from Graph import Graph
from Edge import Edge

from matplotlib import pyplot as plt
import networkx as nx

parser = argparse.ArgumentParser(description='QOSF mentorship program task 4')
parser.add_argument('-s', '--shots', help="Set the number of shots", type=int, default=512)
parser.add_argument('-d', '--depth', help="Set the depth of the Quantum circuit", type=int, default=2)
parser.add_argument('-n', '--num', help="Set the number of qubits", type=int, default=3)
parser.add_argument('-i', '--iter', help="Set the number of iterations for optimal gamma and beta", type=int, default=1000)
parser.add_argument('-g', '--graph', help="Select the type of graph" , type=str, default="cool_graph")



def main():
    args = parser.parse_args()
    shots = args.shots
    depth = args.depth
    num = args.num
    graph = args.graph
    max_iter = args.iter

    if graph == "triangle":
        edge_list = [Edge(0,1,2), Edge(1,2,1), Edge(2,0,2)]
        num = 3
    elif graph == "square":
        edge_list = [Edge(0,1,2), Edge(1,2,1), Edge(2,3,1), Edge(3,0,2)]
        num = 4
    else:
        edge_list = [Edge(0, 1), Edge(1, 2), Edge(2, 3), Edge(3,4), Edge(4,0), Edge(1,3), Edge(2,4)]
        num = 5

    G = nx.Graph()

    for z in edge_list:
        G.add_edge(str(z.start_node), str(z.end_node))

    nx.draw(G)
    plt.savefig('graph.png')
    plt.clf()

    maxcut = MaxCut(edge_list, num, shots, depth)
    maxcut.do_max_cut(max_iter)
    
    print("Executed successfully")
    
if __name__ == "__main__":
    main()