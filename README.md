# Tetris AI - Genetic Learning Algorithm

A Tetris game implementation with an AI that learns to play using a genetic algorithm. Watch as generations of AI agents evolve and improve their Tetris skills over time!

## 🎮 Features

- **Classic Tetris gameplay** - Manual play mode with all 7 tetromino pieces
- **Genetic Algorithm AI** - Population-based learning system
- **Real-time evolution** - Watch AI improve across generations
- **Heuristic-based decision making** - AI evaluates board states using:
  - Aggregate height (keeping stack low)
  - Holes (avoiding empty spaces under blocks)
  - Bumpiness (keeping surface flat)
  - Lines cleared (maximizing score)

## 📁 Project Structure

```
tetris/
├── block.py          # Base block class with movement and rotation
├── blocks.py         # All 7 Tetris pieces (I, J, L, O, S, T, Z)
├── colors.py         # Color definitions
├── game.py           # Core game logic and mechanics
├── grid.py           # Game board and grid operations
├── position.py       # Position helper class
├── main.py           # Manual play mode
└── new_neat.py       # AI training with genetic algorithm
```

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Pygame

### Installation

1. Install Pygame:
```bash
pip install pygame
```

2. Clone or download all project files to the same directory

### Running the Game

**Manual Play:**
```bash
python main.py
```
- Arrow Keys: Move and rotate pieces
- Play until game over, press any key to restart

**AI Training Mode:**
```bash
python new_neat.py
```
- Watch the AI learn automatically
- Press `V` to toggle visualization on/off
- Let it run for 5-10 minutes to see significant improvement

## 🧬 How the AI Works

### Genetic Algorithm Process

1. **Population**: 20 AI agents per generation
2. **Evaluation**: Each AI plays 3 games to determine fitness
3. **Selection**: Top 20% (elite) automatically advance
4. **Breeding**: Best performers create offspring through crossover
5. **Mutation**: Random weight adjustments (10% chance) add variation
6. **Evolution**: New generation replaces old, cycle repeats

### Decision Making

For each piece, the AI:
1. Tests all possible rotations (0-3 rotations)
2. Tests all possible column placements
3. Simulates dropping the piece
4. Evaluates resulting board state using weighted heuristics
5. Chooses the move with the highest score

### Heuristic Weights

The AI learns optimal values for:
- **height**: Penalty for tall stacks (typically negative)
- **holes**: Penalty for gaps under blocks (negative)
- **bumpiness**: Penalty for uneven surface (negative)
- **lines_cleared**: Reward for clearing lines (positive)

## 📊 Training Progress

### What to Expect

- **Generation 0-5**: Random play, scores 0-50
- **Generation 5-20**: Learning basics, scores 50-200
- **Generation 20-50**: Solid strategies, scores 200-500+
- **Generation 50+**: Advanced play, scores 500-1000+

### Performance

- Runs at 50x speed (processes 50 game states per frame)
- ~1-2 generations per second on modern hardware
- Visualization off = faster training
- Best results after 10+ minutes of training

## 🎯 Key Controls

### Manual Play (main.py)
- `↑` - Rotate piece
- `←` - Move left
- `→` - Move right  
- `↓` - Move down faster

### AI Trainer (ai_trainer.py)
- `V` - Toggle game visualization (speeds up training when off)
- Close window to stop training

## 📈 Understanding the Stats

**Generation**: Current evolution cycle number

**AI**: Which agent in the population is currently playing (X/20)

**Current Score**: Score of the game being played right now

**Best Avg Score**: Highest average score across all generations (fitness/games_played)

**Best Weights**: The optimal heuristic values discovered so far

## 🔧 Customization

You can modify these parameters in `ai_trainer.py`:

```python
# Training speed (games per frame)
speed = 50  # Increase for faster training

# Population size
population_size = 20  # More agents = better diversity, slower training

# Games per AI
games_per_generation = 3  # More games = better fitness evaluation

# Mutation rate
mutation_rate = 0.1  # Higher = more exploration
```

## 🧪 How It Learns

The AI doesn't know the rules of Tetris initially. Through evolution:

1. **Early generations** try random strategies, most fail quickly
2. **Mid generations** discover that avoiding holes and keeping low stacks helps
3. **Late generations** optimize the balance between all heuristics
4. **Convergence** occurs when weights stabilize at near-optimal values

## 📝 Score System

- 1 line cleared = 10 points
- 2 lines cleared = 30 points  
- 3 lines cleared = 50 points
- 4 lines (Tetris) = not implemented in scoring but possible to achieve

## 🐛 Known Issues

- AI occasionally makes suboptimal moves early in training (by design - exploration)
- Very long games (500+ lines) may slow down slightly
- First generation is slower due to poor decision making

## 🎓 Educational Value

This project demonstrates:
- Genetic algorithms and evolutionary computation
- Heuristic-based AI decision making
- Game state evaluation
- Population-based optimization
- Real-time visualization of machine learning

## 📄 License

Free to use, modify, and distribute for educational purposes.

## 🤝 Contributing

Feel free to experiment with:
- Different heuristics
- Alternative selection strategies
- Neural network approaches
- Multi-objective optimization

## ✨ Future Improvements

Potential enhancements:
- Save/load best AI weights
- Tournament mode (human vs AI)
- Different difficulty levels
- 4-line clear scoring
- Combo multipliers
- Hold piece feature

---

**Enjoy watching the AI learn!** 🎮🤖

*Tip: Turn off visualization (press V) and let it train for 15+ minutes for the best results.*
