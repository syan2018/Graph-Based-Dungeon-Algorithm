
import networkx as nx
import random

import matplotlib.pyplot as plt
import numpy as np


def generate_graph(n, min_degree, max_degree, target_avg_degree):
    # Start with a cycle graph
    G = nx.cycle_graph(n)
    
    # List of nodes
    nodes = list(G.nodes)

    # Add edges until the average degree is reached or it is not possible to add more edges
    while True:
        # Compute the current average degree
        degrees = [G.degree(n) for n in G.nodes()]
        avg_degree = sum(degrees) / len(degrees)

        # If the target average degree is reached, stop
        if avg_degree >= target_avg_degree:
            break

        # Select a random node
        node = random.choice(nodes)

        # If the degree of the node is already the maximum, continue with the next iteration
        if G.degree(node) >= max_degree:
            continue

        # Try to add an edge to another node
        for _ in range(n):
            # Select another random node
            other_node = random.choice(nodes)

            # The other node must be different and not already connected to the node
            if other_node != node and not G.has_edge(node, other_node):
                # The degree of the other node must not be the maximum
                if G.degree(other_node) < max_degree:
                    G.add_edge(node, other_node)
                    break

    # Check the degrees
    degrees = [G.degree(n) for n in G.nodes()]
    min_degree_generated = min(degrees)
    max_degree_generated = max(degrees)
    avg_degree_generated = sum(degrees) / len(degrees)

    # If the graph doesn't satisfy the conditions, return None
    if min_degree_generated < min_degree or max_degree_generated > max_degree or avg_degree_generated < target_avg_degree:
        return None, None, None, None

    return G, min_degree_generated, max_degree_generated, avg_degree_generated



class DungeonRGT:

    def __init__(self, n=10, min_resistance=1, max_resistance=10, total_resistance=(10, 50), max_iter=3):
        self.n = n  # 节点数量
        self.graph = nx.DiGraph()  # 初始化有向图
        self.graph.add_node(0, resistance=0)  # 添加起始节点，阻力系数为0
        self.min_resistance = min_resistance  # 阻力系数的最小值
        self.max_resistance = max_resistance  # 阻力系数的最大值
        self.total_resistance = total_resistance  # 所有路径上阻力系数之和的范围
        self.max_iter = max_iter  # 最大迭代次数
        self.end_node = None  # 终止节点
        self.old_score = -np.inf  # 旧的评分
        

    def add_bi_edge(self,graph,u,v):
        graph.add_edge(u,v)
        graph.add_edge(v,u)

    def _generate_nodes_and_edges(self):
        # Initialize the graph as a cycle graph
        G, min_degree, max_degree, avg_degree = generate_graph(self.n,min_degree=2,max_degree=4,target_avg_degree=3)
        
        self.graph = nx.DiGraph(G)
        
        # Add resistance to each node
        for i in range(self.n):
            resistance = random.uniform(self.min_resistance, self.max_resistance)
            self.graph.nodes[i]['resistance'] = resistance

        # Transfer the resistance from nodes to edges
        for u, v in self.graph.edges:
            self.graph[u][v]['weight'] = (self.graph.nodes[v]['resistance'] + self.graph.nodes[u]['resistance'])/2

        # print(self.graph)


    def _make_graph_diverse(self, graph):
        # 使地牢设计多样化
        shortest_path = nx.shortest_path(graph, 0, self.end_node, weight='weight')  # 获取最短路径

        if len(shortest_path) > 1:
            idx = random.randint(0, len(shortest_path) - 2)  # 随机选择一个索引
            u, v = shortest_path[idx], shortest_path[idx + 1]
            if graph.has_edge(u, v):  # 如果含正向边
                tmp_graph = graph.copy()
                tmp_graph.remove_edge(u, v)  # 删除正向边
                new_score = self._evaluate_graph(tmp_graph, 0, self.end_node)
                print(f"new_score:{new_score},old_score:{self.old_score}")
                if new_score > self.old_score:
                    self.old_score = new_score
                    return tmp_graph
        return graph


    def _set_end_node(self):
        # 设置终止节点
        nodes = list(self.graph.nodes)[1:]  # 获取除起始节点外的所有节点
        best_score = self.old_score  # 初始最优评分设为old_score
        best_node = None  # 初始化最优节点为None

        for node in nodes:
            node_score = self._evaluate_graph(self.graph, 0, node)  # 计算每个节点的评分
            if node_score > best_score:  # 如果节点的评分超过当前最优评分
                best_score = node_score  # 更新最优评分
                best_node = node  # 更新最优节点

        # 设置阻力系数为0，将最优节点设为终止节点
        self.end_node = best_node
        self.graph.nodes[best_node]['resistance'] = 0


    def _evaluate_graph(self, graph, start_node, end_node):

        # 判断是否存在至少一条从终点到起点的逆向路径
        if not nx.has_path(graph, end_node, start_node):
            return -np.inf  # 如果不存在这样的路径，则返回负无穷大

        # 评价图
        paths = list(nx.all_simple_paths(graph, start_node, end_node))  # 获取所有从起始节点到终止节点的路径
        
        resistances = [sum(graph.nodes[node]['resistance'] for node in path) for path in paths]  # 计算每条路径的阻力系数总和
        path_lengths = [len(path) for path in paths]  # 计算每条路径的长度

        # 计算路径之间的相似度
        similarity = 0
        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                similarity += len(set(paths[i]).intersection(paths[j])) / len(set(paths[i]).union(paths[j]))
        similarity /= (len(paths) * (len(paths) - 1)) / 2 if len(paths) > 1 else 1  # 避免除以0

        # 目标函数：方差缩小，避免相似
        score = -np.var(resistances) * (1 - similarity)
        
        return score


    def generate(self):
        # 生成图
        self._generate_nodes_and_edges()  # 生成节点和边
        self._set_end_node()  # 设置终止节点
        for _ in range(self.max_iter):

            shortest_path = nx.shortest_path(self.graph, 0, self.end_node, weight='weight')  # 获取最短路径
            path_resistance = sum(self.graph[u][v]['weight'] for u, v in zip(shortest_path[:-1], shortest_path[1:]))  # 计算路径阻力系数之和
            print("path resistance",path_resistance)
            # 最短路需要修饰
            if path_resistance <= 15:
                print("diverse!", shortest_path)
                self.graph = self._make_graph_diverse(self.graph)  # 使地牢设计多样化
            else:
                return

    def draw(self):
        def is_bidirectional(edge):
            # Check if the reverse of the edge exists in the graph
            return (edge[1], edge[0]) in self.graph.edges

        pos = nx.spring_layout(self.graph, seed=42, k=1)  # 布局
        nx.draw_networkx_nodes(self.graph, pos, node_color=['red' if node in [0, self.end_node] else 'blue' for node in self.graph.nodes])  # 绘制节点
        nx.draw_networkx_labels(self.graph, pos)  # 绘制节点标签

        # 绘制边
        for edge in self.graph.edges:
            color = 'black' if is_bidirectional(edge) else 'red'
            nx.draw_networkx_edges(self.graph, pos, edgelist=[edge], edge_color=color)  # 绘制边，设置颜色，并添加箭头

        plt.show()  # 显示图


    def print_all_path_lengths(self):
        # 计算并打印所有路径以及对应的"长度"（阻力系数之和）
        paths = list(nx.all_simple_paths(self.graph, 0, self.end_node))  # 获取所有从起始节点到终止节点的路径
        for path in paths:
            path_length = sum(self.graph.nodes[node]['resistance'] for node in path)  # 计算每条路径的阻力系数之和
            print("Path: ", path, "Resistance: ", path_length)



