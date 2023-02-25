from app import TileType
"""
License
https://www.youtube.com/c/LearningOrbis
Copyright (c) 2021 Muhammad Ahsan Naeem
mahsan.naeem@gmail.com


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from tkinter import *
from enum import Enum

class COLOR(Enum):
	'''
	This class is created to use the Tkinter colors easily.
	Each COLOR object has two color values.
	The first two objects (dark and light) are for theme and the two color
	values represent the Canvas color and the Maze Line color respectively.
	The rest of the colors are for Agents.
	The first value is the color of the Agent and the second is the color of
	its footprint
	'''
	dark=('gray11','white')
	light=('white','black')
	black=('black','dim gray')
	red=('red3','tomato')
	cyan=('cyan4','cyan4')
	green=('green4','pale green')
	blue=('DeepSkyBlue4','DeepSkyBlue2')
	yellow=('yellow2','yellow2')

class agent:
	'''
	The agents can be placed on the maze.
	They can represent the virtual object just to indcate the cell selected in Maze.
	Or they can be the physical agents (like robots)
	They can have two shapes (square or arrow)
	'''
	def __init__(self,parentMaze,color:COLOR=COLOR.blue, count=False):
		'''
		parentmaze-->  The maze on which agent is placed.
		x,y-->  Position of the agent i.e. cell inside which agent will be placed
				Default value is the lower right corner of the Maze
		shape-->    square or arrow (as string)
		goal-->     Default value is the goal of the Maze
		filled-->   For square shape, filled=False is a smaller square
					While filled =True is a biiger square filled in complete Cell
					This option doesn't matter for arrow shape.
		footprints-->   When the aganet will move to some other cell, its footprints
						on the previous cell can be placed by making this True
		color-->    Color of the agent.
		
		_orient-->  You don't need to pass this
					It is used with arrow shape agent to shows it turning
		position--> You don't need to pass this
					This is the cell (x,y)
		_head-->    You don't need to pass this
					It is actually the agent.
		_body-->    You don't need to pass this
					Tracks the body of the agent (the previous positions of it)
		'''
		self._parentMaze=parentMaze
		self.color=color
		if(isinstance(color,str)):
			if(color in COLOR.__members__):
				self.color=COLOR[color]
			else:
				raise ValueError(f'{color} is not a valid COLOR!')
		self.filled=True
		self.shape='square'
		self._orient=0
		self.footprints=True
		self._parentMaze._agents.append(self)
		self._body=[]
		self.count = count
		self.steps = 0
		self.x = -1
		self.y = -1
		
	@property
	def x(self):
		return self._x
	@x.setter
	def x(self,newX):
		self._x=newX
	@property
	def y(self):
		return self._y
	@y.setter
	def y(self,newY):
		self._y=newY
	
	def updatePos(self):
		w=self._parentMaze._cell_width
		x=self.x*w+self._parentMaze._LabWidth
		y=self.y*w+self._parentMaze._LabWidth
		
		coord = self._coord=(y, x,y + w, x + w)
		pos = self.position
		labels = self._parentMaze.maze_label

		self._head=self._parentMaze._canvas.create_rectangle(*coord, fill=self.color.value[1], outline='')
		if self.count:
			self.steps += 1
			labels[pos] = str(self.steps)
		if pos in labels:
			self._parentMaze._canvas.create_text((coord[0]+w/2,coord[1]+w/2), text = labels[pos], fill='black')
		

	@property
	def position(self):
		return (self.x,self.y)
	@position.setter
	def position(self,newpos):
		self.x=newpos[0]
		self.y=newpos[1]
		self._position=newpos
class textLabel:
	'''
	This class is to create Text Label to show different results on the window.
	'''
	def __init__(self,parentMaze,title,value):
		'''
		parentmaze-->   The maze on which Label will be displayed.
		title-->        The title of the value to be displayed
		value-->        The value to be displayed
		'''
		self.title=title
		self._value=value
		self._parentMaze=parentMaze
		# self._parentMaze._labels.append(self)
		self._var=None
		self.drawLabel()
	@property
	def value(self):
		return self._value
	@value.setter
	def value(self,v):
		self._value=v
		self._var.set(f'{self.title} : {v}')
	def drawLabel(self):
		self._var = StringVar()
		self.lab = Label(self._parentMaze._canvas, textvariable=self._var, bg="white", fg="black",font=('Helvetica bold',12),relief=RIDGE)
		self._var.set(f'{self.title} : {self.value}')
		self.lab.pack(expand = True,side=LEFT,anchor=NW)

class maze:
	'''
	This is the main class to create maze.
	'''
	def __init__(self):
		'''
		rows--> No. of rows of the maze
		cols--> No. of columns of the maze
		Need to pass just the two arguments. The rest will be assigned automatically
		grid--> A list of all cells
		path--> Shortest path from start(bottom right) to goal(by default top left)
				It will be a dictionary
		_win,_cell_width,_canvas -->    _win and )canvas are for Tkinter window and canvas
										_cell_width is cell width calculated automatically
		_agents-->  A list of aganets on the maze
		markedCells-->  Will be used to mark some particular cell during
						path trace by the agent.
		_
		'''
		self.maze_label={}
		self.path={} 
		self._cell_width=50  
		self._win=None 
		self._canvas=None
		self._agents=[]
		self.markCells=[]

	@property
	def grid(self):
		return self._grid
	@grid.setter        
	def grid(self,n):
		self._grid=[]
		y=0
		for _ in range(self.cols):
			x = 1
			y = 1+y
			for _ in range(self.rows):
				self.grid.append((x,y))
				x = x + 1 
	
	def CreateMaze(self,map:list[list[TileType]],theme:COLOR=COLOR.dark):
		'''
		One very important function to create a Random Maze
		pattern-->  It can be 'v' for vertical or 'h' for horizontal
					Just the visual look of the maze will be more vertical/horizontal
					passages will be there.
		loopPercent-->  0 means there will be just one path from start to goal (perfect maze)
						Higher value means there will be multiple paths (loops)
						Higher the value (max 100) more will be the loops
		saveMaze--> To save the generated Maze as CSV file for future reference.
		loadMaze--> Provide the CSV file to generate a desried maze
		theme--> Dark or Light
		'''
		self.theme=theme
		if(isinstance(theme,str)):
			if(theme in COLOR.__members__):
				self.theme=COLOR[theme]
			else:
				raise ValueError(f'{theme} is not a valid theme COLOR!')
		self.rows = len(map)
		self.cols = len(map[0])
		self.grid=[]
		self._drawMaze(self.theme)

	def _drawMaze(self,theme):
		'''
		Creation of Tkinter window and maze lines
		'''
		
		self._LabWidth=26 # Space from the top for Labels
		self._win=Tk()
		self._win.state('zoomed')
		self._win.title('PYTHON MAZE WORLD by Learning Orbis')
		
		scr_width=self._win.winfo_screenwidth()
		scr_height=self._win.winfo_screenheight()
		self._win.geometry(f"{scr_width}x{scr_height}+0+0")
		self._canvas = Canvas(width=scr_width, height=scr_height, bg=theme.value[0]) # 0,0 is top left corner
		self._canvas.pack(expand=YES, fill=BOTH)
		# Some calculations for calculating the width of the maze cell
		self._cell_width=round(min(
			(scr_height-4*self._LabWidth)/(self.rows+1),
			(scr_width-4*self._LabWidth)/(self.cols+1)
			),3)

	_tracePathList=[]
	def _tracePathSingle(self,a: agent,p,delay):
		'''
		An interal method to help tracePath method for tracing a path by agent.
		'''

		if(len(p)==0):
			del maze._tracePathList[0]
			if len(maze._tracePathList) == 0:
				return
			for q,w in maze._tracePathList[0][0].items():
				a=q
				p=w
			delay=maze._tracePathList[0][1]
		a.x,a.y=p[0]
		a.updatePos()
		del p[0]

		self._win.after(delay, self._tracePathSingle,a,p,delay)    

	def tracePath(self,d,delay=300):
		'''
		A method to trace path by agent
		You can provide more than one agent/path details
		'''
		self._tracePathList.append((d,delay))
		if maze._tracePathList[0][0]==d: 
			for a,p in d.items():
				if len(p)!=0:
					self._tracePathSingle(a,p,delay)
	def run(self):
		'''
		Finally to run the Tkinter Main Loop
		'''
		self._win.mainloop()
