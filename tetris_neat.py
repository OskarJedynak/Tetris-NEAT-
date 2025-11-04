# [file name]: tetris_neat_improved.py
# [file content begin]
import neat
import numpy as np
import pickle
import os
from game import Game


class TetrisNEATImproved:
    def __init__(self):
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  'neat_config.txt')

    def eval_genome(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game()
        total_score = 0
        moves = 0
        max_moves = 500

        while not game.game_over and moves < max_moves:
            inputs = self.get_board_features(game)
            outputs = net.activate(inputs)
            self.execute_neat_action(game, outputs)
            moves += 1
            total_score = game.score

        fitness = total_score

        if total_score > 0:
            fitness += moves * 0.1
            max_height = self.get_max_height(game.grid)
            fitness -= max_height * 0.5
            holes = self.count_holes(game.grid)
            fitness -= holes * 2

        return max(fitness, 1)

    def get_board_features(self, game):
        grid = game.grid
        features = []

        for row in range(4):
            for col in range(10):
                if row < grid.num_rows and col < grid.num_cols:
                    features.append(1 if grid.grid[row][col] != 0 else 0)
                else:
                    features.append(0)

        block_type = [0] * 7
        block_type[game.current_block.id - 1] = 1
        features.extend(block_type)

        features.append(game.current_block.rotation_state / 4.0)
        features.append(game.current_block.row_offest / 20.0)
        features.append(game.current_block.column_offset / 10.0)

        return features

    def count_holes(self, grid):
        holes = 0
        for col in range(grid.num_cols):
            found_block = False
            for row in range(grid.num_rows):
                if grid.grid[row][col] != 0:
                    found_block = True
                elif found_block:
                    holes += 1
        return holes

    def get_max_height(self, grid):
        max_height = 0
        for col in range(grid.num_cols):
            for row in range(grid.num_rows):
                if grid.grid[row][col] != 0:
                    height = grid.num_rows - row
                    if height > max_height:
                        max_height = height
                    break
        return max_height

    def execute_neat_action(self, game, outputs):
        if outputs[0] > 0.5:
            game.rotate()

        if outputs[1] < -0.3:
            game.move_left()
        elif outputs[1] > 0.3:
            game.move_right()

        game.move_down()

    def train(self, generations=100):
        population = neat.Population(self.config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        winner = population.run(self.eval_genomes, generations)
        with open('best_tetris_genome_improved.pkl', 'wb') as f:
            pickle.dump(winner, f)
        return winner

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = self.eval_genome(genome, config)

    def test_genome(self, genome_path='best_tetris_genome_improved.pkl'):
        with open(genome_path, 'rb') as f:
            genome = pickle.load(f)
        net = neat.nn.FeedForwardNetwork.create(genome, self.config)
        game = Game()
        while not game.game_over:
            inputs = self.get_board_features(game)
            outputs = net.activate(inputs)
            self.execute_neat_action(game, outputs)
        return game.score


if __name__ == "__main__":
    trainer = TetrisNEATImproved()
    trainer.train(generations=100)
    final_score = trainer.test_genome()
    print(f"Final test score: {final_score}")