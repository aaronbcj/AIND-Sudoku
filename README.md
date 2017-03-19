
# Aaron caroltin
# Algorithm to solve any suduko puzzle with diagonal rule
# Assignment No1 :: AI-ND March 2017

# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: First, we define a rule (local constraint) within each unit called naked twins. The rule says, if there are exactly two boxes with the same double digit value (say 23) then we eliminate these two digits (2,3) from every other box within the same unit. Once the rule is followed within a single unit, we propagate the same rule to other units till we no longer have any naked twins within entire puzzle [keep going recursivly to find for newly formed NTs and eliminate them as well]

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We extend the existing row, column, box levels constraint with additional diagonal rule by adding two diagonal units to the existing unitlist.
This is a top level constraint so every decision we take further down[only choice, eliminate, NT etc] are applied to each of the diagonals into consideration.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

