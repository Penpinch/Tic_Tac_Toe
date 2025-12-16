class Grid: # Initialize the 3x3 structure.
    def __init__(self):
        self.grid = [[0 for i in range(3)] for j in range(3)]

class Coordinates:
    def __init__(self, x, y):
        self.setCoordinates(x, y)

    def setCoordinates(self, x, y):
        if not (0 <= x < 3 and 0 <= y < 3):
            raise ValueError("Invalid coordinates. Out of range.")
        self.x = x
        self.y = y
        return [self.x, self.y]

class PlayerInput(Grid):
    def __init__(self, position):
        super().__init__()
        self.player_x = position[0]
        self.player_y = position[1]

    def chosenCell(self):
        self.grid[self.player_x][self.player_y] = 1
        return self.grid

class Player: 
    def __init__(self, name, mark_type):
        self.name = name
        self.figure_type = mark_type

class Game:
    def __init__(self):
        self.grid = Grid()

    def getCoordinates(self):
        print("Where to set the token: ")
        while True:
            try:
                x = int(input("X: ")) - 1
                y = int(input("Y: ")) - 1
                position = Coordinates(x, y)
                return position
            except ValueError:
                print("Invalid coordinates.")

position = Game().getCoordinates()
position = [position.x, position.y]

jugada = PlayerInput(position)
jugada = jugada.chosenCell()
for fila in range(len(jugada)):
    for columna in range(len(jugada)):
        print(jugada[fila][columna], end="\t")
        if columna >= 2:
            print(" ")