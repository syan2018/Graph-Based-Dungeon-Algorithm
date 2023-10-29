import random

class PathSequence:
    """
    Represents the sequence of directions for a path between two nodes.
    """
    def __init__(self, node_pair, sequence="XYZ"):
        self.node_pair = node_pair  # Tuple of nodes (u, v)
        self.sequence = sequence    # Direction sequence (e.g., "XYZ", "XZY", ...)
    
    def get_segments(self, positions):
        """
        Compute the segments for the path based on the sequence and node positions.
        """
        u, v = self.node_pair
        x1, y1, z1 = positions[u]
        x2, y2, z2 = positions[v]
        
        if self.sequence == "XYZ":
            mid1 = (x2, y1, z1)
            mid2 = (x2, y2, z1)
        elif self.sequence == "XZY":
            mid1 = (x2, y1, z1)
            mid2 = (x2, y1, z2)
        elif self.sequence == "YXZ":
            mid1 = (x1, y2, z1)
            mid2 = (x2, y2, z1)
        elif self.sequence == "YZX":
            mid1 = (x1, y2, z1)
            mid2 = (x1, y2, z2)
        elif self.sequence == "ZXY":
            mid1 = (x1, y1, z2)
            mid2 = (x2, y1, z2)
        elif self.sequence == "ZYX":
            mid1 = (x1, y1, z2)
            mid2 = (x1, y2, z2)
        else:
            raise ValueError("Invalid sequence")
        
        segments = [((x1, y1, z1), mid1), (mid1, mid2), (mid2, (x2, y2, z2))]
        
        return segments
    
    def set_random_sequence(self):
        """
        Set a random direction sequence.
        """
        self.sequence = random.choice(["XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"])
        