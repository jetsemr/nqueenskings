## IBM Ponder This - February 2023 Challenge
# Date: 2-28-2022

import random
import numpy
import math

## kingattakcing
# Description: Returns 1 if kings k1 and k2 are attacking each other, 0 o.w.
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

## kingfitnessmulticolumn
# Description: Returns the fitness of king placement by counting number of conflicts
def kingfitnessmulticolumn(encoding):
  E = 19
  for i in range(1,20):
    for j in range(i+1,21):
      E -= kingattacking(encoding[i-1][0], encoding[i-1][1], encoding[j-1][0], encoding[j-1][1])
      if (E < 19):
        return 18
  return E

import itertools

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
  E = 190
  for i in range(1,20):
    for j in range(i+1,21):
      E -= queenattacking(i, encoding[i-1], j, encoding[j-1])
  return E

## getsuccessor
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

## heuristicgrid
# generates a grid that displays the number of queens attacking each space
def heuristicgrid(encoding):
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
  
  return heuristicGrid

## nkings
# checks if the encoding produces a valid nkings solution
def nkings(encoding):
  print(encoding)
  hgrid = heuristicgrid(encoding)
  # print(hgrid)

  # safeboard = numpy.zeros(shape=(20, 20), dtype='int')
  safe = []
  for i in range(20):
    for j in range(20):
      if hgrid[i][j] == 1:
        # safeboard[i][j] = 1
        safe.append([i,j])
  print("Safe:", safe)

  parrangements = -1
  if (len(safe) == 30):
    parrangements = 0
    print("Testing...", len(safe))
    for arrangement in itertools.combinations(safe, 20):
      if kingfitnessmulticolumn(arrangement) == 19:
        print(arrangement)
        parrangements += 1
        print(parrangements)
      if parrangements > 48:
        return "Fail"
  print("Arrangements:", parrangements)
  if parrangements == 48:
        return encoding
  return "Fail"

## kings_from_queens_files
# reads valid queen placements and runs nkings
def kingsfromqueensfile():
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

kingsfromqueensfile()
