## A template for a CA-type model, to simulate vegetation growth
## Interactive mode of matplotlib is used to visualise the results. 

# Load the required libraries
import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters for simulation
grid_size = 100
timesteps = 150  # Number of timesteps to simulate

# Model parameters
r1 = 1
r2 = 3
a = 2
b = 12

#alternative model parameters for investigating stripe patterns
rN = 6
rS = 2
rEW = 1
aa = 2
bb = 2 
cc = 3

# Set the seed at a constant value for reproducability
# Change to get other random initial pattern
random.seed(13)  
            
# First, lets initialize the grid with a random pattern where 95% of the grid points are set to 0 and 5% to 1
initial_population = np.random.choice([0, 1, 2, 3], size=(grid_size, grid_size), p=[0.95, 0.05, 0.0, 0.0])
grid = initial_population

nr_plants = np.count_nonzero(grid)
nr_plants_list = np.zeros(timesteps)
nr_plants_list[0] = nr_plants

#count the sum of states of close neighbors
def count_closeneighbors(grid, i, j, r1):
    close_neighbors = 0
    for ni in range(i - r1, i + r1 + 1):
        for nj in range(j - r1, j + r1 + 1):
            if (ni == i and nj == j):
                continue

            ni_wrapped = ni % grid_size
            nj_wrapped = nj % grid_size
            distance = max(abs(ni_wrapped - i), abs(nj_wrapped - j))
            if distance <= r1:
                close_neighbors += grid[ni_wrapped, nj_wrapped]

    return close_neighbors

#count the sum of states of far neighbors
def count_farneighbors(grid, i, j, r1, r2):
    far_neighbors = 0
    for ni in range(i - r2, i + r2 + 1):
        for nj in range(j - r2, j + r2 + 1):
            if (ni == i and nj == j):
                continue

            ni_wrapped = ni % grid_size
            nj_wrapped = nj % grid_size
            distance = max(abs(ni_wrapped - i), abs(nj_wrapped - j))
            if distance > r1 and distance <= r2:
                far_neighbors += grid[ni_wrapped, nj_wrapped]

    return far_neighbors

#count the number of North neighbors
def count_Nneighbors(grid, i, j, rN):
    N_neighbors = 0
    for nj in range(j+1, j + rN + 1):
        nj_wrapped = nj % grid_size
        N_neighbors += grid[i, nj_wrapped]
    return N_neighbors

def count_Sneighbors(grid, i, j, rN):
    N_neighbors = 0
    for nj in range(j-1, j - rN -1,-1):
        nj_wrapped = nj % grid_size
        N_neighbors += grid[i, nj_wrapped]
    return N_neighbors

def count_EWneighbors(grid, i, j, rN):
    N_neighbors = 0
    for ni in range(i+1, i + rN + 1):
        ni_wrapped = ni % grid_size
        N_neighbors += grid[ni_wrapped, j]
    for ni in range(i-1, i - rN - 1,-1):
        ni_wrapped = ni % grid_size
        N_neighbors += grid[ni_wrapped, j]
    return N_neighbors

def turing_pattern(grid, i, j):

    #original code (cringe):
    # Count the sum of states of close and far neighbors
    # close_neighbors = count_closeneighbors(grid, i, j, r1)
    # far_neighbors = count_farneighbors(grid, i, j, r1, r2) 

    # Apply vegetation growth rules
    #updaterule = b*close_neighbors - a*far_neighbors
    updaterule= -aa*count_Nneighbors(grid, i, j, rN)+bb*count_EWneighbors(grid, i, j, rEW)+cc*count_Sneighbors(grid, i, j, rS)
    newvalue = grid[i, j] + max(-1, min(1, updaterule))
    if newvalue < 0:
        newvalue = 0
    if newvalue > 3:
        newvalue = 3

    return newvalue


# Let's write a function that updates the entire grid once, according to the rules.
# We apply a 'synchronous' update, meaning that we first copy the old grid and use
# that grid for reference to determine what happens next. 
def simulate_step(grid):
    new_grid = grid.copy()  # Make a copy of the current grid state
    for i in range(grid_size):  # loop over all rows
        for j in range(grid_size):  # loop over all columns
            new_grid[i,j] = turing_pattern(grid ,i, j) 
    return new_grid


fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})  # Make the first graph 3 times the height of the second
cols = plt.cm.colors.ListedColormap(['white', 'lightgreen', 'green', 'darkgreen'])
norm = plt.cm.colors.BoundaryNorm(boundaries=[0, 1, 2, 3], ncolors=3)

    
# Finally, run the simulation and update the plots
for t in range(1, timesteps):

    # Plot the grid and number of plants
    if t % 1 == 0:
        ax1.clear()
        ax2.clear()
    
        ax1.imshow(grid.T, cmap=cols, norm=norm, origin='lower')
        ax1.set_title(f"Timestep: {t}")
        ax1.axis("off")
    
        ax2.plot(range(t), nr_plants_list[:t], label='Plants', color='green')
        ax2.set_xlim(0, timesteps)
        ax2.set_ylim(0, grid_size*grid_size)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Plant Number', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        ax2.legend(loc='upper left')

    plt.pause(0.2)  # Pause to refresh the plot
   
    grid = simulate_step(grid)

    # Update number of plants
    nr_plants = np.count_nonzero(grid)
    nr_plants_list[t] = nr_plants

# And open the last plot. 
plt.show()
