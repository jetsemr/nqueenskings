## IBM February 2023 Ponder This Research Challenge
**Problem**: Find a placement of n=20 queens on an n * n board such that no pair of queens threatens each other, and the number of different ways to place n kings on the safe squares without any pair of kings currently threatening one another is 48.

I participated in this challenge while taking "Intro to Artificial Intelligence" at the University of Kansas. For my solution, I implemented a random restart hill climbing algorithm to generate feasible board configurations until a solution was found.

This solution is generally inefficient, but will eventualy find a solution. 
1. Execute **generatequeens.py** to generate a list of boards with positions that fit the queens requirement. Each hill climb starts with a random board encoding and uses a heuristic grid to find valid configurations of the board. This computation is expensive and needs to generate ~5000 boards to find a valid solution to the problem.
2. Execute **nkingsverification.py** to iterate through the list of queens until a valid solution is found. This will take a long time, but it will find a correct solution if it is generated in step 1.

https://research.ibm.com/haifa/ponderthis/challenges/February2023.html
