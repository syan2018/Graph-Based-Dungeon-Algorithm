
import matplotlib.pyplot as plt


def plot_dungeon_layout (opt):
    """
    Plot the paths according to the given solution.
    This follows the style provided in the `plot_3d_layout_segmented_no_duplicates` function.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    solution = opt.solution
    
    # Extract positions and path sequences from the solution
    positions = solution.positions
    path_sequences = solution.path_sequences
    
    # Plot nodes
    node_colors = ['red' if node in [0, opt.dungeon.end_node] else 'blue' for node in solution.graph.nodes]
    xs, ys, zs = zip(*[positions[node] for node in solution.graph.nodes])
    ax.scatter(xs, ys, zs, c=node_colors, s=100)
    
    # Plot edges based on path sequences
    for (u, v), path_seq in path_sequences.items():
        segments = path_seq.get_segments(positions)
        for segment in segments:
            ax.plot([segment[0][0], segment[1][0]],
                    [segment[0][1], segment[1][1]],
                    [segment[0][2], segment[1][2]], color='black')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_zlim(0, 3)
    ax.grid(False)
    ax.set_title('3D Dungeon Layout with Path Sequences')
    
    plt.show()


import plotly.graph_objects as go

def interactive_plot_dungeon_layout(opt):

    solution = opt.solution

    positions = solution.positions
    path_sequences = solution.path_sequences
    
    # Extract node coordinates
    xs, ys, zs = zip(*[positions[node] for node in solution.graph.nodes])
    node_colors = ['red' if node in [0, opt.dungeon.end_node] else 'blue' for node in solution.graph.nodes]
    
    # Create a scatter plot for nodes
    scatter = go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode='markers',
        marker=dict(size=8, color=node_colors)
    )
    
    # Extract edge coordinates
    edge_x, edge_y, edge_z = [], [], []
    for (u, v), path_seq in path_sequences.items():
        segments = path_seq.get_segments(positions)
        for segment in segments:
            edge_x += [segment[0][0], segment[1][0], None]
            edge_y += [segment[0][1], segment[1][1], None]
            edge_z += [segment[0][2], segment[1][2], None]
    
    # Create a line plot for edges
    lines = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='black', width=6)
    )
    
    # Create the layout
    layout = go.Layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[0,3]),
            yaxis=dict(nticks=4, range=[0,3]),
            zaxis=dict(nticks=4, range=[0,3]),
        )
    )
    
    # Plot the figure
    fig = go.Figure(data=[scatter, lines], layout=layout)
    fig.show()
