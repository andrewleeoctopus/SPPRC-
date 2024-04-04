import yaml
from networkx import DiGraph
import math as m


def create_map(mode=2):
    env_config = '../config/config3.yaml'
    with open(env_config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    targets = config['targets']
    if mode == 2:  # 2 对应有必经要求的情况，1对应无必经要求
        num_target = len(targets)  # num_target用于mode=2时资源维度的计算
    else:
        num_target = 0  # mode=1时，目标点上的资源维度为0
    stations = config['charge_stations']
    num_station = len(stations)
    G = DiGraph(directed=True, n_res=2 + num_target)  # 第一个维度为时间，第二个维度为资源, 后面的资源为是否访问某节点
    resl = [0 for _ in range(num_target)]
    resu = [1 for _ in range(num_target)]
    G.add_node(0, pos=[0.0, 0.0], res_min=[0, 0] + resl, res_max=[m.inf, 10] + resu)
    for target in targets:
        G.add_node(target['index'], pos=target['position'], res_min=[0, 0] + resl,
                   res_max=[target['time_window'], 10] + resu)

    for node1 in G.nodes:
        for node2 in G.nodes:
            if node1 != node2:
                pos1 = G.nodes[node1]['pos']
                pos2 = G.nodes[node2]['pos']
                dis = m.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                res1 = [0 for _ in range(num_target)]
                res2 = [0 for _ in range(num_target)]
                if num_target != 0:
                    res1[node1 - 1] = -1
                    res2[node2 - 1] = -1
                if node2 != 0:
                    G.add_edge(node1, node2, res_cost=[dis, dis] + res2)
                if node1 != 0:
                    G.add_edge(node2, node1, res_cost=[dis, dis] + res1)

    for station in stations:
        G.add_node(station['index'], pos=station['position'], res_min=[0, 0] + resl,
                   res_max=[m.inf, 10] + resu)
        for target in targets:
            pos1 = target['position']
            pos2 = station['position']
            dis = m.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
            G.add_edge(target['index'], station['index'], res_cost=[dis, dis] + resl)
        # 起始点也可以连到充电站
        pos1 = [0.0, 0.0]
        pos2 = station['position']
        dis = m.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        G.add_edge(0, station['index'], res_cost=[dis, dis] + resl)

        for i in range(10):
            station_update = station['index'] + str(i + 1)
            G.add_node(station_update, pos=station['position'], res_min=[0, 0] + resl,
                       res_max=[m.inf, 10] + resu)
            G.add_edge(station['index'], station_update, res_cost=[i + 1, -i - 1] + resl)
            for target in targets:
                pos1 = target['position']
                pos2 = station['position']
                dis = m.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                res1 = [0 for _ in range(num_target)]
                if num_target != 0:
                    res1[target['index'] - 1] = -1
                G.add_edge(station_update, target['index'], res_cost=[dis, dis] + res1)
        # 充电站出边连到充电站！
    for station1 in stations:
        for i in range(10):
            station_update = station1['index'] + str(i + 1)
            for station2 in stations:
                if station1 != station2:
                    pos1 = station1['position']
                    pos2 = station2['position']
                    dis = m.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                    G.add_edge(station_update, station2['index'], res_cost=[dis, dis] + resl)
    return G
