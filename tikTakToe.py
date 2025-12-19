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

class Game:
    def __init__(self):
        self.grid = Grid()

    def playerTurn(self, player: Player): # player: Player para que detecte el .name y .mark
        print(f"{player.name} turn. ({player.mark})")
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

        winner_instance = Winner(self.grid, player)
        winner_result, player.name, player.mark = winner_instance.verifyWinner()
        if winner_result == 1:
            print(f"The winner is {self.name} ({self.mark})")
            return True
        return False

# testing
player_1 = Player("Armando", 1)
player_2 = Player("Juan", 2)
game = Game()
turn = 0

def Prueba(game: Game, turn, player_1, player_2):
    while True:
        if turn % 2 == 0:
            game.playerTurn(player_1)
        else:
            game.playerTurn(player_2)
        turn += 1

Prueba(game, turn, player_1, player_2)