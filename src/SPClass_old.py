import heapq


class LexicographicalPriorityQueue:
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
    def __init__(self, node, res, weight, time_stamp, previous_label):
        self.node = node
        self.res = res
        self.weight = weight
        self.time_stamp = time_stamp
        self.previous_label = previous_label

    def __lt__(self, other):
        # 比较函数，根据res的字典序进行比较
        return self.res < other.res

    def print_path(self):
        if self.previous_label is not None:
            self.previous_label.print_path()
            print(' --> ')
        print(str(self.node) + ' ' + str(self.res) + ' ' + str(self.weight))

    def get_path(self):
        if self.previous_label is None:
            return [self.node]
        else:
            path = self.previous_label.get_path()
            path.append(self.node)
            return path


class SPOne:
    def __init__(self, G):
        self.G = G
        self.time_stamp = 0
        self.n_res = G.graph['n_res']
        self.labels = {n: [] for n in list(G.nodes)}

    def new_label(self, node, previous_label=None):
        # FORBID CYCLES
        label = previous_label
        while label is not None:
            if label.node == node:
                return None
            label = label.previous_label
        res = []
        weight = 0
        if previous_label is None:
            res = [1 for r in range(self.n_res)]
            # 对于目前的情况， 我将初始的所有点资源res置为1，到达则更置为0，以便于dominate比大小，以后记得改这里
            res[0] = 0
            res[1] = 0
        else:
            res = [previous_label.res[r] for r in range(self.n_res)]
            edge = self.G.edges[previous_label.node, node]
            weight = previous_label.weight + edge['weight'] + self.G.nodes[node]['weight']
            for r in range(self.n_res):
                res[r] += edge['res_cost'][r]
                if 'res_max' in self.G.nodes[node]:
                    if res[r] > self.G.nodes[node]['res_max'][r]:
                        return None
                if 'res_min' in self.G.nodes[node]:
                    if res[r] < self.G.nodes[node]['res_min'][r]:
                        res[r] = self.G.nodes[node]['res_min'][r]

        return Label(node, res, weight, self.time_stamp, previous_label)

    def dominates(self, label1, label2):
        if label1.weight < label2.weight:
            return True
        # 只有全部元素1都小于等于2, 等于也输出dominate， 便于在undominate中判断
        for r in range(self.n_res):
            if label1.res[r] > label2.res[r]:
                return False
        return True

    def solve(self, start, end):
        self.time_stamp = 0
        self.labels = {n: [] for n in list(self.G.nodes)}
        label = self.new_label(start, None)
        self.labels[start].append(label)
        new_labels = [label]
        labels = new_labels
        while len(labels) > 0:
            new_labels = []
            for previous_label in labels:
                from_node = previous_label.node
                for to_node, datadict in self.G.adj[from_node].items():
                    new_label = self.new_label(to_node, previous_label)
                    if new_label is None:
                        continue

                    dominates = False
                    if len(self.labels[to_node]) == 0:
                        dominates = True
                    else:
                        for label in self.labels[to_node]:
                            if self.dominates(new_label, label):
                                # remove label
                                if label.time_stamp == self.time_stamp and to_node != end:
                                    # also remove from new
                                    new_labels.remove(label)
                                self.labels[to_node].remove(label)
                                dominates = True
                    if dominates:
                        self.labels[to_node].append(new_label)
                        if to_node != end:
                            new_labels.append(new_label)

            self.time_stamp += 1
            labels = new_labels
            print(f'Iteration {self.time_stamp} found {len(labels)} new labels')


class SPAll(SPOne):
    def __init__(self, G):
        super().__init__(G)
        self.H = LexicographicalPriorityQueue()

    def undominate(self, L, l):
        if len(L) == 0:
            return True
        else:
            for label in L:
                if self.dominates(label, l):
                    return False
            return True

    def solve_all(self, start):
        self.H = LexicographicalPriorityQueue()
        self.labels = {n: [] for n in list(self.G.nodes)}
        label = self.new_label(start, None)
        self.labels[start].append(label)
        self.H.push(label)
        while not self.H.is_empty():
            label_min = self.H.pop()
            for to_node, datadict in self.G.adj[label_min.node].items():
                new_label = self.new_label(to_node, label_min)
                if new_label is None:
                    continue

                if self.undominate(self.labels[to_node], new_label):
                    self.H.push(new_label)
                    for label in self.labels[to_node]:
                        if self.dominates(new_label, label):
                            self.labels[to_node].remove(label)
                    self.labels[to_node].append(new_label)

    # 第一个为时间，第二个为资源，选出时间最小的
    def get_best_solution(self):
        G = LexicographicalPriorityQueue()
        for node in self.G.nodes:
            for label in self.labels[node]:
                if all(x == 0 for x in label.res[2:]):
                    G.push(label)
        # while not G.is_empty():
        #     label_best = G.pop()
        #     label_best.print_path()
        label_best = G.pop()
        label_best.print_path()
