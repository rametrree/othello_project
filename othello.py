"""
The reference of this code is www.johnafish.ca

Developed by
Ramet Saelee 6601012620054
Singhanat Pothongkham 6601012610172

Is a mini-project for the Programming Fundamentals subject.
"""

#Library import
from tkinter import *
from tkinter import messagebox
from math import *
from time import *
from random import *
from copy import deepcopy

#mode setup
pvp_mode = False
pvaeasy_mode = False
pvanorml_mode = False
pvahard_mode = False
ava_mode = False

#Tkinter setup
root = Tk()
root.resizable(False,False)
screen = Canvas(root, width=800, height=625, background="#8DDFCB",highlightthickness=0)
screen.pack()

#time
time_running = 0
time_display = StringVar(value="00:00")
after_code = None

#history
turn1 = 1
turn2 = 1

# The Game class is a blueprint for creating game objects.
class Game:
	def __init__(self) :
		#White goes first
		self.player = 0
		self.passed = False
		self.won = False

		#Initializing an empty board
		self.array = []
		for x in range(8):
			self.array.append([])
			for y in range(8):
				self.array[x].append(None)

		#Initializing center values
		self.array[3][3] = "w"
		self.array[3][4] = "b"
		self.array[4][3] = "b"
		self.array[4][4] = "w"

		#Initializing old values
		self.oldarray = self.array

	def update(self):
		screen.delete("highlight")
		screen.delete("tile")
		for x in range(8):
			for y in range(8):
				if self.oldarray[x][y] == "w":
					screen.create_text(75+50*x,74+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
					screen.create_text(75+50*x,72+50*y,tags="tile {0}-{1}".format(x,y),fill="#FFCACC",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")

				elif self.oldarray[x][y] == "b":
					screen.create_text(75+50*x,74+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
					screen.create_text(75+50*x,72+50*y,tags="tile {0}-{1}".format(x,y),fill="#DBC4F0",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
		
		#Animation of new tiles
		screen.update()
		for x in range(8):
			for y in range(8):
				if self.array[x][y] != self.oldarray[x][y] and self.array[x][y] == "w":
					screen.delete("{0}-{1}".format(x,y))
					for i in range(21):
						screen.create_text(75+i+50*x,74+i+50*y,tags="tile animated",fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")	
						screen.create_text(75+i+50*x,72+i+50*y,tags="tile animated",fill="#DBC4F0",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
						if i % 3 == 0:
							sleep(0.003)
						screen.update()
						screen.delete("animated")
					for i in reversed(range(21)):
						screen.create_text(75+i+50*x,74+i+50*y,tags="tile animated",fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
						screen.create_text(75+i+50*x,72+i+50*y,tags="tile animated",fill="#FFCACC",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
						if i % 3 == 0:
							sleep(0.003)
						screen.update()
						screen.delete("animated")

					screen.create_text(75+50*x,74+50*y,tags="tile",fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
					screen.create_text(75+50*x,72+50*y,tags="tile",fill="#FFCACC",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
					screen.update()

				elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="b":
					screen.delete("{0}-{1}".format(x,y))
					for i in range(21):
						screen.create_text(75+i+50*x,74+i+50*y,tags="tile animated",fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
						screen.create_text(75+i+50*x,72+i+50*y,tags="tile animated",fill="#FFCACC",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
						if i % 3 == 0:
							sleep(0.003)
						screen.update()
						screen.delete("animated")
					for i in reversed(range(21)):
						screen.create_text(75+i+50*x,74+i+50*y,tags="tile animated",fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
						screen.create_text(75+i+50*x,72+i+50*y,tags="tile animated",fill="#DBC4F0",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
						if i % 3 == 0:
							sleep(0.003)
						screen.update()
						screen.delete("animated")

					screen.create_text(75+50*x,74+50*y,tags="tile",fill="#aaa",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
					screen.create_text(75+50*x,72+50*y,tags="tile",fill="#DBC4F0",anchor="c",font=("Comic Sans MS",40, "bold"), text="✿")
					screen.update()	

		#Drawing of highlight circles
		for x in range(8):
			for y in range(8):
				if self.player == 0:
					if ValidMove(self.array,self.player,x,y):
						screen.create_text(75+50*x,75+50*y,tags="highlight",fill="#ECEE81",anchor="c",font=("Comic Sans MS",18, "bold"), text="✿")
				else:
					if ValidMove(self.array,self.player,x,y):
						screen.create_text(75+50*x,75+50*y,tags="highlight",fill="#ECEE81",anchor="c",font=("Comic Sans MS",18, "bold"), text="✿")

		if not self.won:
			self.drawScoreBoard()
			screen.update()

		else:
			StopTimer()
			if self.player1_score > self.player2_score:
				screen.create_text(250,550,anchor="c",font=("Comic Sans MS",15, "bold"), text="The game is done!\n  Player 1 WIN.",fill="#FAF3F0")
				msbox = messagebox.askquestion("The game is done!","Player 1 WIN.\nDo you want to restart?")
				if msbox == 'yes':
					PlayGame()
				else:
					pass
			
			elif self.player1_score < self.player2_score:
				screen.create_text(250,550,anchor="c",font=("Comic Sans MS",15, "bold"), text="The game is done!\n  Player 2 WIN.",fill="#FAF3F0")
				msbox = messagebox.askquestion("The game is done!","Player 2 WIN.\nDo you want to restart?")
				if msbox == 'yes':
					PlayGame()
				else:
					pass

			else:
				screen.create_text(250,550,anchor="c",font=("Comic Sans MS",15, "bold"), text="The game is done!\n      DRAW.",fill="#FAF3F0")
				msbox = messagebox.askquestion("The game is done!","DRAW.\nDo you want to restart?")
				if msbox == 'yes':
					PlayGame()
				else:
					pass

	def boardMove(self,x,y):
		# Move and update screen
		self.oldarray = self.array
		if self.player == 0:
			self.oldarray[x][y] = "w"
		else:
			self.oldarray[x][y] = "b"
		self.array = MoveArray(self.array, x, y)

		# Switch Player
		self.player = 1 - self.player

		# Check if player must pass
		self.passTest()

		# Update the board after each move
		self.update()

	def passTest(self):
		mustPass = True
		for x in range(8):
			for y in range(8):
				if ValidMove(self.array,self.player,x,y):
					mustPass = False

		if mustPass:
			self.won = True

		else:
			self.passed = False	

	def drawScoreBoard(self):
		#Deleting prior score elements
		screen.delete("score")

		#Scoring based on number of tiles
		self.player1_score = 0
		self.player2_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y] == "w":
					self.player1_score += 1
				elif self.array[x][y] == "b":
					self.player2_score += 1

		if self.player == 0:
			self.player1_colour = "#ECEE81"
			self.player2_colour = "#8DDFCB"
		else:
			self.player1_colour = "#8DDFCB"
			self.player2_colour = "#ECEE81"	
		
		screen.create_text(130,545,fill=self.player1_colour,font=("Comic Sans MS", 25, "bold"),text="✿")
		screen.create_text(370,545,fill=self.player2_colour,font=("Comic Sans MS", 25, "bold"),text="✿")

		#Pushing text to screen
		screen.create_text(65,500,anchor="c", tags="score",font=("Comic Sans MS", 15, "bold"),fill="#FAF3F0",text="Player 1")
		screen.create_text(435,500,anchor="c", tags="score",font=("Comic Sans MS", 15, "bold"),fill="#FAF3F0",text="Player 2")
		screen.create_rectangle(30,520,100,580,fill="#FAF3F0",outline="#FAF3F0")
		screen.create_text(65,550,anchor="c", tags="score",font=("Comic Sans MS", 45, "bold"),fill="#FFCACC",text=self.player1_score)
		screen.create_rectangle(400,520,470,580,fill="#FAF3F0",outline="#FAF3F0")
		screen.create_text(435,550,anchor="c", tags="score",font=("Comic Sans MS", 45, "bold"),fill="#DBC4F0",text=self.player2_score)

		return self.player1_score,self.player2_score
	
	def easyAI(self):
		#Generates all possible moves
		choices = []
		for x in range(8):
			for y in range(8):
				if ValidMove(self.array,self.player,x,y):
					choices.append([x,y])
		#Chooses a random move, moves there
		if choices:
			movechoices = choice(choices)
			self.boardMove(movechoices[0],movechoices[1])
			Historyplay(movechoices[0],movechoices[1])

	def normalAI(self):
		#Generates all possible choices and boards corresponding to those
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if ValidMove(self.array,self.player,x,y):
					test = MoveArray(self.array,x,y)
					boards.append(test)
					choices.append([x,y])
		
		#Determines the best score based on the prior generated boards and ScoreTest()
		bestScore = -float("inf")
		bestIndex = 0
		for i in range(len(boards)):
			score = self.ScoreNormalTest(boards[i],self.player)
			if score > bestScore:
				bestIndex = i
				bestScore = score

		#Move to the best location based on ScoreTest()
		if choices:
			self.boardMove(choices[bestIndex][0],choices[bestIndex][1])
			Historyplay(choices[bestIndex][0],choices[bestIndex][1])

	def hardAI(self):
		#Generates all possible choices and boards corresponding to those
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if ValidMove(self.array,self.player,x,y):
					test = MoveArray(self.array,x,y)
					boards.append(test)
					choices.append([x,y])

		bestScore = -float("inf")
		bestIndex  = 0
		#Determines the best score based on the prior generated boards and ScoreHardTest()
		for i in range(len(boards)):
			score = self.ScoreHardTest(boards[i],self.player)
			if score > bestScore:
				bestIndex = i
				bestScore = score
		#Move to the best location based on ScoreHardTest()	
		if choices:
			self.boardMove(choices[bestIndex][0],choices[bestIndex][1])
			Historyplay(choices[bestIndex][0],choices[bestIndex][1])

	def ScoreNormalTest(self,array,player):
		score = 0
		#Set player and opponent colours
		if player == 1:
			colour="b"
			opponent="w"
		else:
			colour = "w"
			opponent = "b"
		#+1 if it's player colour, -1 if it's opponent colour
		for x in range(8):
			for y in range(8):
				if array[x][y]==colour:
					score+=1
				elif array[x][y]==opponent:
					score-=1
		return score

	def ScoreHardTest(self,array,player):
		score = 0
		#Set player and opponent colours
		if player==1:
			colour="b"
			opponent="w"
		else:
			colour = "w"
			opponent = "b"
		#Go through all the tiles	
		for x in range(8):
			for y in range(8):
				#Normal tiles worth 1
				add = 1
				#Edge tiles worth 3
				if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
					add=3
				#Corner tiles worth 5
				elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
					add = 5
				#Add or subtract the value of the tile corresponding to the colour
				if array[x][y]==colour:
					score+=add
				elif array[x][y]==opponent:
					score-=add
		return score

def MoveArray(passedArray,x,y):
	#Must copy the passedArray so we don't alter the original
	array = deepcopy(passedArray)
	#Set colour and set the moved location to be that colour
	if board.player==0:
		colour = "w"
		
	else:
		colour = "b"
	array[x][y]=colour
	
	
	#Determining the neighbours to the square
	neighbours = []
	for i in range(max(0,x-1),min(x+2,8)):
		for j in range(max(0,y-1),min(y+2,8)):
			if array[i][j]!=None:
				neighbours.append([i,j])
	
	#Which tiles to convert
	convert = []

	#For all the generated neighbours, determine if they form a line
	#If a line is formed, we will add it to the convert array
	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]
		#Check if the neighbour is of a different colour - it must be to form a line
		if array[neighX][neighY]!=colour:
			#The path of each individual line
			path = []
			
			#Determining direction to move
			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			#While we are in the bounds of the board
			while 0<=tempX<=7 and 0<=tempY<=7:
				path.append([tempX,tempY])
				value = array[tempX][tempY]
				#If we reach a blank tile, we're done and there's no line
				if value==None:
					break
				#If we reach a tile of the player's colour, a line is formed
				if value==colour:
					#Append all of our path nodes to the convert array
					for node in path:
						convert.append(node)
					break
				#Move the tile
				tempX+=deltaX
				tempY+=deltaY
				
	#Convert all the appropriate tiles
	for node in convert:
		array[node[0]][node[1]]=colour

	return array
#Method for drawing the gridlines 
def DrawBackground():
	#Restart button
	#Background/shadow
	screen.create_rectangle(0,5,50,53,fill="#aaa", outline="#aaa")
	screen.create_rectangle(0,0,50,50,fill="#82A0D8", outline="#82A0D8")

	#text Restart
	screen.create_text(25,25,anchor="c",text="Restart",font=("Comic Sans MS", 10, "bold"),fill="#FAF3F0")

	#Create and configure a label to display the time
	time_label = Label(root, textvariable=time_display, font=("Comic Sans MS", 17, "bold"), fg="#FAF3F0",background="#8DDFCB")
	time_label.place(x=250, y=473, anchor="center")
	
    #label position y
	for i in range(1,9):
		screen.create_text(25,25+50*i,anchor="c",text=i,font=("Comic Sans MS", 12, "bold"),fill="#FAF3F0")

    #label position x
	for i in range(1,9):
		col = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H'}
		screen.create_text(25+50*i,25,anchor="c",text=col[i],font=("Comic Sans MS", 12, "bold"),fill="#FAF3F0")

	screen.create_rectangle(50,50,450,450,outline="#FAF3F0",fill="#D4E2D4")
	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		screen.create_line(50,lineShift,450,lineShift,fill="#FAF3F0")

		#Vertical line
		screen.create_line(lineShift,50,lineShift,450,fill="#FAF3F0")

	#history
	screen.create_rectangle(500,40,780,580,outline="#FAF3F0",fill="#D4E2D4")
	screen.create_line(550,40,550,580,fill="#FAF3F0")
	screen.create_line(665,40,665,580,fill="#FAF3F0")
	screen.create_text(610,10,anchor="n",text="Player 1",font=("Comic Sans MS", 12, "bold"),fill="#FAF3F0")
	screen.create_text(730,10,anchor="n",text="Player 2",font=("Comic Sans MS", 12, "bold"),fill="#FAF3F0")
	screen.create_line(500,40,780,40,fill="#FAF3F0")
	for i in range(1,31):
		screen.create_text(525,20+18*i,anchor="n",text=i,font=("Comic Sans MS", 12),fill="#A9A9A9")
		screen.create_line(500,40+18*i,780,40+18*i,fill="#FAF3F0")

	screen.update()

def ValidMove(array,player,x,y):
	#Sets player colour
	if player==0:
		colour="w"
	else:
		colour="b"
		
	#If there's already a piece there, it's an invalid move
	if array[x][y]!=None:
		return False

	else:
		#Generating the list of neighbours
		neighbour = False
		neighbours = []
		for i in range(max(0,x-1),min(x+2,8)):
			for j in range(max(0,y-1),min(y+2,8)):
				if array[i][j]!=None:
					neighbour=True
					neighbours.append([i,j])
		#If there's no neighbours, it's an invalid move
		if not neighbour:
			return False
		else:
			#Iterating through neighbours to determine if at least one line is formed
			valid_move = False
			for neighbour in neighbours:

				neighX = neighbour[0]
				neighY = neighbour[1]
				
				#If the neighbour colour is equal to your colour, it doesn't form a line
				#Go onto the next neighbour
				if array[neighX][neighY]==colour:
					continue
				else:
					#Determine the direction of the line
					deltaX = neighX-x
					deltaY = neighY-y
					tempX = neighX
					tempY = neighY

					while 0<=tempX<=7 and 0<=tempY<=7:
						#If an empty space, no line is formed
						if array[tempX][tempY]==None:
							break
						#If it reaches a piece of the player's colour, it forms a line
						if array[tempX][tempY]==colour:
							valid_move=True
							break
						#Move the index according to the direction of the line
						tempX+=deltaX
						tempY+=deltaY
			return valid_move
	
def GamePlay(event):
	global turn1,turn2,pvp_mode,pvaeasy_mode,pvanorml_mode,pvahard_mode,ava_mode
	xMouse = event.x
	yMouse = event.y
	x = int((event.x-50)/50)
	y = int((event.y-50)/50)
	#Determine the grid index for where the mouse was clicked
    #If the click is inside the bounds and the move is valid, move to that location

	if pvp_mode:
		if xMouse<=50 and yMouse<=50:
			PlayGame()

		else:
			if board.player==0 and turn1 < 32:
				if 0<=x<=7 and 0<=y<=7:
					if ValidMove(board.array,board.player,x,y):
						board.boardMove(x,y)
						Historyplay(x,y)
						turn1 += 1
						
			elif board.player==1 and turn2 < 32:
				if 0<=x<=7 and 0<=y<=7:
					if ValidMove(board.array,board.player,x,y):
						board.boardMove(x,y)
						Historyplay(x,y)
						turn2 += 1
						
	elif pvaeasy_mode:
		if xMouse<=50 and yMouse<=50:
			PlayGame()

		else:
			if board.player==0 and turn1 < 32:
				if 0<=x<=7 and 0<=y<=7:
					if ValidMove(board.array,board.player,x,y):
						board.boardMove(x,y)
						Historyplay(x,y)
						turn1 += 1
						SimulateClick(None)
						
			elif board.player==1 and turn2 < 32:
				board.easyAI()
				board.passTest()
				turn2 += 1
				
				
	elif pvanorml_mode:
		if xMouse<=50 and yMouse<=50:
			PlayGame()

		else:
			if board.player==0 and turn1 < 32:
				if 0<=x<=7 and 0<=y<=7:
					if ValidMove(board.array,board.player,x,y):
						board.boardMove(x,y)
						Historyplay(x,y)
						turn1 += 1
						SimulateClick(None)
						
			elif board.player==1 and turn2 < 32:
				board.normalAI()
				board.passTest()
				turn2 += 1
				
								
	elif pvahard_mode:
		if xMouse<=50 and yMouse<=50:
			PlayGame()

		else:
			if board.player==0 and turn1 < 32:
				if 0<=x<=7 and 0<=y<=7:
					if ValidMove(board.array,board.player,x,y):
						board.boardMove(x,y)
						Historyplay(x,y)
						turn1 += 1
						SimulateClick(None)
						
						
			elif board.player==1 and turn2 < 32:
				board.hardAI()
				board.passTest()
				turn2 += 1
				
				
	elif ava_mode:
		if xMouse<=50 and yMouse<=50:
			PlayGame()
			SimulateClick(None)

		else:
			if board.player==0 and turn1 < 32:
				board.hardAI()
				board.passTest()
				turn1 += 1
				SimulateClick(None)
				
						
			elif board.player==1 and turn2 < 32:
				board.easyAI()
				board.passTest()
				turn2 += 1
				SimulateClick(None)			
			
	else:
		#Menu
		if 250<=xMouse<=550:
			#pvp
			if 260 <= yMouse <= 300:
				PlayGame()
				pvp_mode = True
				
			# boteasy
			elif 320<=yMouse<=360:
				PlayGame()
				pvaeasy_mode = True
				
			#botnormal
			elif 380<=yMouse<=420:
				PlayGame()
				pvanorml_mode = True

			#bothard
			elif 440<=yMouse<=480:
				PlayGame()
				pvahard_mode = True

			#ava
			elif 500<=yMouse<=540:
				ava_mode = True
				PlayGame()
				SimulateClick(None)
					
def HomePage():
	#Title and shadow
	screen.create_text(400,53+20,anchor="c",text="✿thello",font=("Comic Sans MS", 85, "bold"),fill="#aaa")
	screen.create_text(400,50+20,anchor="c",text="✿thello",font=("Comic Sans MS", 85, "bold"),fill="#ECEE81")
	screen.create_text(400,105+30,anchor="c",text="Developed by SPY & JAR.",font=("Comic Sans MS", 10, "bold"),fill="#FAF3F0")
	screen.create_text(400,120+30,anchor="c",text="Is a mini-project for the Programming Fundamentals subject.",font=("Comic Sans MS", 10, "bold"),fill="#FAF3F0")

	#mode
	screen.create_rectangle(350, 160+40, 462, 192+40, fill="#aaa", outline="#aaa")
	screen.create_rectangle(340, 150+40, 460, 190+40, fill="#FAF3F0", outline="#FAF3F0")
	screen.create_text(400,171.5+40,anchor="c",text="MODE",font=("Comic Sans MS", 20, "bold"),fill="#aaa")
	screen.create_text(400,170+40,anchor="c",text="MODE",font=("Comic Sans MS", 20, "bold"),fill="#FFCACC")

	#pvp
	screen.create_rectangle(260, 220+50, 552, 252+50, fill="#aaa", outline="#aaa")
	screen.create_rectangle(250, 210+50, 550, 250+50, fill="#FAF3F0", outline="#FAF3F0")
	screen.create_text(400,231+50,anchor="c",text="► Player vs Player ◄",font=("Comic Sans MS", 16, "bold"),fill="#aaa")
	screen.create_text(400,230+50,anchor="c",text="► Player vs Player ◄",font=("Comic Sans MS", 16, "bold"),fill="#FFCACC")

	#boteasy
	screen.create_rectangle(260, 280+50, 552, 312+50, fill="#aaa", outline="#aaa")
	screen.create_rectangle(250, 270+50, 550, 310+50, fill="#FAF3F0", outline="#FAF3F0")
	screen.create_text(400,291+50,anchor="c",text="► Player vs Easy AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#aaa")
	screen.create_text(400,290+50,anchor="c",text="► Player vs Easy AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#FFCACC")

	#botnormal
	screen.create_rectangle(260, 340+50, 552, 372+50, fill="#aaa", outline="#aaa")
	screen.create_rectangle(250, 330+50, 550, 370+50, fill="#FAF3F0", outline="#FAF3F0")
	screen.create_text(400,351+50,anchor="c",text="► Player vs Normal AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#aaa")
	screen.create_text(400,350+50,anchor="c",text="► Player vs Normal AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#FFCACC")

	#bothard
	screen.create_rectangle(260, 400+50, 552, 432+50, fill="#aaa", outline="#aaa")
	screen.create_rectangle(250, 390+50, 550, 430+50, fill="#FAF3F0", outline="#FAF3F0")
	screen.create_text(400,411+50,anchor="c",text="► Player vs Hard AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#aaa")
	screen.create_text(400,410+50,anchor="c",text="► Player vs Hard AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#FFCACC")

	#ava
	screen.create_rectangle(260, 460+50, 552, 492+50, fill="#aaa", outline="#aaa")
	screen.create_rectangle(250, 450+50, 550, 490+50, fill="#FAF3F0", outline="#FAF3F0")
	screen.create_text(400,471+50,anchor="c",text="► AI vs AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#aaa")
	screen.create_text(400,470+50,anchor="c",text="► AI vs AI ◄",font=("Comic Sans MS", 16, "bold"),fill="#FFCACC")

	#credit
	screen.create_text(400,585,anchor="c",text="The reference of this code is www.johnafish.ca",font=("Comic Sans MS", 10, "bold"),fill="#FAF3F0")

	screen.update()

def TimeTicking():
	global time_running,time_display,after_code
	converted = strftime("%M:%S", gmtime(time_running)) # convert seconds to hour:minute:second
	time_display.set(converted) # change time display
	time_running += 1
	after_code = root.after(1000, TimeTicking)

def StopTimer():
	global after_code
	if after_code is not None:
		root.after_cancel(after_code)
		after_code = None

def SimulateClick(event):
    x, y = 200, 200
    screen.event_generate("<Button-1>", x=x, y=y)

def Historyplay(x,y):
	global turn1,turn2
	colchar = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}
	col = x
	row = y+1
	if board.player == 0:
		screen.create_text(730,20+18*turn2,anchor="n",text=f'"{colchar[col]},{row}"',font=("Comic Sans MS", 12),fill="#A9A9A9")
	else:
		screen.create_text(610,20+18*turn1,anchor="n",text=f'"{colchar[col]},{row}"',font=("Comic Sans MS", 12),fill="#A9A9A9")
	
def PlayGame():
	global board,time_running,turn2,turn1
	
	turn1,turn2 = 1,1
	StopTimer()
	time_running = 0
	screen.delete(ALL)
	TimeTicking()
	board = 0

	#Draw the background
	DrawBackground()

	#Create the board and update it
	board = Game()
	board.won = False
	board.update()
	
#Binding, setting
screen.bind("<Button-1>", GamePlay)
screen.focus_set()

#Run forever
if __name__ == "__main__":
	HomePage()
	root.wm_title("✿thello")
	root.mainloop()