from networkx import DiGraph
from numpy import array
import math as m
from SPClass_old import SPAll, SPOne

G = DiGraph(directed=True, n_res=2)  # 第一个维度为时间，第二个维度为资源
G.add_edge('S', 'A', res_cost=array([5, 5]), weight=0.0)
G.add_edge('A', 'S', res_cost=array([5, 5]), weight=0.0)
G.add_edge('S', 'B', res_cost=array([10, 10]), weight=0.0)
G.add_edge('B', 'S', res_cost=array([10, 10]), weight=0.0)
G.add_edge('B', 'T', res_cost=array([1, 1]), weight=0.0)
G.add_edge('T', 'B', res_cost=array([1, 1]), weight=0.0)
G.add_edge('A', 'T', res_cost=array([9, 9]), weight=0.0)
G.add_edge('T', 'A', res_cost=array([9, 9]), weight=0.0)
G.add_edge('A', 'station', res_cost=array([3, 3]), weight=0.0)
G.add_edge('station', 'A', res_cost=array([3, 3]), weight=0.0)
G.add_edge('S', 'station', res_cost=array([10, 10]), weight=0.0)
G.add_edge('station', 'S', res_cost=array([10, 10]), weight=0.0)
G.add_edge('T', 'station', res_cost=array([7, 7]), weight=0.0)
G.add_edge('station', 'T', res_cost=array([7, 7]), weight=0.0)
G.add_edge('station', 'station#', res_cost=array([10, -10]), weight=0.0)
G.add_edge('station#', 'S', res_cost=array([10, 10]), weight=0.0)
G.add_edge('station#', 'T', res_cost=array([7, 7]), weight=0.0)
G.add_edge('station#', 'A', res_cost=array([3, 3]), weight=0.0)

G.add_node('S', res_min=[0, 0], res_max=[m.inf, 10], weight=0.0)
G.add_node('A', res_min=[0, 0], res_max=[6, 10], weight=0.0)
G.add_node('B', res_min=[0, 0], res_max=[9, 10], weight=0.0)
G.add_node('station', res_min=[0, 0], res_max=[m.inf, 10], weight=0.0)
G.add_node('station#', res_min=[0, 0], res_max=[m.inf, 10], weight=0.0)
G.add_node('T', res_min=[0, 0], res_max=[m.inf, 10], weight=0.0)

sp = SPAll(G)
sp.solve_all('S')
sp.get_best_solution('T')
# for l in sp.labels['T']:
#     print(f'{l.weight} for path {l.get_path()}')
