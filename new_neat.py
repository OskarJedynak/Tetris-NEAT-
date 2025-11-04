import sys, pygame
import random
import copy
from game import Game
from colors import Colors


class TetrisAI:
    def __init__(self, weights=None):
        if weights is None:
            self.weights = {
                'height': random.uniform(-1, 0),
                'holes': random.uniform(-1, 0),
                'bumpiness': random.uniform(-1, 0),
                'lines_cleared': random.uniform(0, 1)
            }
        else:
            self.weights = weights
        self.fitness = 0
        self.games_played = 0

    def evaluate_board(self, game):
        grid = game.grid.grid

        heights = []
        for col in range(game.grid.num_cols):
            for row in range(game.grid.num_rows):
                if grid[row][col] != 0:
                    heights.append(game.grid.num_rows - row)
                    break
            else:
                heights.append(0)

        aggregate_height = sum(heights)

        holes = 0
        for col in range(game.grid.num_cols):
            block_found = False
            for row in range(game.grid.num_rows):
                if grid[row][col] != 0:
                    block_found = True
                elif block_found and grid[row][col] == 0:
                    holes += 1

        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])

        lines_cleared = game.score / 10

        score = (self.weights['height'] * aggregate_height +
                 self.weights['holes'] * holes +
                 self.weights['bumpiness'] * bumpiness +
                 self.weights['lines_cleared'] * lines_cleared)

        return score

    def get_best_move(self, game):
        best_score = float('-inf')
        best_move = {'rotation': 0, 'column': 0}

        original_state = self.save_game_state(game)

        for rotation in range(4):
            for col in range(-2, game.grid.num_cols + 2):
                test_game = self.restore_game_state(game, original_state)

                for _ in range(rotation):
                    test_game.current_block.rotate()

                current_col = test_game.current_block.column_offset
                moves = col - current_col

                if moves > 0:
                    for _ in range(moves):
                        test_game.move_right()
                elif moves < 0:
                    for _ in range(abs(moves)):
                        test_game.move_left()

                if not test_game.block_inside():
                    continue

                drop_count = 0
                while not test_game.game_over and drop_count < 25:
                    test_game.move_down()
                    drop_count += 1
                    if test_game.game_over:
                        break

                if not test_game.game_over:
                    score = self.evaluate_board(test_game)
                    if score > best_score:
                        best_score = score
                        best_move = {'rotation': rotation, 'column': col}

        return best_move

    def save_game_state(self, game):
        return {
            'grid': copy.deepcopy(game.grid.grid),
            'current_block': copy.deepcopy(game.current_block),
            'score': game.score
        }

    def restore_game_state(self, game, state):
        new_game = Game()
        new_game.grid.grid = copy.deepcopy(state['grid'])
        new_game.current_block = copy.deepcopy(state['current_block'])
        new_game.score = state['score']
        return new_game


class GeneticAlgorithm:
    def __init__(self, population_size=20):
        self.population_size = population_size
        self.population = [TetrisAI() for _ in range(population_size)]
        self.generation = 0
        self.best_fitness = 0
        self.best_ai = None

    def evolve(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        if self.population[0].fitness > self.best_fitness:
            self.best_fitness = self.population[0].fitness
            self.best_ai = copy.deepcopy(self.population[0])

        elite_size = self.population_size // 5
        new_population = self.population[:elite_size]

        while len(new_population) < self.population_size:
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)

        self.population = new_population
        self.generation += 1

        for ai in self.population:
            ai.fitness = 0
            ai.games_played = 0

    def select_parent(self):
        tournament_size = 3
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=lambda x: x.fitness)

    def crossover(self, parent1, parent2):
        child_weights = {}
        for key in parent1.weights:
            if random.random() < 0.5:
                child_weights[key] = parent1.weights[key]
            else:
                child_weights[key] = parent2.weights[key]
        return TetrisAI(child_weights)

    def mutate(self, ai, mutation_rate=0.1):
        for key in ai.weights:
            if random.random() < mutation_rate:
                ai.weights[key] += random.uniform(-0.2, 0.2)
        return ai


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 650))
    pygame.display.set_caption("Tetris AI - Genetic Learning")

    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 20)

    clock = pygame.time.Clock()

    ga = GeneticAlgorithm(population_size=20)
    current_ai_index = 0
    game = Game()

    speed = 50  # Games per frame
    show_visualization = True

    games_per_generation = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    show_visualization = not show_visualization

        for _ in range(speed):
            if game.game_over:
                current_ai = ga.population[current_ai_index]
                current_ai.fitness += game.score
                current_ai.games_played += 1

                if current_ai.games_played >= games_per_generation:
                    current_ai_index += 1

                    if current_ai_index >= len(ga.population):
                        ga.evolve()
                        current_ai_index = 0

                game = Game()

            current_ai = ga.population[current_ai_index]
            move = current_ai.get_best_move(game)

            for _ in range(move['rotation']):
                game.rotate()

            current_col = game.current_block.column_offset
            target_col = move['column']

            if target_col > current_col:
                for _ in range(target_col - current_col):
                    game.move_right()
            elif target_col < current_col:
                for _ in range(current_col - target_col):
                    game.move_left()

            game.move_down()

        screen.fill(Colors.backg_color)

        if show_visualization:
            game.draw(screen)

        current_ai = ga.population[current_ai_index]

        stats = [
            f"Generation: {ga.generation}",
            f"AI: {current_ai_index + 1}/{len(ga.population)}",
            f"Current Score: {game.score}",
            f"Best Avg Score: {int(ga.best_fitness / games_per_generation)}",
            f"",
            f"Press V to toggle visualization",
            f"(speeds up training when off)"
        ]

        y = 20
        for stat in stats:
            if stat:
                text = small_font.render(stat, True, Colors.white)
                screen.blit(text, (520, y))
            y += 25

        if ga.best_ai:
            y = 350
            title = small_font.render("Best Weights:", True, Colors.white)
            screen.blit(title, (520, y))
            y += 25

            for key, value in ga.best_ai.weights.items():
                text = small_font.render(f"{key}: {value:.3f}", True, Colors.white)
                screen.blit(text, (520, y))
                y += 20

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()