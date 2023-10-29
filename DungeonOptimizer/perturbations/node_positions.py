import random

from utils.solutions import Solution


# 随机交换位置
def perturb_swap_positions(solution):
    """Perturb the positions by randomly swapping two nodes, if possible."""
    positions = solution.positions
    nodes = list(positions.keys())
    if len(nodes) < 2:
        return solution
    
    node1, node2 = random.sample(nodes, 2)
    new_positions = positions.copy()
    new_positions[node1], new_positions[node2] = new_positions[node2], new_positions[node1]
    
    return Solution(graph=solution.graph, positions=new_positions, path_sequences=solution.path_sequences)

# 随机移动单个点
def perturb_by_displacement(solution):
    """
    Apply the displacement perturbation to the given positions.
    """
    positions = solution.positions
    new_positions = positions.copy()
    
    # Randomly select a node
    node = random.choice(list(new_positions.keys()))
    
    # Randomly select a new position for the node, ensuring the new position is currently unoccupied
    available_positions = [(x, y, z) for x in range(4) for y in range(4) for z in range(4) if (x, y, z) not in new_positions.values()]
    new_position = random.choice(available_positions)
    
    # Update the position of the selected node
    new_positions[node] = new_position
    
    return Solution(graph=solution.graph, positions=new_positions, path_sequences=solution.path_sequences)

# 随机扰动单个点
def perturb_by_single_displacement(solution):
    """
    Apply the single step displacement perturbation in one of the three directions (X, Y, or Z).
    """
    positions = solution.positions
    new_positions = positions.copy()
    
    # Randomly select a node
    node = random.choice(list(new_positions.keys()))
    x, y, z = new_positions[node]

    # Randomly select a direction and move by one step in that direction
    direction = random.choice(['X', 'Y', 'Z'])
    step = random.choice([-1, 1])
    
    if direction == 'X':
        x += step
    elif direction == 'Y':
        y += step
    else:
        z += step

    # Ensure the new position is within bounds and is not occupied
    if (0 <= x < 4 and 0 <= y < 4 and 0 <= z < 4) and (x, y, z) not in new_positions.values():
        new_positions[node] = (x, y, z)
    
    return Solution(graph=solution.graph, positions=new_positions, path_sequences=solution.path_sequences)