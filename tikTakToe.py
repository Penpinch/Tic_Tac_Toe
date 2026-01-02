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
            return 1, self.player.name, self.player.mark
        if diagonal_2 == 3:
            return 1, self.player.name, self.player.mark

        return 0, self.player.name, self.player.mark

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

        #   X:  -3.6  →  +3.6
        #   Y:  -2.7  →  +2.7
        lines = Line3D(self.render)

        lines.addLine((-1.5, 0), (1.5, 0), (0, 0, 0, 1), z = 0) # x1
        lines.addLine((-1.5, 1.3), (1.5, 1.3), (0, 0, 0, 1), z = 0) # x2
        lines.addLine((-0.65, -0.85), (-0.65, 2.15), (0, 0, 0, 1), z = 0) # y1
        lines.addLine((0.65, -0.85), (0.65, 2.15), (0, 0, 0, 1), z = 0) # y2
        self.line_np = lines.build()

        self.grid = Grid()
        self.turn = 0
        self.player1 = Player("Luis", 1)
        self.player2 = Player("Mario", 2)
        self.current_player = self.player1

        text = CreateText(self.aspect2d)
        self.name_one = text.create_text(self.player1.name, (-0.50, 0.75), 0.07)
        self.name_two = text.create_text(self.player2.name, (0.50, 0.75), 0.07)

        self.button1 = DirectButton( # top left corner
            scale = (1.521, 0.01, 1.521), pos = (-0.405, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button1))

        self.button2 = DirectButton( #  top center
            scale = (2.3, 0.01, 1.521), pos = (0, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button2))

        self.button3 = DirectButton( # top right corner
            scale = (1.521, 0.01, 1.521), pos = (0.405, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button3))

        self.button4 = DirectButton( # left center
            scale = (1.521, 0.01, 2.3), pos = (-0.405, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button4))

        self.button5 = DirectButton( # center
            scale = (2.3, 0.01, 2.3), pos = (0, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button5))

        self.button6 = DirectButton( # right center
            scale = (1.521, 0.01, 2.3), pos = (0.405, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button6))

        self.button7 = DirectButton( # bottom left corner
            scale = (1.521, 0.01, 1.521), pos = (-0.405, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button7))

        self.button8 = DirectButton( #  bottom center
            scale = (2.3, 0.01, 1.521), pos = (0, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button8))

        self.button9 = DirectButton( # bottom right corner
            scale = (1.521, 0.01, 1.521), pos = (0.405, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.setMark(self.button9))

        self.button_to_coordinates = {
            self.button1 : (0, 0), self.button2 : (0, 1), self.button3 : (0, 2), 
            self.button4 : (1, 0), self.button5 : (1, 1), self.button6 : (1, 2), 
            self.button7 : (2, 0), self.button8 : (2, 1), self.button9 : (2, 2),
        }

    def setMark(self, button):
        try:
            btn_coords = self.button_to_coordinates[button]

            if self.grid.isFreeCell(btn_coords) == True:
                self.grid.chosenCell(btn_coords, self.current_player.mark)
            else: 
                return

            button["state"] = "disabled"
            if self.current_player.mark == 1:
                button["image"] = "o_sign.png"
            else:
                button["image"] = "x_sign.jpg"
            button["image_scale"] = 0.1
            button.show()

            self.grid.showCell()

            winner_instance = Winner(self.grid, self.current_player)
            win_result, winner_player, winner_mark = winner_instance.verifyWinner()

            if win_result == 1:
                print(f"The winner is {winner_player} ({winner_mark})")
                for btn in [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9]:
                    btn["state"] = "disabled"
                    return
            elif winner_instance.draw() == 2:
                print("Draw!")
                for btn in [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9]:
                    btn["state"] = "disabled"
                    return
            else:
                self.turn += 1
                if self.turn % 2 == 0:
                    self.current_player = self.player1
                else:
                    self.current_player = self.player2
                print(f"{self.current_player.name} turn.")
        except ValueError:
            print("Invalid coordinates.")

app = MyApp()
app.run()