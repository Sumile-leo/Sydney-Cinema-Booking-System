# COMP9001 Final Project - Elemental Magic Arena

English Version | [中文版](./README_CN.md)

## Project Overview

This is the final project for COMP9001 course at the University of Sydney (USYD). The project is an **Elemental Magic Arena** - a particle-based magic defense game where players use elemental spells to defend against waves of enemies.

## Course Information

- **University**: University of Sydney (USYD)
- **Course Code**: COMP9001
- **Project Type**: Final Project
- **Project Name**: Elemental Magic Arena (元素魔法大乱斗)
- **Submission Deadline**: November 2, 2025

## Project Features

### 🎮 Game Concept
Players act as a magic wizard, drawing elemental magic with the mouse to defeat enemies attacking from above. Different elements have strengths and weaknesses, and combining elements creates powerful combo spells!

### Core Features
- 🔥 **5 Elemental Magic**: Fire, Water, Thunder, Ice, Wind
- 💫 **Particle Effects**: Stunning particle system with trails and glow effects
- 👹 **Enemy System**: 5 enemy types with elemental attributes and weaknesses
- ⚔️ **Combo Skills**: Combine elements to create 8+ powerful magic combos
- 📈 **Progression System**: Level up, unlock skills, and upgrade attributes
- 🎯 **Wave System**: Increasing difficulty with boss battles
- ✨ **Visual Effects**: Explosions, screen shake, slow motion, and more

### Technical Highlights
- 🖥️ **Built with PyQt5**: Modern GUI with custom particle rendering
- 🎨 **Advanced Particle System**: Thousands of particles with physics simulation
- ⚡ **Real-time Combat**: 60 FPS gameplay with smooth animations
- 🎮 **Game Mechanics**: Element interactions, collision detection, AI enemies
- 🌟 **Visual Polish**: Bloom effects, motion blur, screen effects

## Project Structure

```
Comp9001_finalproject/
├── README.md                  # Project documentation (English)
├── README_CN.md               # Project documentation (Chinese)
├── PROJECT_PROPOSAL.md        # Detailed project proposal (English)
├── PROJECT_PROPOSAL_CN.md     # Detailed project proposal (Chinese)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
├── main.py                    # Game entry point
├── game/                      # Game source code
│   ├── __init__.py
│   ├── window.py             # Main game window
│   ├── particle.py           # Particle system
│   ├── element.py            # Element types and properties
│   ├── enemy.py              # Enemy classes
│   ├── combat.py             # Combat logic
│   ├── effects.py            # Visual effects
│   ├── combo_system.py       # Combo skill system
│   ├── level_system.py       # Leveling and progression
│   ├── skill_tree.py         # Skill tree system
│   ├── boss.py               # Boss enemies
│   ├── ui.py                 # User interface
│   ├── audio.py              # Sound effects and music
│   └── manager.py            # Game state management
├── assets/                    # Game assets (optional)
│   ├── sounds/               # Sound effects
│   ├── music/                # Background music
│   └── images/               # Images and sprites
└── docs/                      # Additional documentation
```

## Tech Stack

- **Programming Language**: Python 3.8+
- **GUI Framework**: PyQt5
- **Graphics**: QPainter with custom rendering
- **Mathematics**: NumPy for particle physics
- **Audio**: pygame.mixer (optional)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sumile-leo/Comp9001_finalproject.git
   cd Comp9001_finalproject
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

```bash
python main.py
```

## Game Controls

### Mouse Controls
- **Left Click + Drag**: Draw elemental magic
- **Mouse Movement**: Aim magic spells

### Keyboard Controls
- **1 / Q**: Switch to Fire element 🔥
- **2 / W**: Switch to Water element 💧
- **3 / E**: Switch to Thunder element ⚡
- **4 / R**: Switch to Ice element ❄️
- **5 / T**: Switch to Wind element 🌪️
- **Space**: Use combo skill (when ready)
- **Shift**: Defensive stance
- **Tab**: View skill tree
- **Esc**: Pause menu
- **[ / ]**: Adjust time speed (debug)

## Gameplay

### Objective
Survive as many waves as possible by defeating enemies with elemental magic. Use the correct elements to exploit enemy weaknesses and combine elements for powerful combos!

### Element System

**Element Interactions:**
- 🔥 Fire is strong against 💧 Water enemies (ice creatures)
- 💧 Water is strong against 🔥 Fire enemies
- ⚡ Thunder is strong against 💧 Water (electrocution)
- ❄️ Ice freezes and slows enemies
- 🌪️ Wind pushes and redirects enemies

**Combo Magic:**
- 🌋 Steam Explosion = Fire + Water
- ⚡ Thunder Storm = Thunder + Water
- 🌪️ Fire Tornado = Fire + Wind
- 💎 Crystal Burst = Ice + Thunder
- 🌈 Plasma Cannon = Fire + Thunder
- ...and more to discover!

### Enemy Types

1. **🔥 Fire Slime** - Fast, weak to water
2. **💧 Water Elemental** - Medium, weak to thunder
3. **⚡ Thunder Spirit** - Very fast, weak to ice
4. **❄️ Ice Giant** - Slow, high HP, weak to fire
5. **🌪️ Wind Knight** - Fast, deflects weak spells

### Boss Battles

Every 10 waves, face a powerful elemental boss with unique attack patterns and mechanics!

## Development Progress

- [x] Project initialization and repository setup
- [x] Project documentation and proposal
- [ ] Week 1: Core game framework and particle system
- [ ] Week 2: Combat system and visual effects
- [ ] Week 3: Advanced features and polish

## Development Timeline

### Week 1 (Oct 10-16): Foundation
- Game window and loop (60 FPS)
- Particle system implementation
- 5 elemental effects
- Enemy spawning and movement
- Basic combat and UI

### Week 2 (Oct 17-23): Core Gameplay
- Advanced particle effects (trails, glow)
- Combo skill system
- Level and progression system
- Skill tree implementation
- Enhanced visual effects

### Week 3 (Oct 24 - Nov 2): Polish & Complete
- Boss battles
- Advanced systems (talents, achievements)
- Audio implementation
- Performance optimization
- Documentation and presentation

## Technical Challenges

### Particle System
- Managing thousands of particles efficiently
- Implementing physics simulation (velocity, acceleration, lifetime)
- Creating diverse visual effects for each element

### Combat System
- Collision detection optimization (spatial partitioning)
- Element interaction logic
- Combo detection and triggering

### Performance Optimization
- Object pooling for particles
- Spatial hashing for collision detection
- Level of detail (LOD) for distant particles

## Learning Outcomes

This project demonstrates:

**Python Programming:**
- Object-oriented design (classes for particles, enemies, elements)
- Data structures (managing collections of game objects)
- Algorithms (collision detection, pathfinding)
- Mathematical computations (vectors, trigonometry)

**GUI Development:**
- PyQt5 advanced features
- Custom painting and rendering
- Event handling (mouse, keyboard)
- Animation systems

**Game Development:**
- Game loop architecture
- Physics simulation
- Particle systems
- Visual effects

**Software Engineering:**
- Modular design
- Code organization
- Performance optimization
- Documentation

## Screenshots

(Screenshots will be added as development progresses)

## Demo Video

(Demo video will be added upon completion)

## Team Members

- Zhou Li - [GitHub](https://github.com/Sumile-leo)

## Acknowledgments

Special thanks to:
- COMP9001 course instructors and tutors
- University of Sydney for providing learning resources
- PyQt5 and Python communities for documentation and support

## License

This project is for academic purposes only and is part of the COMP9001 course requirements at the University of Sydney.

## Contact

- **GitHub Repository**: [Comp9001_finalproject](https://github.com/Sumile-leo/Comp9001_finalproject)
- **GitHub Issues**: [Report Issues](https://github.com/Sumile-leo/Comp9001_finalproject/issues)
- **Email**: your.email@university.edu.au

---

**Academic Integrity Notice**: This project is submitted as original work for COMP9001. All code is written by the project author. Please maintain academic integrity.

**Last Updated**: October 10, 2025
