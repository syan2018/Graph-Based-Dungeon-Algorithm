from core.dungeon import DungeonRGT
import matplotlib.pyplot as plt

from utils.solutions import Solution

from core.simulated_annealing import SimulatedAnnealing

from utils.positions import assign_initial_positions

from utils.plotting import plot_dungeon_layout


class DungeonOptimizer:
    def __init__(self, evaluate_fn, perturb_fns, 
                 plot_fn=plot_dungeon_layout, init_fn=assign_initial_positions, 
                 n=10, min_resistance=1, max_resistance=10, total_resistance=(10, 50), max_iter=3):
        self.dungeon = DungeonRGT(n, min_resistance, max_resistance, total_resistance, max_iter)
        self.evaluate_fn = evaluate_fn
        self.perturb_fns = perturb_fns
        self.plot_fn = plot_fn
        self.init_fn = init_fn
        self.current_score = float('inf')  # Initialize with a high score

    # 初始化图，并创建位置
    def generate_dungeon(self):
        self.dungeon.generate()
        self.solution = Solution(self.dungeon.graph, self.init_fn(self.dungeon.graph))

    def evaluate_layout(self, solution=None):
        if solution is None:
            solution = self.solution
        return self.evaluate_fn(solution)

    def optimize_layout(self, initial_temp=1000, final_temp=1, alpha=0.95, max_iterations=500):
        annealer = SimulatedAnnealing(
            initial_solution=self.solution,
            evaluate_fn=self.evaluate_layout,
            perturb_fns=self.perturb_fns,
            initial_temp=initial_temp,
            final_temp=final_temp,
            alpha=alpha,
            max_iterations=max_iterations
        )
        self.solution, self.current_score = annealer.run()

        print("first step optimize: " + str(self.current_score))

        from perturbations.node_positions import perturb_by_single_displacement

        sec_annealer = SimulatedAnnealing(
            initial_solution=self.solution,
            evaluate_fn=self.evaluate_layout,
            perturb_fns=[perturb_by_single_displacement],
            initial_temp=initial_temp,
            final_temp=final_temp,
            alpha=alpha,
            max_iterations=max_iterations
        )
        self.solution, self.current_score = sec_annealer.run()

        print("second step optimize: " + str(self.current_score))


    def plot_layout(self):
        self.plot_fn(self)