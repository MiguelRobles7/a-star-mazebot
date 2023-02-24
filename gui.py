from a_star_search import A_Star, initMaze, TileType
from pyamaze import maze, COLOR, agent
def getWalls(m):
	return [(ix,iy) for ix, row in enumerate(m) for iy, i in enumerate(row) if i == TileType.WALL]
def main():
	map, start, goal = initMaze("test_mazes/maze.txt")
	optimal_path, order_path = A_Star(map, start, goal)
	m=maze()
	m.CreateMaze(map, theme=COLOR.dark)


	wall_agent=agent(m, color=COLOR.dark)
	order_agent=agent(m, color=COLOR.blue, count=True)
	optimal_agent=agent(m, color=COLOR.green)
	m.tracePath({wall_agent:getWalls(map)}, delay=0)
	m.tracePath({order_agent:order_path}, delay=600)
	m.tracePath({optimal_agent:optimal_path}, delay=300)
	m.run()


if __name__ == '__main__':
	main()