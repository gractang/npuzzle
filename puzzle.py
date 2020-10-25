import sys
import math
import time

def DebugPrint(state):
	n = int(math.sqrt(len(state)))
	for row in range(n):
		for col in range(n):
			print(str(state[row*n+col]) + ' ', end='')
		print()

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


def IsGoal(state):
	state = list(state)
	print(state)

	for i in range(len(state)):
		if i == 0:
			continue
		if state[i] < state[i-1]:
			return False
	return True

def Swap(i, j, arr):
	a = arr[:]
	a[i] = arr[j]
	a[j] = arr[i]
	return a

start = time.time()
file_path = sys.argv[1]
print(file_path)
board = LoadFromFile(file_path)
#print(board)
DebugPrint(board)
#print(IsGoal(board))
# print(BuildPositions(3))

# wack variable name so that autograder hopefully doesn't die
gracs_cool_dictionary = BuildPositions(int(math.sqrt(len(board))))
# print(gracs_cool_dictionary)


# this should work?
def ComputeNeighbors(state):
	n = int(math.sqrt(len(state)))
	index = -1
	for i in range(len(state)):
		if state[i] == n*n:
			index = i
			break
	pos = BuildPositions(n)
	adjacents = pos[index]

	pairs = []

	for adj in adjacents:
		num = state[adj]
		neighbor_state = Swap(index, adj, list(state))
		pairs.append((num, tuple(neighbor_state)))

	return pairs


def BFS(state):
	frontier = [tuple(state)]
	discovered = set(state)
	parents = {tuple(state): None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(tuple(current_state))
		if IsGoal(current_state):
			temp = current_state
			moves = []
			print(parents)
			while parents[temp]:
				parent = parents[temp]
				moves.append(parent[0])
				# print(parent[0])
				# print(parent[1])
				temp = parent[1]
			return moves[::-1]
			# return the path you need by backtracking in parents

		for neighbor in ComputeNeighbors(current_state):
			# print(neighbor)
			# print("neighbor: " + str(type(neighbor)))
			if neighbor not in discovered:
				frontier.append(neighbor[1])
				discovered.add(neighbor[1])

				# add neighbor: current_state to the parents map
				parents[neighbor] = current_state

# print(ComputeNeighbors(board))
# print(ComputeNeighbors([7,8,2,1,4,3,5,9,6]))
print(BFS(board))

end = time.time()
print(f"Runtime of the program is {end - start}")