import itertools
import numpy
import math

# returns 1 if kings k1 and k2 are attacking each other, 0 o.w.
def kingattacking(k1col, k1row, k2col, k2row):
  coldiff=k1col-k2col
  rowdiff=k1row-k2row

  if k1col==k2col and abs(rowdiff) == 1:
    return 1  # same column
  if k1row==k2row and abs(coldiff) == 1:
    return 1  # same row
  if abs(coldiff)==1 and abs(rowdiff)==1:
    return 1  # same diagonal
  return 0

def kingfitnessmulticolumn(encoding):
  E = 13
  for i in range(1,14):
    for j in range(i+1,15):
      E -= kingattacking(encoding[i-1][0], encoding[i-1][1], encoding[j-1][0], encoding[j-1][1])
      if (E < 13):
        return 12
  return E

# the following is useful in a variety of algorithms
# returns the nth successor of an encoding
def getsuccessor(init, n, succ):
  n -= 1
  quotient, remainder = divmod(n,13) 
  newrow=init[quotient]+remainder+1
  if newrow>14:
    newrow -= 14
  for j in range(14):
    if j==quotient:
      succ[j]=newrow
    else:
      succ[j]=init[j]

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
  E = 91
  for i in range(1,14):
    for j in range(i+1,15):
      E -= queenattacking(i, encoding[i-1], j, encoding[j-1])
  return E

def heuristicgrid(encoding):
  # grid to store heuristics
  heuristicGrid = numpy.zeros(shape=(14, 14), dtype='int')

  # mark the existing queen placements
  for i in range(14):
    heuristicGrid[i][encoding[i] - 1] = 99
  
  # calculate the fitness of each move
  for i in range(1,183):
    temp = encoding[:]
    getsuccessor(encoding, i, temp)
    
    heuristicGrid[math.floor((i - 1) / 13)][temp[math.floor((i - 1) / 13)] - 1] = 91 - queenfitness(temp)
  
  return heuristicGrid.transpose()

def nkings(encoding):
  print(encoding)
  hgrid = heuristicgrid(encoding)
  print(hgrid)

  safeboard = numpy.zeros(shape=(14, 14), dtype='int')
  safe = []
  for i in range(14):
    for j in range(14):
      if hgrid[i][j] == 1:
        safeboard[i][j] = 1
        # safe[i].append(j)
        safe.append([i,j])
  print(safeboard)
  print("Safe:", safe)

  # print(kingfitnessmulticolumn([[0, 1], [0, 5], [1, 3], [1, 7], [2, 9], [3, 15], [4, 13], [5, 2], [6, 19], [6, 15], [7, 1], [8, 3], [9, 5], [10, 15], [12, 2], [13, 4], [15, 9], [17, 11], [19, 20], [20, 18]]))
  # ncombos([1,2,3,4],3)
  parrangements = -1
  if (len(safe) > 0):
    parrangements = 0
    print("Testing...", len(safe))
    # arrangements = ncombos(safe, 20)
    # for arrangement in arrangements:
    for arrangement in itertools.combinations(safe, 14):
      if kingfitnessmulticolumn(arrangement) == 13:
        print(arrangement)
        parrangements += 1
        print(parrangements)
      if parrangements > 41:
        return "Fail"
  print("Arrangements:", parrangements)
  if parrangements == 41:
        return encoding
  return "Fail"

nkings([2, 10, 8, 6, 4, 13, 11, 14, 12, 7, 5, 3, 1, 9])