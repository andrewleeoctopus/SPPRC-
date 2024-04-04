from create_map import create_map
from SPPRC import SP
from SPClass_old import SPAll
import matplotlib.pyplot as plt
import networkx as nx

G = create_map()
pos = {node: tuple(data['pos']) for node, data in G.nodes(data=True)}
# 创建一个新的位置字典，确保每个位置只显示一个节点编号
pos_filtered = {}
seen_positions = set()
for node, position in pos.items():
    if position not in seen_positions:
        pos_filtered[node] = position
        seen_positions.add(position)

# 使用分开的函数绘制节点、边和节点标签
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=70)
nx.draw_networkx_edges(G, pos, edge_color='k')
# 仅为pos_filtered中的节点准备标签
labels = {node: str(node) for node in pos_filtered.keys()}
# 使用过滤后的标签集绘制标签
nx.draw_networkx_labels(G, pos_filtered, labels=labels, font_weight='bold')
plt.axis('equal')
plt.show()
sp = SP(G)
sp.solve(0)
sp.get_best_solution()
# # 绘制图
# nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
# # 显示图形
# plt.show()
