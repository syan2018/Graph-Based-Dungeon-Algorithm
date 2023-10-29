import random

from utils.evaluation import segments_intersect_without_overlap


# 随机初始化点的位置
def assign_initial_positions(graph):
    """Assign initial positions to nodes in a random manner within the 4x4x4 grid."""
    positions = {}
    available_positions = [(x, y, z) for x in range(4) for y in range(4) for z in range(4)]
    random.shuffle(available_positions)

    for node in graph.nodes():
        positions[node] = available_positions.pop()

    return positions

def generate_valid_initial_positions(graph):

    iteration = 0
    """Generate an initial layout for the graph without overlapping or crossing paths."""
    while True:
        positions = assign_initial_positions(graph)
        valid = True
        
        all_segments = []
        for u, v in graph.edges():
            x1, y1, z1 = positions[u]
            x2, y2, z2 = positions[v]
            
            # Calculate intermediate points for segmented edge
            mid_x, mid_y, mid_z = x1, y2, z1

            segment1 = ((x1, y1, z1), (mid_x, mid_y, mid_z))
            segment2 = ((mid_x, mid_y, mid_z), (x2, y2, z2))
            segment3 = ((x2, y2, z2), (x2, y2, mid_z))

            # Check for overlapping or intersecting segments
            for seg in all_segments:
                if (segments_intersect_without_overlap(seg, segment1) or 
                    segments_intersect_without_overlap(seg, segment2) or 
                    segments_intersect_without_overlap(seg, segment3)):
                    valid = False
                    break

            if not valid:
                break

            all_segments.extend([segment1, segment2, segment3])

        iteration  = iteration + 1

        if valid:
            print("Tried for:" + str(iteration))
            return positions