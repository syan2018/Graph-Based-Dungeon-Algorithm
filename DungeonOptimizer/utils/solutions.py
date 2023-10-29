from utils.sequences import PathSequence


# 解决方案定义
# 包含图、点坐标、点连接等关系
class Solution:
    def __init__(self, graph, positions, path_sequences=None):
        self.graph = graph
        self.positions = positions
        self.path_sequences = path_sequences or self._initialize_path_sequences()

    def _initialize_path_sequences(self):
        path_sequences = {}
        for u, v in self.graph.edges():
            if (v, u) not in path_sequences:  # Check to avoid duplicates for undirected edges
                path_seq = PathSequence((u, v))
                path_seq.set_random_sequence()
                path_sequences[(u, v)] = path_seq
        return path_sequences