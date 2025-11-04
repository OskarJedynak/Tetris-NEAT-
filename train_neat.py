from tetris_neat import TetrisNEATImproved
import time


def main():
    print("=== IMPROVED NEAT TETRIS TRAINING ===")
    print("This will train for 500 generations with better fitness rules.")
    print("It may take a while...")

    start_time = time.time()
    trainer = TetrisNEATImproved()

    winner = trainer.train(generations=500)

    training_time = time.time() - start_time
    print(f"\nTraining completed in {training_time:.2f} seconds")

    print("\nTesting the best genome...")
    final_score = trainer.test_genome()
    print(f"🎯 Best genome achieved score: {final_score}")

    if final_score > 0:
        print("Success! The AI is learning to play Tetris.")
    else:
        print("The AI still needs more training. Consider increasing generations.")


if __name__ == "__main__":
    main()