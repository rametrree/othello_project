### Header Comment
The header comment contains metadata about the project and the developers:

```python
"""
The reference of this code is www.johnafish.ca

Developed by
Ramet Saelee 6601012620054
Singhanat Pothongkham 6601012610172

Is a mini-project for the Programming Fundamentals subject.
"""
```

### Library Imports
Various libraries are imported for different functionalities:

```python
from tkinter import *
from tkinter import messagebox
from math import *
from time import *
from random import *
from copy import deepcopy
```

- `tkinter` is used for creating the GUI.
- `math`, `time`, `random`, and `deepcopy` are standard Python libraries used for mathematical operations, time-related functions, random number generation, and deep copying objects, respectively.

### Global Variables
The mode variables and some Tkinter setup variables are defined:

```python
pvp_mode = False
pvaeasy_mode = False
pvanorml_mode = False
pvahard_mode = False
ava_mode = False

root = Tk()
root.resizable(False,False)
screen = Canvas(root, width=800, height=625, background="#8DDFCB",highlightthickness=0)
screen.pack()

time_running = 0
time_display = StringVar(value="00:00")
after_code = None

turn1 = 1
turn2 = 1
```

### The Game Class
The `Game` class encapsulates all the functionality related to the game logic and rendering:

#### Initialization
The constructor initializes the game board, player, and other attributes:

```python
class Game:
    def __init__(self):
        self.player = 0
        self.passed = False
        self.won = False

        self.array = []
        for x in range(8):
            self.array.append([])
            for y in range(8):
                self.array[x].append(None)

        self.array[3][3] = "w"
        self.array[3][4] = "b"
        self.array[4][3] = "b"
        self.array[4][4] = "w"

        self.oldarray = self.array
```

#### Update Method
The `update` method refreshes the graphical representation of the game board:

```python
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
        ...
```

#### Board Move
Handles the logic for making a move:

```python
    def boardMove(self, x, y):
        self.oldarray = self.array
        if self.player == 0:
            self.oldarray[x][y] = "w"
        else:
            self.oldarray[x][y] = "b"
        self.array = MoveArray(self.array, x, y)

        self.player = 1 - self.player
        self.passTest()
        self.update()
```

#### Pass Test
Checks if the current player must pass their turn:

```python
    def passTest(self):
        mustPass = True
        for x in range(8):
            for y in range(8):
                if ValidMove(self.array, self.player, x, y):
                    mustPass = False

        if mustPass:
            self.won = True
        else:
            self.passed = False
```

#### Draw Scoreboard
Draws the scoreboard on the screen:

```python
    def drawScoreBoard(self):
        screen.delete("score")

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

        screen.create_text(130, 545, fill=self.player1_colour, font=("Comic Sans MS", 25, "bold"), text="✿")
        screen.create_text(370, 545, fill=self.player2_colour, font=("Comic Sans MS", 25, "bold"), text="✿")

        screen.create_text(65, 500, anchor="c", tags="score", font=("Comic Sans MS", 15, "bold"), fill="#FAF3F0", text="Player 1")
        screen.create_text(435, 500, anchor="c", tags="score", font=("Comic Sans MS", 15, "bold"), fill="#FAF3F0", text="Player 2")
        screen.create_rectangle(30, 520, 100, 580, fill="#FAF3F0", outline="#FAF3F0")
        screen.create_text(65, 550, anchor="c", tags="score", font=("Comic Sans MS", 45, "bold"), fill="#FFCACC", text=self.player1_score)
        screen.create_rectangle(400, 520, 470, 580, fill="#FAF3F0", outline="#FAF3F0")
        screen.create_text(435, 550, anchor="c", tags="score", font=("Comic Sans MS", 45, "bold"), fill="#DBC4F0", text=self.player2_score)

        return self.player1_score, self.player2_score
```

### AI Methods
Methods to handle AI moves for different difficulty levels:

```python
    def easyAI(self):
        choices = []
        for x in range(8):
            for y in range(8):
                if ValidMove(self.array, self.player, x, y):
                    choices.append([x, y])
        if choices:
            movechoices = choice(choices)
            self.boardMove(movechoices[0], movechoices[1])
            Historyplay(movechoices[0], movechoices[1])

    def normalAI(self):
        boards = []
        choices = []
        for x in range(8):
            for y in range(8):
                if ValidMove(self.array, self.player, x, y):
                    test = MoveArray(self.array, x, y)
                    boards.append(test)
                    choices.append([x, y])

        bestScore = -float("inf")
        bestIndex = 0
        for i in range(len(boards)):
            score = self.ScoreNormalTest(boards[i], self.player)
            if score > bestScore:
                bestIndex = i
                bestScore = score

        if choices:
            self.boardMove(choices[bestIndex][0], choices[bestIndex][1])
            Historyplay(choices[bestIndex][0], choices[bestIndex][1])

    def hardAI(self):
        boards = []
        choices = []
        for x in range(8):
            for y in range(8):
                if ValidMove(self.array, self.player, x, y):
                    test = MoveArray(self.array, x, y)
                    boards.append(test)
                    choices.append([x, y])

        bestScore = -float("inf")
        bestIndex = 0
        for i in range(len(boards)):
            score = self.ScoreHardTest(boards[i], self.player)
            if score > bestScore:
                bestIndex = i
                bestScore = score
        if choices:
            self.boardMove(choices[bestIndex][0], choices[bestIndex][1])
            Historyplay(choices[bestIndex][0], choices[bestIndex][1])

    def ScoreNormalTest(self, array, player):
        score = 0
        if player == 1:
            colour = "b"
            opponent = "w"
        else:
            colour = "w"
            opponent = "b"
        for x in range(8):
            for y in range(8):
                if array[x][y] == colour:
                    score += 1
                elif array[x][y] == opponent:
                    score -= 1
        return score

    def ScoreHardTest(self, array, player):
        score = 0
        if player == 1:
            colour =

 "b"
            opponent = "w"
        else:
            colour = "w"
            opponent = "b"

        score += array[0].count(colour) * 5
        score += array[7].count(colour) * 5
        score += array[0][0] == colour and 15 or 0
        score += array[0][7] == colour and 15 or 0
        score += array[7][0] == colour and 15 or 0
        score += array[7][7] == colour and 15 or 0

        for x in range(8):
            for y in range(8):
                if array[x][y] == colour:
                    score += 1
                elif array[x][y] == opponent:
                    score -= 1
        return score
```

### Main Loop
The main game loop which calls update functions and checks for game status:

```python
    def mainLoop(self):
        self.update()
        self.drawScoreBoard()
        if pvp_mode:
            root.after(100, self.mainLoop)
        elif pvaeasy_mode:
            if self.player == 1:
                self.easyAI()
            root.after(100, self.mainLoop)
        elif pvanorml_mode:
            if self.player == 1:
                self.normalAI()
            root.after(100, self.mainLoop)
        elif pvahard_mode:
            if self.player == 1:
                self.hardAI()
            root.after(100, self.mainLoop)
        elif ava_mode:
            if self.player == 0:
                self.hardAI()
            else:
                self.normalAI()
            root.after(100, self.mainLoop)
```

### Helper Functions
Various helper functions such as `ValidMove`, `MoveArray`, `Historyplay`, and others are defined to assist in game logic and state management.

### Main Execution
Finally, the main game instance is created, and the main loop is started:

```python
game = Game()
game.mainLoop()
root.mainloop()
```

This concludes the breakdown of the code. The code primarily focuses on setting up the game, handling the user interface, managing game state, and implementing different AI difficulty levels for the game Othello.
