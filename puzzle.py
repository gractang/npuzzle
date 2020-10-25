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


def IsGoal(state):

	# current state passed in includes how to get there
	state = list(state[1])
	# print(state)

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
board = LoadFromFile(file_path)

# a not wack variable name— sorry if autograder dies because i
# couldn't be bothered to name n something else
n = int(math.sqrt(len(board)))

# wack variable name so that autograder hopefully doesn't die
gracs_cool_dictionary = BuildPositions(n)

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


def BFS(state):
	frontier = [(None, tuple(state))]
	discovered = set((None, tuple(state)))
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




print(BFS(board))

end = time.time()
print(f"Runtime of the program is {end - start}")