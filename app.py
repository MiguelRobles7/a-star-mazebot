import queue
from enum import Enum
from collections import namedtuple
import webbrowser
import os

"""
to run simply run app.py or gui.py,
FAQs, Troubleshooting, and further instructions in the docs (report.pdf)
"""

class TileType(Enum):
	WALL = 0
	EMPTY = 1
	START = 2
	END = 3
# to keep track of the blocks of maze
class Point(namedtuple('Point', ['x', 'y'])):
	def __lt__(self,_):
		return False
# manhattan_distance
def manhattan_distance(src, dst):
	return (abs(src[0]-dst[0])+abs(src[1]-dst[1]))
# returns points (up down left right) that are not walls
def get_valid_moves(maze: list[list[TileType]], point) -> list[Point]:
	size_x, size_y = len(maze), len(maze[0])
	valid_moves = []
	for offset in [(1,0),(0,1),(-1,0),(0,-1)]:
		x, y = point[0] + offset[0], point[1] + offset[1]
		if x < 0 or y < 0 or x >= size_x or y >= size_y:
			continue
		if maze[x][y] != TileType.WALL:
			valid_moves.append(Point(x, y))
	return valid_moves
#given the cost table, trace back the path A* took from end to start
def trace_optimal_path(maze, costs, start, end):
	optimal_path = [end]
	while start != optimal_path[-1]:
		a = optimal_path[-1]
		child_cost = costs[a.x][a.y] - 1
		for child in get_valid_moves(maze, a):
			if costs[child.x][child.y] == child_cost:
				optimal_path.append(child)
				break
		else:
			return []
	optimal_path.reverse()
	return optimal_path
#the search algorithm
def a_star(
	maze: list[list[TileType]], 
	start: Point, end: Point) -> tuple[
		list[Point],
		list[Point]
	]:

	if maze[start.x][start.y] == TileType.WALL:
		return [], []
	
	order = [] #the order in which states are explored, not part of the algo

	costs = [[-1 for _ in range(len(maze[i]))] #so that the optimal path can be traced back
				for i in range(len(maze))] # from end to start and to check if state is explored
	
	
	pq = queue.PriorityQueue() #(priority, heuristic, state)
	pq.put((0, 0, start))

	while not pq.empty():
		prio, h, curr = pq.get()
		#the heuristic is consistent so the cost of the state is optimal once it is explored
		if costs[curr.x][curr.y] != -1:
			continue
		#a state is explored when its child nodes are expanded
		#so this is placed in the outer loop
		costs[curr.x][curr.y] = prio - h
		order.append(curr)
		if curr == end:
			return trace_optimal_path(maze, costs, start, end), order
		child_cost = prio - h + 1 #the cost of each action is 1
		for child in get_valid_moves(maze, curr):
			(x, y) = child
			if costs[x][y] != -1: #not yet explored
				continue 

			heuristic = manhattan_distance(child, end)

			pq.put((
				heuristic + child_cost,
				heuristic,
				child,
			))

	return [], order #the end state is unreachable
def init_maze(fname):
	maze = [ ]
	file = open(fname, 'r')
	file.readline().split()[0]
	types = {
		'#': TileType.WALL,
		'.': TileType.EMPTY,
		'S': TileType.START,
		'G': TileType.END
	}
	for row in file.read().strip().split('\n'):
		maze.append(list(map(lambda c: types[c], row)))
	# look for the beginning position
	(start_x, start_y) = [
		[(i, j) for j, cell in enumerate(row) if cell == TileType.START]
		for i, row in enumerate(maze) if TileType.START in row
	][0][0]
	# and take the goal position (used in the heuristic)
	(goal_x, goal_y) = [
		[(i, j) for j, cell in enumerate(row) if cell == TileType.END]
		for i, row in enumerate(maze) if TileType.END in row
	][0][0]

	# we have their coordinates so turn to 1 (we assume that the start and end are not walls)
	maze[start_x][start_y] = TileType.EMPTY
	maze[goal_x][goal_y] = TileType.EMPTY

	return maze, Point(start_x, start_y), Point(goal_x, goal_y)
def main():
	maze, start, goal = init_maze("test_mazes/maze.txt")

	print("Create animation? (y/n)")
	an = input()

	print("Original Normalized Maze:")
	
	for i in maze:
		for a in i:
			print(a.value, end=" ")
		print()
	
	# x is y (as coordinates)
	print(f"Start: {start.y}, {start.x} Destination: {goal.y}, {goal.x}")
	
	# Returns the closed list, we can use this to simulate making a maze
	optimal_path, order = a_star(maze, start, goal)

	if an == 'y':
		optimal_count = 0
		squares_explored = 0
		f = open("website/optimal.txt", "w")
		for i in optimal_path:
			f.write(str(i[0]) + "," + str(i[1]) + "\n")
			optimal_count += 1
		f.close()

		f = open("website/order.txt", "w")
		for i in order:
			f.write(str(i[0]) + "," + str(i[1]) + "\n")
			squares_explored += 1
		f.close()

		f = open("website/maze.txt", "w")
		for i in maze:
			for a in i:
				f.write(str(a.value))
			f.write("2")
		f.close()

		f = open("website/info.txt", "w")
		f.write("Size: " + str(len(maze[0])) + "\n")
		f.write("Starting Position: " + str(start.y) + "," + str(start.x) + "\n")
		f.write("Goal Position: " + str(goal.y) + "," + str(goal.x) + "\n")
		f.write("Number of Squares Explored: " + str(squares_explored) + "\n")
		f.write("Optimal Squares to Goal: " + str(optimal_count))
		f.close()

	for a in range(len(maze)):
		for i in range(len(maze[0])):
			if maze[a][i] == TileType.WALL:
				maze[a][i] = "##"
			else:
				maze[a][i] = ".."

	count = 1 # to get explored order
	for (x, y) in optimal_path:
		maze[x][y] = f"{count:02}"
		count+=1

	print("Solved Maze Path: ")
	for i in maze:
		for a in i:
			print(a, end=" ")
		print()

	count = 1 # to get explored order
	for (x, y) in order:
		maze[x][y] = f"{count:02}"
		count+=1
	print("\nOrder:")
	for i in maze:
		for a in i:
			print(a, end=" ")
		print()

	if an == "y":
		print("\nAnimation created! If not automatically opened, go to http://localhost:9000/website/index.html\n\n")
		webbrowser.open('http://localhost:9000/website/index.html', new=0, autoraise=True)
		os.system('python -m http.server 9000')

if __name__ == '__main__':
	main()
