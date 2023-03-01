import numpy
import math

## is_safe
# Description: Checks if a king can be placed at a given row and column given the previously placed kings.
def is_safe(kings, row, col):
    for r, c in kings:
        if (r == None or c == None):
          return True
        if (row == r and abs(col - c) == 1) or (col == c and abs(row - r) == 1) or (abs(row - r) == abs(col - c) and abs(row - r) == 1):
            return False
    return True

## count_safe placements
# Description: Counts the number of ways to place 20 kings on the safe squares given the currently places kings.
def count_safe_placements(kings, spaces):
    if len(kings) == 26:
        return 1
    count = 0
    for i, (row, col) in enumerate(spaces):
        if is_safe(kings, row, col):
            count += count_safe_placements(kings + [(row, col)], spaces[i+1:])
    return count

## queenattacking
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

## queenfitness
# evaluates the fitness of an encoding by calculating the number of attacking queen pairs
def queenfitness(encoding):
  E = 325
  for i in range(1,26):
    for j in range(i+1,27):
      E -= queenattacking(i, encoding[i-1], j, encoding[j-1])
  return E

## getsuccessor
# returns the nth successor of an encoding
def getsuccessor(init, n, succ):
  n -= 1
  quotient, remainder = divmod(n,25) 
  newrow=init[quotient]+remainder+1
  if newrow>26:
    newrow -= 26
  for j in range(26):
    if j==quotient:
      succ[j]=newrow
    else:
      succ[j]=init[j]

## heuristicgrid
# generates a grid that displays the number of queens attacking each space
def heuristicgrid(encoding):
  # grid to store heuristics
  heuristicGrid = numpy.zeros(shape=(26, 26), dtype='int')

  # mark the existing queen placements
  for i in range(26):
    heuristicGrid[i][encoding[i] - 1] = 99
  
  # calculate the fitness of each move
  for i in range(1,651):
    temp = encoding[:]
    getsuccessor(encoding, i, temp)
    
    heuristicGrid[math.floor((i - 1) / 25)][temp[math.floor((i - 1) / 25)] - 1] = 325 - queenfitness(temp)
  
  return heuristicGrid.transpose()

## nkings
# checks if the encoding produces a valid nkings solution
def nkings(encoding):
  print(encoding)
  hgrid = heuristicgrid(encoding)
  print(hgrid)

  # safeboard = numpy.zeros(shape=(20, 20), dtype='int')
  safe = []

  for i in range(26):
    for j in range(26):
      if hgrid[i][j] == 1:
        # safeboard[i][j] = 1
        safe.append([i,j])
  print("Safe:", safe)
  # if (len(safe) < 35 and len(safe) > 30):
  print("Calculating...", len(safe))
  parrangements = count_safe_placements([], safe)
  if parrangements == 0:
    print("Success")
    return encoding
  else:
    print("Arrangements:", parrangements)
    return "Fail"
  # return "Fail"

## kings_from_queens_files
# reads valid queen placements and runs nkings
def kings_from_queens_file():
  f = open("testdata.txt", "r")

  lines = f.readlines()
  run = 0

  for line in lines:
    run += 1
    print("Line:",run)

    q_list = line.split(" ")
    encoding = list(map(int, q_list))
    sol = nkings(encoding)

    if sol != "Fail":
      print(sol)
      return "Success"

  return "Fail"

## solutions
# nkings([20, 15, 6, 1, 10, 5, 13, 18, 3, 12, 7, 2, 14, 9, 19, 16, 8, 11, 17, 4])
# nkings([4, 12, 9, 20, 6, 3, 11, 17, 14, 5, 18, 10, 7, 13, 2, 16, 19, 8, 15, 1])
kings_from_queens_file()