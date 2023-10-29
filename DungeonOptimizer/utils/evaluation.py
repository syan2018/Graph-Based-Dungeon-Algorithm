import numpy as np

def segments_intersect_without_overlap(segment1, segment2):
    """
    Check if two line segments intersect.
    This function currently assumes that the segments are either horizontal or vertical 
    (i.e., aligned with the x, y, or z axis), as is the case with our dungeon layout.
    """
    # Unpack segments
    (x1, y1, z1), (x2, y2, z2) = segment1
    (x3, y3, z3), (x4, y4, z4) = segment2

    # Check for intersection along X-axis
    if x1 == x2 == x3 == x4:
        if min(y1, y2) < max(y3, y4) and max(y1, y2) > min(y3, y4) and min(z1, z2) < max(z3, z4) and max(z1, z2) > min(z3, z4):
            return True

    # Check for intersection along Y-axis
    if y1 == y2 == y3 == y4:
        if min(x1, x2) < max(x3, x4) and max(x1, x2) > min(x3, x4) and min(z1, z2) < max(z3, z4) and max(z1, z2) > min(z3, z4):
            return True

    # Check for intersection along Z-axis
    if z1 == z2 == z3 == z4:
        if min(x1, x2) < max(x3, x4) and max(x1, x2) > min(x3, x4) and min(y1, y2) < max(y3, y4) and max(y1, y2) > min(y3, y4):
            return True

    return False


def segments_intersect(segment1, segment2):
    """
    Check if two line segments intersect or overlap.
    This function assumes that the segments are either horizontal or vertical 
    (i.e., aligned with the x, y, or z axis), as is the case with our dungeon layout.
    """
    # Unpack segments
    (x1, y1, z1), (x2, y2, z2) = segment1
    (x3, y3, z3), (x4, y4, z4) = segment2

    # Check for intersection or overlap along X-axis
    if x1 == x2 == x3 == x4:
        if not (max(y1, y2) < min(y3, y4) or min(y1, y2) > max(y3, y4) or max(z1, z2) < min(z3, z4) or min(z1, z2) > max(z3, z4)):
            return True

    # Check for intersection or overlap along Y-axis
    if y1 == y2 == y3 == y4:
        if not (max(x1, x2) < min(x3, x4) or min(x1, x2) > max(x3, x4) or max(z1, z2) < min(z3, z4) or min(z1, z2) > max(z3, z4)):
            return True

    # Check for intersection or overlap along Z-axis
    if z1 == z2 == z3 == z4:
        if not (max(x1, x2) < min(x3, x4) or min(x1, x2) > max(x3, x4) or max(y1, y2) < min(y3, y4) or min(y1, y2) > max(y3, y4)):
            return True

    return False





def evaluate_solution(solution, z_penalty=10):
    total_distance = 0
    all_segments = []

    # Generate segments for each edge based on the PathSequence from the solution
    for (u, v), path_seq in solution.path_sequences.items():
        segments = path_seq.get_segments(solution.positions)
        
        for segment in segments:
            # Check for overlapping or intersecting segments
            for existing_segment in all_segments:
                if segments_intersect_without_overlap(segment, existing_segment):
                    return float('inf')  # Return a high score if there's an overlap
                
                if segments_intersect(segment, existing_segment):
                    total_distance += 2
            
            all_segments.append(segment)
            
            distance = np.linalg.norm(np.array(segment[0]) - np.array(segment[1]))
            total_distance += distance
            
            # Add penalty for segments that move along the Z-axis
            if segment[0][2] != segment[1][2]:
                z_difference = abs(segment[0][2] - segment[1][2])
                total_distance += z_penalty * z_difference

    return total_distance