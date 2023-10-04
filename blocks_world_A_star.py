'''
This project populates a 9x9 grid and then randomly populates the numbers 1-9 into it
It then moves one block at a time until either the solution is found using A* algorithm
'''
import numpy as np
import random
import time

start_time = time.time()
#Sets constant vals and populates world with 0's
NUM_BLOCKS = 9

world = np.zeros((NUM_BLOCKS, NUM_BLOCKS))

def pretty_print(world):
  ### Prints grid W/O array and zeros
  for row in world:
    for value in row:
      if value != 0:
        print(int(value), end=" ")
      else:
        print(" ", end=' ')
    print()


def initialize_world(world):
  ##Randomly places blocks on grid
  rand_num = np.random.default_rng()
  one = 1
  two = 1
  three = 1
  four = 1
  five = 1
  six = 1
  seven = 1
  eight = 1
  nine = 1
  for i in range(NUM_BLOCKS):
    num = random.randrange(1, NUM_BLOCKS, 1)
    if num == 1:
      world[-one][0] = i+1
      one += 1
    elif num == 2:
      world[-two][1] = i+1
      two += 1
    elif num == 3:
      world[-three][2] = i+1
      three += 1
    elif num == 4:
      world[-four][3] = i+1
      four += 1
    elif num == 5:
      world[-five][4] = i+1
      five += 1
    elif num == 6:
      world[-six][5] = i+1
      six += 1
    elif num == 7:
      world[-seven][6] = i+1
      seven += 1
    elif num == 8:
      world[-eight][7] = i+1
      eight += 1
    elif num == 9:
      world[-nine][8] = i+1
      nine += 1
  return world

def calc_heuristic(world, NUM_BLOCKS):
  #Calculates heuristic score
  heur = 3*NUM_BLOCKS
  #Maximum of 18, solution at 0
  for i in range(1, NUM_BLOCKS+1, 1):
    ind = np.where(world[:][-(i)] == i)[0]
    #Gets column where given value is found
    if (np.any(world[:][-i] == i)) and (((world[-(i-1)][ind])[0] == i-1) or i == 1):
    #Checks if value is in right row (1 on bottom row, 9 on top row, etc) and if preceding value is directly below it
    #Execption for 1 since it is the minimum value
      heur -= 3
    #Larger heuristic deduction encourages correct stacking, if possible
    else:
      if (np.any(world[:][-1] == i)):
    #Checks if given value is on bottom row if previous logic statement is false
    #this helps prime blocks world for efficient stacking
        heur -= 1
    #Encourages flattening out the world if logic statement is false, but lesser value so stacking happens if possible
      else:
        heur += 1
  return heur


def check_next_vals(world, min_heur, NUM_BLOCKS):
  #Checks and stores all possible next moves and chooses best one
  nodes = []
  #Keeps track of possible moves
  for i in range(len(world)):
    #iterates through all columns
    #makes copy of world so that it is not modified all the time
    world_copy = world.copy()
    if len((np.where(world[:,i]!=0))[0]) > 0:
      #Makes sure there are non-zero values in column, skips if there aren't
      index = (np.where(world[:,i]!=0))[0]
      val = world[index.min()][i]
      #finds and saves 'top' non-zero value in given column
      world_copy[index.min()][i] = 0
      #Sets location to zero


      for j in range(len(world)):
        #Iterares throughevery column again and makes another copy to prevent modification
        world_copy2 = world_copy.copy()
        if len((np.where(world_copy2[:,j]==0))[0]) > 0:
        #Makes sure column isn't full (probably not needed)
          index2 = (np.where(world_copy2[:,j]==0))[0]
          world_copy2[index2.max()][j] = val
          #Places saved value at lowest 0 spot in column

          if calc_heuristic(world_copy2, NUM_BLOCKS) < min_heur:
            save_val = world_copy2
            min_heur = calc_heuristic(world_copy2, NUM_BLOCKS)
          #calculates heuristic and saves world state and heuristic score if new minimum is found
          nodes.append(world_copy2)
          #Adds node to list regardless


  world = save_val

  min_heuristic = min_heur
  #Assigned world and heuristic values to best solution found for given move

  return world, min_heuristic, nodes





def shuffle_blocks(world, NUM_BLOCKS):
  #Keeps track of iterations
  counter = 1
  #Set minumum heuristic score at maximum possible
  min_heur = 3*NUM_BLOCKS
  #
  generated_nodes = []
  #While loop continues until goal is reached
  while min_heur > 0:
    #returns best move, heuristic score of best move, and list of all possible moves
    world, min_heur, nodes = check_next_vals(world, min_heur, NUM_BLOCKS)
    #Appends list of possible nodes on given move to list of all nodes

    generated_nodes.append(nodes)
    print("------------------")
    pretty_print(world)
    print("------------------")
    print("Iteration:", counter)
    print('Heuristic Score:', min_heur)
    counter += 1


new_world = initialize_world(world)
shuffle_blocks(new_world, NUM_BLOCKS)
print("--- %s seconds ---" % (time.time() - start_time))