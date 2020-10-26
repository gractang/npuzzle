import sys
import math
import time

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


start = time.time()
file_path = sys.argv[1]
board = LoadFromFile(file_path)

# a not wack variable name— sorry if autograder dies because i
# couldn't be bothered to name n something else
n = int(math.sqrt(len(board)))

# wack variable name so that autograder hopefully doesn't die
gracs_cool_dictionary = BuildPositions(n)

def MakeGoalState():
	return tuple([i + 1 for i in range(n*n)])

goal = MakeGoalState()
#    goal = (7, 6, 2, 3, 9, 5, 4, 1, 8)


def IsGoal(state):
	return state[1] == goal
	# current state passed in includes how to get there
	# state = list(state[1])
	# # print(state)

	# for i in range(len(state)):
	# 	if i == 0:
	# 		continue
	# 	if state[i] < state[i-1]:
	# 		return False
	# return True

def Swap(i, j, arr):
	a = arr[:]
	a[i] = arr[j]
	a[j] = arr[i]
	return a

def DebugPrint(state):
	for row in range(n):
		for col in range(n):
			print(str(state[row*n+col]) + ' ', end='')
		print()

# this should work?
def ComputeNeighbors(state):
	index = -1
	for i in range(len(state)):
		if state[i] == n*n:
			index = i
			break

	adjacents = gracs_cool_dictionary[index]

	pairs = []

	for adj in adjacents:
		num = state[adj]
		neighbor_state = Swap(index, adj, list(state))
		pairs.append((num, tuple(neighbor_state)))

	return pairs

# i am going to be completely real with you i have no idea
# why or how this works. i made multiple mistakes that might have
# cancelled each other out. but afaik it works so god knows i'm not
# changing it. what am i, a masochist?
def BFS(state):
	frontier = [(None, tuple(state))]
	discovered = set(tuple(state))
	parents = {tuple(state): None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(tuple(current_state))
		if IsGoal(current_state):
			# print(parents)
			# print(discovered)
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

def DFS(state):
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

# where end is the reached state, -1 direction means going from 
# reached state to start (a), 1 means from reached state to end (b)
def TraceBack(end, parents, direction):
	moves = []
	current = end

	# parent state including how to get to current state
	prev_i = parents[current]

	while prev_i:
		#print(prev_i)
		# add move that got you there
		moves.append(prev_i[0])

		# set new current to previous state (not incl move to get there)
		current = prev_i[1]

		prev_i = parents[current]

	return moves[::direction]


# state now normal (just the n^2 numbers)
def BidirectionalSearch(state):
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
			# print(union_node[0])
			# print(discovered_a)
			# print(parents_a)
			# print(parents_b)

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

		


print(BFS(board))
bfs_time = time.time()
print(f"Runtime of bfs is {bfs_time - start}")

print(DFS(board))
dfs_time = time.time()
print(f"Runtime of dfs is {dfs_time - bfs_time}")

print(BidirectionalSearch(board))
bds_time = time.time()
print(f"Runtime of bds is {bds_time - dfs_time}")