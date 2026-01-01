from panda3d.core import TextNode
from panda3d.core import loadPrcFileData
from panda3d.core import LineSegs
from direct.gui.DirectGui import DirectButton
from direct.gui import DirectGuiGlobals
from direct.showbase.ShowBase import ShowBase

loadPrcFileData("", "win-size 1000 1000")
loadPrcFileData("", "window-title Tic Tac Toe")

class Grid: # Initialize the 3x3 structure.
    def __init__(self):
        self.grid = [[0 for i in range(3)] for j in range(3)]

    def isFreeCell(self, coordinates: tuple): 
        x, y = coordinates
        return (True if self.grid[x][y] == 0 else False)

    def chosenCell(self, coordinates: tuple, mark):
        x, y = coordinates
        self.grid[x][y] = mark

    def showCell(self):
        for fila in range(3):
            for columna in range(3):
                print(self.grid[fila][columna], end="\t")
                if columna >= 2:
                    print(" ")

class InputCoordinates:
    @staticmethod
    def getCoordinates():
        x = int(input("X(1-3): ")) - 1
        y = int(input("Y(1-3): ")) - 1
        return  x, y

class Coordinates: # setter para el control del ValueError
    def __init__(self, value: tuple):
        self.x = 0
        self.y = 0
        self.coordinates = value #Automatically calls the setter.

    @property
    def coordinates(self):
        return self.x, self.y

    @coordinates.setter
    def coordinates(self, value):
        x, y = value
        if not (0 <= x < 3 and 0 <= y < 3):
            raise ValueError("Invalid coordinates. Out of range.")
        self.x = x
        self.y = y

class Player: 
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

class Winner():
    def __init__(self, grid: Grid, player: Player):
        self.grid = grid
        self.player = player

    def draw(self):
        mark_counter = 0
        for i in range(len(self.grid.grid)):
            for j in range(len(self.grid.grid[i])):
                if self.grid.grid[i][j] != 0:
                    mark_counter += 1
        if mark_counter == 9:
            return 2
        return 0

    def verifyWinner(self):
        mark_counter = 0

        for a in range(len(self.grid.grid)):
            for b in range(len(self.grid.grid[a])):
                if self.grid.grid[a][b] == self.player.mark:
                    mark_counter += 1
            if mark_counter == 3:
                return 1, self.player.name, self.player.mark
            mark_counter = 0

        for c in range(len(self.grid.grid[0])):
            mark_counter = 0
            for d in range(len(self.grid.grid)):
                if self.grid.grid[d][c] == self.player.mark:
                    mark_counter += 1
            if mark_counter == 3:
                return 1, self.player.name, self.player.mark
            mark_counter = 0

        diagonal_1 = 0; diagonal_2 = 0
        for e in range(len(self.grid.grid)):
            if self.grid.grid[e][e] == self.player.mark:
                diagonal_1 += 1
            if self.grid.grid[e][len(self.grid.grid) - 1 - e] == self.player.mark:
                diagonal_2 += 1
        if diagonal_1 == 3:
            return self.player.name, self.player.mark
        if diagonal_2 == 3:
            return 1, self.player.name, self.player.mark

        return 0, self.player.name, self.player.mark

class Game:
    def __init__(self):
        self.grid = Grid()

    def playerTurn(self, player: Player): # player: Player para que detecte el .name y .mark
        print(f"{player.name} turn. ({player.mark})")
        winner_instance = Winner(self.grid, player)
        draw_result = winner_instance.draw()
        if draw_result == 2:
            print("Draw!")
            return False
        while True:
            try:
                coord = InputCoordinates()
                coord = coord.getCoordinates()
                coords = Coordinates(coord)
                coords = coords.coordinates

                if self.grid.isFreeCell(coords) == True:
                    self.grid.chosenCell(coords, player.mark)
                    break
                else:
                    print("Already occuped.")
            except ValueError:
                print("Invalid coordinates. ")

        self.grid.showCell()

        winner_result, player.name, player.mark = winner_instance.verifyWinner()
        if winner_result == 1:
            print(f"The winner is {player.name} ({player.mark})")
            return False
        return True

# testing
"""player_1 = Player("Armando", 1)
player_2 = Player("Juan", 2)
game = Game()
turn = 0"""

"""def Prueba(game: Game, turn, player_1, player_2):
    game_can_continue = True

    while game_can_continue == True:
        if turn % 2 == 0:
            game_can_continue = game.playerTurn(player_1)
        else:
            game_can_continue = game.playerTurn(player_2)
        turn += 1

Prueba(game, turn, player_1, player_2)"""

class Line3D:
    def __init__(self, parent):
        self.line = LineSegs()
        self.line.setThickness(12)
        self.parent = parent

    def addLine(self, start, end, color = (1, 1, 1, 1), z = 0):
        self.line.setColor(*color)
        self.line.moveTo(start[0], start[1], z)
        self.line.drawTo(end[0], end[1], z)

    def build(self):
        return self.parent.attachNewNode(self.line.create())

class CreateText:
    def __init__(self, parent):
        self.parent = parent

    def create_text(self, content, pos, scale = 0.07):
        text = TextNode("text node")
        text.setText(content)
        np = self.parent.attachNewNode(text)
        np.setScale(scale)
        np.setPos(pos[0], 0, pos[1])
        return np

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera.setPos(0, 0, -10)
        self.camera.lookAt(0, 0, 0)

        """ X:  -3.6  →  +3.6
            Y:  -2.7  →  +2.7"""
        lines = Line3D(self.render)

        lines.addLine((-1.5, 0), (1.5, 0), (0, 0, 0, 1), z = 0) # x1
        lines.addLine((-1.5, 1.3), (1.5, 1.3), (0, 0, 0, 1), z = 0) # x2
        lines.addLine((-0.65, -0.85), (-0.65, 2.15), (0, 0, 0, 1), z = 0) # y1
        lines.addLine((0.65, -0.85), (0.65, 2.15), (0, 0, 0, 1), z = 0) # y2
        self.line_np = lines.build()

        self.game = Game()
        self.player1 = Player("Luis", 1)
        self.player2 = Player("Mario", 2)

        text = CreateText(self.aspect2d)
        self.name_one = text.create_text(self.player1.name, (-0.50, 0.75), 0.07)
        self.name_two = text.create_text(self.player2.name, (0.50, 0.75), 0.07)

        self.button1 = DirectButton( # top left corner
            scale = (1.521, 0.01, 1.521), pos = (-0.405, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button1))

        self.button2 = DirectButton( # bottom left corner
            scale = (1.521, 0.01, 1.521), pos = (-0.405, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button2))

        self.button3 = DirectButton( # top right corner
            scale = (1.521, 0.01, 1.521), pos = (0.405, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button3))

        self.button4 = DirectButton( # bottom right corner
            scale = (1.521, 0.01, 1.521), pos = (0.405, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button4))

        self.button5 = DirectButton( #  top corner
            scale = (2.3, 0.01, 1.521), pos = (0, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button5))
        
        self.button6 = DirectButton( #  bottom corner
            scale = (2.3, 0.01, 1.521), pos = (0, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button6))
        
        self.button7 = DirectButton( # left corner
            scale = (1.521, 0.01, 2.3), pos = (-0.405, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button7))
        
        self.button8 = DirectButton( # right corner
            scale = (1.521, 0.01, 2.3), pos = (0.405, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button8))
        
        self.button9 = DirectButton( # right corner
            scale = (2.3, 0.01, 2.3), pos = (0, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.deactivateButton(self.button9))
        
        """self.button1 = DirectCheckButton( # top left corner
            scale = (0.3, 0.01, 0.26), pos = (-0.28, 0, 0.17), 
            command = lambda: self.deactivateButton(self.button1))

        self.button2 = DirectCheckButton( # bottom left corner
            scale = (0.3, 0.01, 0.26), pos = (-0.28, 0, -0.66), 
            command = lambda: self.deactivateButton(self.button2))

        self.button3 = DirectCheckButton( # top right corner
            scale = (0.3, 0.01, 0.26), pos = (0.54, 0, 0.17), 
            command = lambda: self.deactivateButton(self.button3))

        self.button4 = DirectCheckButton( # bottom right corner 
            scale = (0.3, 0.01, 0.26), pos = (0.54, 0, -0.66), 
            command = lambda: self.deactivateButton(self.button4))

        self.button5 = DirectCheckButton( # top center 
            scale = (0.44, 0.01, 0.26), pos = (0.19, 0, 0.17), 
            command = lambda: self.deactivateButton(self.button5))

        self.button6 = DirectCheckButton( # bottom center
            scale = (0.44, 0.01, 0.26), pos = (0.19, 0, -0.66), 
            command = lambda: self.deactivateButton(self.button6))

        self.button7 = DirectCheckButton( # left center 
            scale = (0.3, 0.01, 0.38), pos = (-0.28, 0, -0.24), 
            command = lambda: self.deactivateButton(self.button7))

        self.button8 = DirectCheckButton( # right center
            scale = (0.3, 0.01, 0.38), pos = (0.54, 0, -0.24), 
            command = lambda: self.deactivateButton(self.button8))

        self.button9 = DirectCheckButton( # center
            scale = (0.44, 0.01, 0.38), pos = (0.19, 0, -0.24), 
            command = lambda: self.deactivateButton(self.button9))"""

        self.buttons = [
            self.button1, self.button2, self.button3, 
            self.button4, self.button5, self.button6, 
            self.button7, self.button8, self.button9]
        
        """for btn in self.buttons:
            btn.hide()"""


        #self.taskMgr.add(self.gameLoop, "GameLoop")

    def deactivateButton(self, button):
        for btn in self.buttons:
            if btn == button:
                # --- DirectButton text states = (text, text_pressed, text_rollover, text_disabled) ---
                button["state"] = "disabled"
                button.show()

                button["text"] = 'A'
                button["text_scale"] = 0.1
                button["text_align"] = TextNode.ACenter
                button["text_pos"] = (0, 0)
                button["text_fg"] = (1, 0, 0, 1)
                button["text_shadow"] = (0, 0, 0, 1)
                button["relief"] = DirectGuiGlobals.FLAT #DGG.RAISED, DGG.SUNKEN

    def gameLoop(self, task):
        game_can_continue = True
        turn = 0
        while game_can_continue == True:
            if turn % 2 == 0:
                game_can_continue = self.game.playerTurn(self.player1)
            else:
                game_can_continue = self.game.playerTurn(self.player2)
            turn += 1

app = MyApp()
app.run()