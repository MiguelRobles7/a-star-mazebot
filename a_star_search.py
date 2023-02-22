import queue
# to keep track of the blocks of maze
class Grid_Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# each block will have its own position and cost of steps taken
class Node:
    def __init__(self, pos: Grid_Position, cost):
        self.pos = pos
        self.cost = cost

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        else:
            return False

def manhattan_distance(curr_node,dest):
    return (abs(curr_node.x-dest.x)+abs(curr_node.y-dest.y))

def A_Star(maze, end, start, size):
    # Create lists for open nodes and closed nodes
    pq = queue.PriorityQueue() #I'm not sure if we can use this but makes life much easier, we can ask sir, if not we can manually sort the list
    closed = [[False for i in range(size)]
                      for j in range(size)] # all in the closed list are unexplored for now
    closed[start.x][start.y] = True # start node is explored

    # will be used to get neighbors 
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]

    # Create a start node and an goal node
    Start = Node(start, 0)

    # Add the start node
    pq.put((0, Start))
    cost = 0
    cells = 4

    # Loop until the open list is empty
    while pq:
    # Sort the open list to get the node with the lowest cost first
        # for now since using priority queue we don't need to sort manually

    # Get the node with the lowest cost
        current = pq.get() # priority queue automatically gets lowest cost node 
        current_node = current[1] 
        current_pos = current_node.pos

    # Add the current node to the closed list
        if current_node not in closed:
            closed[current_pos.x][current_pos.y] = True
            cost = cost + 1

    # Check if we have reached the goal, return the path if we have
        if current_pos.x == end.x and current_pos.y == end.y:
            print("Algorithm used = A* Algorithm")
            print("No. of moves utilized = ", cost)
            return closed

        x_pos = current_pos.x
        y_pos = current_pos.y

    # If not, we get neighbours 
        for i in range(cells):
            if x_pos == len(maze) - 1 and adj_cell_x[i] == 1:
                x_pos = current_pos.x
                y_pos = current_pos.y + adj_cell_y[i]
            if y_pos == 0 and adj_cell_y[i] == -1:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y
            else:
                x_pos = current_pos.x + adj_cell_x[i]
                y_pos = current_pos.y + adj_cell_y[i]
            if x_pos < size and y_pos < size and x_pos >= 0 and y_pos >= 0:
                if maze[x_pos][y_pos] == 1:
                    if not closed[x_pos][y_pos]:
                        neighbor = Node(Grid_Position(x_pos, y_pos), current_node.cost + 1)
                        h = manhattan_distance(neighbor.pos, end) #get heuristic value of neighbours
                        f = h + neighbor.cost #getting f by f = h + g
                        closed[x_pos][y_pos] = True #adding neighbour to closed
                        pq.put((f, neighbor))

    return -1
def printMaze(maze):
    for i in maze:
        for a in i:
            print(a, end=" ")
        print()

def main():
    # normalize maze into numbers
    # WHERE 0 = wall, 1 = empty, 2 = start, 3 = end
    file = open("test_mazes/maze.txt", "r")
    size = file.readline().split()[0] 
    row = []
    maze = []
    for c in file.read():
        if c == '#':
            row.append(0)
        elif c == '.':
            row.append(1)
        elif c == 'S':
            row.append(2)
        elif c == 'G':
            row.append(3)
        else:
            maze.append(row)
            row = []

    print("Original Maze:")
    printMaze(maze)

    # look for the beginning position
    (start_x, start_y) = [[(i, j) for j, cell in enumerate(row) if cell == 2] for i, row in enumerate(maze) if 2 in row][0][0]
    # and take the goal position (used in the heuristic)
    (goal_x, goal_y) = [[(i, j) for j, cell in enumerate(row) if cell == 3] for i, row in enumerate(maze) if 3 in row][0][0]
    
    destination = Grid_Position(goal_x, goal_y)
    starting_position = Grid_Position(start_x, start_y)

    # we have their coordinates so turn to 1 (we assume that the start and end are not walls)
    maze[start_x][start_y] = 1
    maze[goal_x][goal_y] = 1

    print(f"\nStart: {start_x}, {start_y}\nDestination: {goal_x}, {goal_y}")
    
    # Returns the closed list, we can use this to simulate making a maze
    path = A_Star(maze, destination, starting_position, int(size))
    count = 1 # to get explored order
    
    for a in range(len(path)):
        for i in range(len(path[0])):
            if path[a][i]:
                if count < 10:
                    maze[a][i] = "0" + str(count)
                else:
                    maze[a][i] = count
                count+=1
            elif maze[a][i] == 0:
                maze[a][i] = "##"
            elif maze[a][i] == 1:
                maze[a][i] = ".."

    print("\nSolved Maze Path: ")
    printMaze(maze)

if __name__ == '__main__':
    main()