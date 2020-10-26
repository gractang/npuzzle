import sys
import math
import time

# loads the data from the file and formats
# it into a list with n*n replacing the '*'
def LoadFromFile(file_path):
	file = open(file_path, "r")
	n = int(file.readline())
	board = []
	for i in range(n):
		row = file.readline()
		row = row.replace('\n', '')
		row = row.replace('\t', ' ')
		row = row.split()
		int_row = []
		for num in row:
			if num == '*':
				int_row.append(n*n)
			else:
				int_row.append(int(num))
		board.extend(int_row)
	return board

# this is disgusting but i'm too smooth brain to fix it
# builds the adjacency dictionary for each position on the board
# ie position 1 is adjacent to 2 and 5 on n = 4, so it would be
# 1 : [2, 5]
def BuildPositions(n):
	adjacency_dict = {}
	for index in range(n*n):	# for each index
		adjacents = []			# build list of adjacent indexes
		if index == 0: 			# upper left special case
			adjacents.append(index + 1)
			adjacents.append(n)
		elif index == n - 1: 		# upper right special case
			adjacents.append(n - 2)
			adjacents.append(2 * n - 1)
		elif index == n * n - n:	# lower left special case
			adjacents.append(n * n - 2 * n)
			adjacents.append(n * n - n + 1)
		elif index == n * n - 1:		# lower right special case
			adjacents.append(n * n - 1 - n)
			adjacents.append(n * n - 2)
		else:
			if index < n or index > n * n - n: # either first or last row
				adjacents.append(index - 1)
				adjacents.append(index + 1)
				adjacents.append(index + n) if index < n else adjacents.append(index - n)
			elif index % n == 0 or index % n == n - 1: # either first or last col
				adjacents.append(index - n)
				adjacents.append(index + n)
				adjacents.append(index + 1) if index % n == 0 else adjacents.append(index - 1)
			else:
				adjacents.append(index - 1)
				adjacents.append(index + 1)
				adjacents.append(index + n)
				adjacents.append(index - n)
		adjacency_dict[index] = adjacents
	return adjacency_dict

# start = time.time()
# file_path = sys.argv[1]
# board = LoadFromFile(file_path)

# a not wack variable name— sorry if autograder dies because i
# couldn't be bothered to name n something else
n = int(math.sqrt(len(board)))

# wack variable name so that autograder hopefully doesn't die
gracs_cool_dictionary = BuildPositions(n)

# returns a goal state
def MakeGoalState():
	return tuple([i + 1 for i in range(n*n)])

# more global variables in a misguided attempt to make my code faster
goal = MakeGoalState()

# state here has both a move and a state
# checks if state is the goal state
def IsGoal(state):
	return state[1] == goal

# swaps the array elements of arr at indices i and j
# then returns a new array with the things swapped
def Swap(i, j, arr):
	a = arr[:]
	a[i] = arr[j]
	a[j] = arr[i]
	return a

# debug print method that i never actually used to debug
# because— well, i should've, but i didn't
def DebugPrint(state):
	for row in range(n):
		for col in range(n):
			print(str(state[row*n+col]) + ' ', end='')
		print()

# this should work?
# computes the neighbors of a given state
def ComputeNeighbors(state):
	index = -1

	# find index of the space to use it to swap later
	for i in range(len(state)):
		if state[i] == n*n:
			index = i
			break

	adjacents = gracs_cool_dictionary[index]
	pairs = []

	# for each adjacent index
	for adj in adjacents:
		num = state[adj]
		neighbor_state = Swap(index, adj, list(state))
		pairs.append((num, tuple(neighbor_state)))

	return pairs

# returns the number of inversions in state,
# where an inversion is a set of two tiles where 
# a > b but b appears after a
def CountInversions(state):
	i = 0
	inversions = 0
	for num in state:
		if num == n*n:
			num = 0
		
		#print(num)
		for index in range(len(state)):
			if (num > state[index]) and (i < index):
				#print(str(num) + " " + str(state[index]))
				inversions += 1
		i += 1
		#print(inversions)
	return inversions

# checks whether state is solveable using a nifty formula
# returns True if solvable and False if not
def Solvable(state):
	ninv = CountInversions(state)
	row = 0
	for i in range(len(state)):
		if i % n == 0:
			row += 1
		if state[i] == len(state):
			break

	# grid width odd & num inversions even
	# or gridwidth even & parity of row counting from top is same parity of num inversions
	return (n % 2 == 1 and ninv % 2 == 0)  or  (n % 2 == 0 and (row % 2 == ninv % 2))


# i am going to be completely real with you i have no idea
# why or how this works. i made multiple mistakes that might have
# cancelled each other out. but afaik it works so god knows i'm not
# changing it. what am i, a masochist?

# Breadth-First Search finds the shortest path from
# the start state to the end state (if possible).
# it is guaranteed to find a shortest path, as it 
# explores every node on the same level before 
# exploring nodes further down
# arguments: state -- the initial state of the board
# returns the sequence of moves needed to get to the goal state,
#	or None if no such moves exist
def BFS(state):
	if not Solvable(state):
		return None
	frontier = [(None, tuple(state))]
	discovered = set(tuple(state))
	parents = {tuple(state): None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(tuple(current_state))

		if IsGoal(current_state):
			temp = current_state
			moves = []
			key = temp[1]

			# while move to get to it is not none
			while temp[0]:
				moves.append(temp[0])
				temp = parents[key]
				key = temp[1]

			# reverse to get correct order
			return moves[::-1]

		for neighbor in ComputeNeighbors(current_state[1]):
			if neighbor[1] not in discovered:
				frontier.append(neighbor)
				discovered.add(neighbor[1])

				# map parent
				# builds parents such that the state is mapped to
				# (move, parent)
				parents[neighbor[1]] = current_state

# Depth-First Search. just like BFS but slightly lamer in this case,
# since our graph is not particularly dense. explores and finds a path,
# but not necessarily the shortest path, as it explores downwards before
# exploring other nodes at a certain level. uses a stack instead of a
# queue.
# argument: state -- the initial state of the board
# returns the sequence of moves needed to get to the goal state,
#	or None if no such moves exist
def DFS(state):
	if not Solvable(state):
		return None
	frontier = [(None, tuple(state))]
	discovered = set(tuple(state))
	parents = {tuple(state): None}
	while frontier:
		current_state = frontier.pop(-1)
		discovered.add(tuple(current_state))
		if IsGoal(current_state):
			temp = current_state
			moves = []
			key = temp[1]

			# while move to get to it is not none
			while temp[0]:
				moves.append(temp[0])
				temp = parents[key]
				key = temp[1]

			# reverse to get correct order
			return moves[::-1]

		for neighbor in ComputeNeighbors(current_state[1]):
			if neighbor[1] not in discovered:
				frontier.insert(0, neighbor)
				discovered.add(neighbor[1])

				# map parent
				# builds parents such that the state is mapped to
				# (move, parent)
				parents[neighbor[1]] = current_state

# traces through the parents dictionary and finds the path
# to the goal state
# precondition: such a path exists
# arguments:
#	end -- the reached state
# 	parents -- the dictionary of parents and children
#	direction -- where -1 means going from reached state to start,
#				and 1 means going from reached state to end
# returns: a sequence of moves leading from the intial state to the 
#	end state
def TraceBack(end, parents, direction):
	moves = []
	current = end

	# parent state including how to get to current state
	prev_i = parents[current]

	while prev_i:

		# add move that got you there
		moves.append(prev_i[0])

		# set new current to previous state (not incl move to get there)
		current = prev_i[1]

		prev_i = parents[current]

	return moves[::direction]

# starts searching from both ends (the initial state and the goal state)
# faster yay
# this works for 4x4's up until roughly 28 moves,
# at which point it takes more than a minute
# argument: state -- the inital state of the board
# returns: a sequence of moves leading from the inital state to the final
#	state, or None if no such sequence exists
def BidirectionalSearch(state):
	if not Solvable(state):
		return None
	frontier_a = [(None, tuple(state))]
	discovered_a = set()
	discovered_a.add(tuple(state))
	parents_a = {tuple(state): None}
	frontier_b = [(None, goal)]
	discovered_b = set(goal)
	parents_b = {goal: None}

	while frontier_a or frontier_b:
		current_state_a = frontier_a.pop(0)
		discovered_a.add(tuple(current_state_a[1]))

		current_state_b = frontier_b.pop(0)
		discovered_b.add(tuple(current_state_b[1]))

		if discovered_a & discovered_b:
			union_node = discovered_a & discovered_b
			union_node = [n for n in union_node]
			#print(union_node)

			moves = TraceBack(union_node[0], parents_a, -1)
			moves.extend(TraceBack(union_node[0], parents_b, 1))

			return moves

		for neighbor in ComputeNeighbors(current_state_a[1]):
			if neighbor[1] not in discovered_a:
				frontier_a.append(neighbor)
				discovered_a.add(neighbor[1])
				parents_a[neighbor[1]] = (neighbor[0], current_state_a[1])

		for neighbor in ComputeNeighbors(current_state_b[1]):
			if neighbor[1] not in discovered_b:
				frontier_b.append(neighbor)
				discovered_b.add(neighbor[1])
				parents_b[neighbor[1]] = (neighbor[0], current_state_b[1])


# print(BFS(board))
# bfs_time = time.time()
# print(f"Runtime of bfs is {bfs_time - start}")

# print(DFS(board))
# dfs_time = time.time()
# print(f"Runtime of dfs is {dfs_time - bfs_time}")

# print(BidirectionalSearch(board))
# bds_time = time.time()
# print(f"Runtime of bds is {bds_time - start}")
# print(f"Runtime of bds is {bds_time - dfs_time}")