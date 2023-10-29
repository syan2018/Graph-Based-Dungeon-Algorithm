
import random

import numpy as np


class SimulatedAnnealing:
    def __init__(self, initial_solution, evaluate_fn, perturb_fns, initial_temp=1000, final_temp=1, alpha=0.95, max_iterations=5000):
        
        # 记录解决方案
        self.current_solution = initial_solution
        self.current_score = evaluate_fn(initial_solution)
        
        # 记录最佳方案
        self.best_solution = self.current_solution
        self.best_score = self.current_score
        
        # 评估函数和退火算子
        self.evaluate_fn = evaluate_fn
        self.perturb_fns = perturb_fns
        
        # 温度和终止控制
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.cur_iteration = 0

    def run(self):

        temp = self.initial_temp

        while temp > self.final_temp and self.cur_iteration < self.max_iterations:

            # 随机应用算子
            perturb_fn = random.choice(self.perturb_fns)
            new_solution = perturb_fn(self.current_solution)

            new_score = self.evaluate_fn(new_solution)

            if new_score < self.current_score or random.uniform(0, 1) < np.exp(-(new_score - self.current_score) / temp):
                self.current_solution, self.current_score = new_solution, new_score
                if self.current_score < self.best_score:
                    self.best_solution, self.best_score = self.current_solution, self.current_score

            # 降温
            temp *= self.alpha
            self.cur_iteration += 1

        return self.best_solution, self.best_score