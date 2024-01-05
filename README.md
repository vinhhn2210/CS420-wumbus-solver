# CS420-wumbus-solver
## Getting Started
### Installing
* Clone the project to your computer. 
```
  git clone https://github.com/vinhhn2210/CS420-wumbus-solver.git
```
* Set up Pygame Library:
```
  python3 -m pip install -U pygame --user
```
* Run the program:
```
  python main.py
```

### Executing program
* Using an IDE to compile this game (Sublime Text 3, Visual Studio Code, ...)
* Remember to add all source codes to project before building and running
* Run file main.py to enjoy the Game

## How To Use
### Adding new maps
* Put new map in .txt format in /Map directory.

### Map generator
1. Gen random 10 map with size 10 x 10
* python3 Sources/map_generator.py
3. Gen with size and name
* python3 Sources/map_generator.py 10 map_sample
4. Gen with pitCoeff, wumpusMaximum, goldMaximum
* python3 Sources/map_generator.py 10 map_sample 0.3 5 5

### Solving
1. To automaticly solving all map with all current algorithms:
* python3 Sources/system.py Map auto
2. To solve with specify map-algorithm and guide:
* python3 Sources/system.py Map custom
3. To visualize
* python3 main.py
