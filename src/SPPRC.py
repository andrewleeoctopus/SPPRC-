import heapq


class LexicographicalPriorityQueue:  # 字典序优先队列
    def __init__(self):
        self.heap = []

    def push(self, label):
        heapq.heappush(self.heap, label)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0] if self.heap else None

    def is_empty(self):
        return not self.heap


class Label:
    def __init__(self, node, res, previous_label):
        self.node = node  # 当前节点
        self.res = res  # 当前资源
        self.previous_label = previous_label  # 前一个标签

    def __lt__(self, other):
        # 比较函数，根据res的字典序进行比较
        return self.res < other.res

    def print_path(self):
        if self.previous_label is not None:
            self.previous_label.print_path()
            print(' --> ')
        print(str(self.node) + ' ' + str(self.res))

    def get_path(self):
        if self.previous_label is None:
            return [self.node]
        else:
            path = self.previous_label.get_path()
            path.append(self.node)
            return path


class SP:
    def __init__(self, G):
        self.G = G
        self.n_res = G.graph['n_res']
        self.labels = {n: [] for n in list(G.nodes)}
        self.H = LexicographicalPriorityQueue()

    def dominates(self, label1, label2):
        # 不严格dominate，等于也叫做dominate，便于non_dominate判断
        for r in range(self.n_res):
            if label1.res[r] > label2.res[r]:
                return False
        return True

    def non_dominate(self, L, l):
        if len(L) == 0:
            return True
        else:
            for label in L:
                if self.dominates(label, l):
                    return False
            return True

    def new_label(self, node, previous_label=None):
        # # FORBID CYCLES IN OBJECTIVE NODES
        if isinstance(node, int) and node > 0:
            label = previous_label
            while label is not None:
                if label.node == node:
                    return None
                label = label.previous_label
        res = []
        if previous_label is None:
            res = [1 for r in range(self.n_res)]
            # 对于目前的情况， 我将初始的所有点资源res置为1，到达则更置为0，以便于dominate比大小
            res[0] = 0
            res[1] = 0
        else:
            res = [previous_label.res[r] for r in range(self.n_res)]
            edge = self.G.edges[previous_label.node, node]
            for r in range(self.n_res):
                res[r] += edge['res_cost'][r]
                if 'res_max' in self.G.nodes[node]:
                    if res[r] > self.G.nodes[node]['res_max'][r]:
                        return None
                if 'res_min' in self.G.nodes[node]:
                    if res[r] < self.G.nodes[node]['res_min'][r]:
                        res[r] = self.G.nodes[node]['res_min'][r]

        return Label(node, res, previous_label)

    def solve(self, start, end=None):
        self.H = LexicographicalPriorityQueue()
        self.labels = {n: [] for n in list(self.G.nodes)}
        label = self.new_label(start, None)
        self.labels[start].append(label)
        self.H.push(label)
        while not self.H.is_empty():
            label_min = self.H.pop()
            if label_min.node == end:
                continue
            for to_node, datadict in self.G.adj[label_min.node].items():
                new_label = self.new_label(to_node, label_min)
                if new_label is None:
                    continue

                if self.non_dominate(self.labels[to_node], new_label):
                    self.H.push(new_label)
                    for label in self.labels[to_node]:
                        if self.dominates(new_label, label):
                            self.labels[to_node].remove(label)
                    self.labels[to_node].append(new_label)

    # 第一个为时间，第二个为资源，选出时间最小的
    def get_best_solution(self, end=None):
        G = LexicographicalPriorityQueue()
        if end is None:
            for node in self.G.nodes:
                for label in self.labels[node]:
                    if all(x == 0 for x in label.res[2:]):
                        G.push(label)
        else:
            for label in self.labels[end]:
                if all(x == 0 for x in label.res[2:]):
                    G.push(label)
        label_best = G.pop()
        label_best.print_path()
