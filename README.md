# Ojected Oriented Programming Classes

## Objective

OOP approach to real valued matrix algebra and multidirectional elevators.

## Code Functionality

*Matrix Valued Algebra*

The code begins by importing required libraries, including math, randint from random, and modules from mpl_toolkits and matplotlib.pyplot for 3D visualization. It sets up Matplotlib for interactive mode and displays the plot. Several classes are defined to represent various aspects of the simulation:

-Point3D: Represents a point in 3D space and includes methods for vector operations and comparisons.
-Person: Represents a person in the simulation, with attributes such as name, current position, destination, and whether they have arrived.
-Factory: Represents the factory environment and contains methods for simulating the elevator's operation, displaying the state, and checking if everyone has arrived.
-Elevator: Represents the elevator itself and includes methods for moving, picking up, and dropping off people.

Main Simulation Loop: In the if __name__ == '__main__': block, the code initializes the factory environment, people, and the elevator. It then enters a loop where it repeatedly runs the simulation, updates the display, and checks if everyone has arrived. The loop continues until all people have reached their destinations. Finally, the code prints "Everyone has arrived." when the simulation is complete, indicating that all people have reached their destinations.

*Multidirectional Elevators*

The code imports the tabulate module for formatting matrices. The Matrix class is defined to represent matrices and includes various methods for matrix operations.

- __init__: Initializes the class with a matrix and stores its dimensions.
-__str__: Formats the matrix for display using the tabulate function.
  -create_identity: Generates an identity matrix of the same size.
  -multiplication: Performs matrix multiplication.
  -stacking: Stacks two matrices horizontally.
  -un_stacking: Extracts the right block of a stacked matrix.
  -gauss_jordan: Performs Gauss-Jordan elimination to reduce the matrix to RREF form.
  -inverse: Computes the inverse of the matrix using Gauss-Jordan elimination.
  -linear_equations: Solves a system of linear equations using matrix multiplication.
  -my_test: A testing function for demonstrating matrix operations (though it's not part of the class itself).

The my_test function demonstrates matrix multiplication by creating two matrices and performing their multiplication using the multiplication method. This code is currently outside the class definition, and there is a missing self parameter in the method call.
