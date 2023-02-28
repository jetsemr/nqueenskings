## 8-Queens Problem solved via min conflicts algorithm
# Date: 2-22-2022

import random
import numpy
import math
from copy import deepcopy

## QUEENS

# returns 1 if queens q1 and q2 are attacking each other, 0 o.w.
def queenattacking(q1col, q1row, q2col, q2row):
  if q1col==q2col:
    return 1  # same column
  if q1row==q2row:
    return 1  # same row
  coldiff=q1col-q2col
  rowdiff=q1row-q2row
  if abs(coldiff)==abs(rowdiff):
    return 1  # same diagonal
  return 0

# evaluates the fitness of an encoding, defined as the number of
# non-attacking pairs of queens (28 - number of attacking pairs)
#
# the global variable EVALS keeps track of the number of times called
def queenfitness(encoding):
  E = 190
  for i in range(1,20):
    for j in range(i+1,21):
      E -= queenattacking(i, encoding[i-1], j, encoding[j-1])
  return E

# the following is useful in a variety of algorithms
# returns the nth successor of an encoding
def getsuccessor(init, n, succ):
  n -= 1
  quotient, remainder = divmod(n,19) 
  newrow=init[quotient]+remainder+1
  if newrow>20:
    newrow -= 20
  for j in range(20):
    if j==quotient:
      succ[j]=newrow
    else:
      succ[j]=init[j]

# find neighbor
def findNeighbor(encoding):
  # grid to store heuristics
  heuristicGrid = numpy.zeros(shape=(20, 20), dtype='int')

  # mark the existing queen placements
  for i in range(20):
    heuristicGrid[i][encoding[i] - 1] = 99

  # calculate the fitness of each move
  for i in range(1,381):
    temp = encoding[:]
    getsuccessor(encoding, i, temp)
    
    heuristicGrid[math.floor((i - 1) / 19)][temp[math.floor((i - 1) / 19)] - 1] = 190 - queenfitness(temp)
  
  minNeighbor = [0,0]

  for i in range(20):
    for j in range(20):
      if heuristicGrid[i][j] < heuristicGrid[minNeighbor[0]][minNeighbor[1]]:
        minNeighbor = [i,j]

  return minNeighbor

# hill climb
def nqueens(encoding):
  # current <-- problem.initial
  current = encoding

  while(1):
    # neighbor <- highest value successor
    neighbor = deepcopy(current)
    highestValueSuccessor = findNeighbor(current)
    neighbor[highestValueSuccessor[0]] = highestValueSuccessor[1] + 1

    # return condition
    if queenfitness(neighbor) <= queenfitness(current):
      return current
    
    # current <-- neighbor
    current = neighbor

# random restart
def RR(limit):
  count = 0
  while (count < limit):

    # track number of iterations
    count += 1

    # generate a random encoding
    encoding = []
    for _ in range(20):
      encoding.append(random.randint(1,20))

    # run the hill climb
    solution = nqueens(encoding)

    # check solution
    if queenfitness(solution) == 190:
      return solution
  return "Fail"


def test():
  for i in range(100000):
    print("Run:",i)
    run = RR(100)
    if run != "Fail":
      mystring=' '.join(map(str,run))
      f = open("nqueens.txt", "a")
      f.write(mystring)
      f.write("\n")
  f.close()
  return "Done"

print(test())
