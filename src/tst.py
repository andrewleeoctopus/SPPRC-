import networkx as nx
import matplotlib.pyplot as plt

# 创建图
G = nx.Graph()
# 添加一些节点和边，例如：
G.add_nodes_from([1, 2, 3, 4])
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 1)

# 手动定义节点位置
pos = {1: (0, 0), 2: (1, 0), 3: (1, 1), 4: (0, 1)}

# 绘制图形
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k')

# 显示坐标轴
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('on')

# 显示栅格
plt.grid(True)

# 在节点旁边添加坐标标签
for p in pos:
    plt.text(pos[p][0], pos[p][1]+0.05, s=f"{pos[p]}", bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')

# 显示图形
plt.show()