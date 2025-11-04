import neat
import pygame
import pickle
from game import Game
from colors import Colors


class TetrisAI:
    def __init__(self, genome_path='best_tetris_genome.pkl'):
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  'neat_config.txt')

        with open(genome_path, 'rb') as f:
            self.genome = pickle.load(f)

        self.net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)

    def get_board_features(self, game):
        grid = game.grid
        features = []

        heights = self.get_column_heights(grid)
        features.extend(heights)

        for i in range(len(heights) - 1):
            features.append(heights[i + 1] - heights[i])

        features.append(self.count_holes(grid))

        block_type = [0] * 7
        block_type[game.current_block.id - 1] = 1
        features.extend(block_type)

        features.append(game.current_block.rotation_state / 4.0)

        features.append(game.current_block.row_offest / 20.0)
        features.append(game.current_block.column_offset / 10.0)

        features = [min(max(f, -1), 1) for f in features]

        return features

    def get_column_heights(self, grid):
        heights = []
        for col in range(grid.num_cols):
            height = 0
            for row in range(grid.num_rows):
                if grid.grid[row][col] != 0:
                    height = grid.num_rows - row
                    break
            heights.append(height / grid.num_rows)
        return heights

    def count_holes(self, grid):
        holes = 0
        total_cells = grid.num_rows * grid.num_cols

        for col in range(grid.num_cols):
            found_block = False
            for row in range(grid.num_rows):
                if grid.grid[row][col] != 0:
                    found_block = True
                elif found_block:
                    holes += 1

        return holes / total_cells

    def make_move(self, game):
        inputs = self.get_board_features(game)
        outputs = self.net.activate(inputs)


        if outputs[0] > 0.5:
            game.rotate()

        if outputs[1] < -0.3:
            game.move_left()
        elif outputs[1] > 0.3:
            game.move_right()

        if outputs[2] > 0.5:
            for _ in range(3):
                old_score = game.score
                game.move_down()
                if game.score > old_score:
                    break
        else:
            game.move_down()


def main():
    pygame.init()

    title_font = pygame.font.Font(None, 40)
    score_surface = title_font.render("Score", True, Colors.white)
    next_surface = title_font.render("Next", True, Colors.white)
    game_over_surface = title_font.render("GAME OVER", True, Colors.white)
    ai_surface = title_font.render("AI PLAYING", True, Colors.white)

    score_rect = pygame.Rect(320, 55, 170, 60)
    next_rect = pygame.Rect(320, 215, 170, 180)

    screen = pygame.display.set_mode((500, 620))
    pygame.display.set_caption("Trained Tetris AI")

    clock = pygame.time.Clock()

    game = Game()
    ai = TetrisAI('best_tetris_genome.pkl')

    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, 50)  # Faster updates for AI

    print("AI Tetris started! Watch the trained AI play.")
    print("Close the window to stop.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset with R key
                    game.reset()
                    print("Game reset!")
                if game.game_over:
                    game.game_over = False
                    game.reset()

            if event.type == GAME_UPDATE and not game.game_over:
                ai.make_move(game)


        score_value_surface = title_font.render(str(game.score), True, Colors.white)

        screen.fill(Colors.backg_color)
        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (375, 180, 50, 50))
        screen.blit(ai_surface, (320, 450, 50, 50))

        if game.game_over:
            screen.blit(game_over_surface, (320, 500, 50, 50))
            print(f"Game Over! Final Score: {game.score}")

        pygame.draw.rect(screen, Colors.empty, score_rect, 0, 10)
        screen.blit(score_value_surface,
                    score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
        pygame.draw.rect(screen, Colors.empty, next_rect, 0, 10)
        game.draw(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()