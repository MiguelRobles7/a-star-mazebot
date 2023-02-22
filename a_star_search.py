import queue
from enum import Enum
class TileType(Enum):
	WALL = 0
	EMPTY = 1
	START = 2
	END = 3
# to keep track of the blocks of maze
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __lt__(self, _): #to fix issues on pq
		return False

def manhattan_distance(curr_node,dest):
	return (abs(curr_node.x-dest.x)+abs(curr_node.y-dest.y))

def getValidMoves(maze, point):
	size_x, size_y = len(maze), len(maze[0])
	validMoves = []
	for offset in [(1,0),(0,1),(-1,0),(0,-1)]:
		x, y = point.x + offset[0], point.y + offset[1]
		if x < 0 or y < 0 or x >= size_x or y >= size_y:
			continue
		if maze[x][y] != TileType.WALL:
			validMoves.append(Point(x, y))
	return validMoves

def A_Star(maze, end, start):

	size_x, size_y = len(maze), len(maze[0]) #size of maze
	pq = queue.PriorityQueue() # holds (priority, point)
	order = [(start.x, start.y)] #the order in which states are explored

	costs = [[-1 for _ in range(size_y)] #so that the optimal path can be traced back
				for _ in range(size_x)] # from end to start and to check if state is explored
	costs[start.x][start.y] = 0

	pq.put((0, start))
	while not pq.empty():
		curr = pq.get()[1]
		if curr.x == end.x and curr.y == end.y:
			break
		parent_cost = costs[curr.x][curr.y]
		for child in getValidMoves(maze, curr):
			x, y = child.x, child.y
			if costs[x][y] != -1:
				continue

			costs[x][y] = parent_cost + 1 #the cost of each action is 1
			order.append((x, y))

			pq.put((costs[x][y] + manhattan_distance(child, end), child))
	return costs, order


def printMaze(maze):
	for i in maze:
		for a in i:
			print(a.value, end=" ")
		print()
def initMaze(fname):
	maze = []
	file = open(fname, 'r')
	file.readline().split()[0]
	types = {
		'#': TileType.WALL,
		'.': TileType.EMPTY,
		'S': TileType.START,
		'G': TileType.END
	}
	for row in file.read().split('\n'):
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
	return maze, Point(start_x, start_y), Point(goal_x, goal_y)
def main():
	maze, start, goal = initMaze("test_mazes/maze.txt")
	print("Original Normalized Maze:")
	printMaze(maze)
	
	# we have their coordinates so turn to 1 (we assume that the start and end are not walls)
	maze[start.x][start.y] = TileType.EMPTY
	maze[goal.x][goal.y] = TileType.EMPTY

	print(f"Start: {start.x}, {start.y} Destination: {goal.x}, {goal.y}")
	
	# Returns the closed list, we can use this to simulate making a maze
	costs, path = A_Star(maze, goal, start)
	count = 1 # to get explored order

	for (x, y) in path:
		maze[x][y] = f"{count:02}"
		count+=1

	for a in range(len(maze)):
		for i in range(len(maze[0])):
			if maze[a][i] == TileType.WALL:
				maze[a][i] = "##"
			elif maze[a][i] == TileType.EMPTY:
				maze[a][i] = ".."

	print("Solved Maze Path: ")
	for i in maze:
		for a in i:
			print(a, end=" ")
		print()
	print("\nCosts:")
	for i in costs:
		for a in i:
			print(f"{a:02}", end=" ")
		print()

if __name__ == '__main__':
	main()