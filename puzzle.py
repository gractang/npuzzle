import sys

def read_data(file_path):
	file = open(file_path, "r")
	print(file.read())
	

def is_goal(state):
	return True

def compute_neighbors(state):
	return []

def BFS(state):
	frontier = [state]
	discovered = set(state)
	parents = {state: None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(current_state)
	if is_goal(current_state):
		# return the path you need by backtracking in parents
	for neighbor in compute_neighbors(current_state):
		if neighbor not in discovered:
			frontier.append(neighbor)
			discovered.add(neighbor)
			# add neighbor: current_state to the parents map

if __name__ == '__main__':
	filename = sys.argv[1]
	print(filename)
	read_data(file_path)