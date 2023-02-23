from a_star_search import A_Star, initMaze
from pyamaze import maze

def main():
	optimal_path, order = A_Star(*initMaze("test_mazes/maze.txt"))
	m=maze()
	m.CreateMaze()
	m.run()


if __name__ == '__main__':
	main()