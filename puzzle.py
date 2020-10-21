import sys
import math

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

def Build_Positions(state):
	n = len(state)
	adjacency_dict = {}
	for index in range(n*n):	# for each index
		adjacents = []			# build list of adjacent indexes
		if index == 0: 			# upper left special case
			adjacents.append(1)
			adjacents.append(3)
		elif index == n - 1: 		# upper right special case
			adjacents.append(n - 2)
			adjacents.append(2 * n - 1)
		elif index == n * n - n:	# lower left special case
			adjacents.append(n * n - 2 * n)
			adjacents.append(n * n - n + 1)
		elif index = n * n - 1:		# lower right special case
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
	for i in range(len(state)):
		if i == 0:
			continue
		if state[i] < state[i-1]:
			return False
	return True

def find_neighbors_of_hole(state):
	n = int(sqrt(len(state)))
	index = -1
	for i in range(len(state)):
		if state[i] == n*n:
			index = i
			break


def ComputeNeighbors(state):

	return []

def BFS(state):
	frontier = [state]
	discovered = set(state)
	parents = {state: None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(current_state)
	if IsGoal(current_state):
		# return the path you need by backtracking in parents
		for neighbor in ComputeNeighbors(current_state):
			if neighbor not in discovered:
				frontier.append(neighbor)
				discovered.add(neighbor)
				# add neighbor: current_state to the parents map

if __name__ == '__main__':
	file_path = sys.argv[1]
	print(file_path)
	board = read_data(file_path)
	print(board)
	DebugPrint(board)
	print(IsGoal(board))
	print(IsGoal([7,8,2,1,4,3,5,0,6]))

