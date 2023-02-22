import queue
from enum import Enum
class TileType(Enum):
	WALL = 0
	EMPTY = 1
	START = 2
	END = 3
# to keep track of the blocks of maze
class Point:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y
	def __lt__(self, _): #to fix issues on pq
		return False

def manhattan_distance(src: Point, dst: Point):
	return (abs(src.x-dst.x)+abs(src.y-dst.y))

def getValidMoves(maze: list[list[TileType]], point: tuple[int,int]) -> list[tuple[int,int]]:
	size_x, size_y = len(maze), len(maze[0])
	validMoves = []
	for offset in [(1,0),(0,1),(-1,0),(0,-1)]:
		x, y = point[0] + offset[0], point[1] + offset[1]
		if x < 0 or y < 0 or x >= size_x or y >= size_y:
			continue
		if maze[x][y] != TileType.WALL:
			validMoves.append((x, y))
	return validMoves

def A_Star(
	maze: list[list[TileType]], 
	end: Point, start: Point) -> tuple[
		list[tuple[int,int]],
		list[tuple[int,int]]
	]:

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
		child_cost = costs[curr.x][curr.y] + 1 #the cost of each action is 1
		for (x, y) in getValidMoves(maze, (curr.x, curr.y)):
			if costs[x][y] != -1:
				continue

			costs[x][y] = child_cost
			order.append((x, y))

			child = Point(x, y)
			pq.put((
				costs[x][y] + manhattan_distance(child, end), 
				child
			))

	end = (end.x, end.y)
	start = (start.x, start.y)
	optimal_path = [end]
	while start != optimal_path[-1]:
		a = optimal_path[-1]
		child_cost = costs[a[0]][a[1]] - 1
		for (x, y) in getValidMoves(maze, a):
			if costs[x][y] == child_cost:
				optimal_path.append((x,y))
				break
	optimal_path.reverse()
	return optimal_path, order


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
	optimal_path, order = A_Star(maze, goal, start)

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

if __name__ == '__main__':
	main()