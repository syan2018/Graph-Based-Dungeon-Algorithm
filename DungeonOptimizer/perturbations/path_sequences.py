import random

from utils.solutions import Solution

# 随机替换连边顺序
def perturb_path_sequence(solution):
    """
    Randomly selects an edge in the solution and alters its PathSequence.
    """
    # Copy the current solution's attributes to ensure we're not modifying the original solution
    new_path_sequences = solution.path_sequences.copy()
    
    # Randomly select an edge
    edge = random.choice(list(new_path_sequences.keys()))
    
    # Alter the PathSequence for the selected edge
    new_path_sequences[edge].set_random_sequence()
    
    # Create a new solution with the altered path sequence 
    return Solution(
        graph=solution.graph,
        positions=solution.positions,
        path_sequences=new_path_sequences
    )