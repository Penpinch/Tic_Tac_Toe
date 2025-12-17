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
        x = int(input("X: ")) - 1
        y = int(input("Y: ")) - 1
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

class Game:
    def __init__(self):
        self.grid = Grid()

    def playerTurn(self, player: Player): # player: Player para que detecte el .name y .mark
        print(f"{player.name} turn.")
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

# testing
player_1 = Player("Armando", 1)
player_2 = Player("Juan", 2)

game = Game()

game.playerTurn(player_1)
game.playerTurn(player_2)