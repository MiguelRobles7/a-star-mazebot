from app import a_star, init_maze, TileType
from pyamaze import maze, COLOR, agent, textLabel
def get_walls(m):
	return [(ix,iy) for ix, row in enumerate(m) for iy, i in enumerate(row) if i == TileType.WALL]
def main():
	map, start, goal = init_maze("test_mazes/maze.txt")
	optimal_path, order_path = a_star(map, start, goal)
	walls = get_walls(map)
	
	m=maze()
	m.CreateMaze(map, theme=COLOR.dark)
	
	textLabel(m, 'Rows/Cols', str(m.rows) + '/' + str(m.cols))
	textLabel(m, 'Empty/Wall', str(m.rows * m.cols - len(walls)) + '/' + str(len(walls)))
	textLabel(m, 'Total explored', len(order_path))
	textLabel(m, 'Optimal explored', len(optimal_path))

	wall_agent=agent(m, color=COLOR.dark)
	order_agent=agent(m, color=COLOR.blue, count=True)
	optimal_agent=agent(m, color=COLOR.green)
	m.tracePath({wall_agent:get_walls(map)}, delay=0)
	m.tracePath({order_agent:order_path}, delay=600)
	m.tracePath({optimal_agent:optimal_path}, delay=300)
	m.run()


if __name__ == '__main__':
	main()
