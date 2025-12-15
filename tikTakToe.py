class Grid:
    def __init__(self):
        self.row = 3
        self.columns = 3

    def gridInit(self):
        grid_structure = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        return grid_structure

class Coordinates:
    def __init__(self, choose):
        self.x = choose[0]
        self.y = choose[1]
        
    def positionSelected(self):
        self.x = int(input("X: "))
        self.y = int(input("Y: "))
        choose = [self.x - 1, self.y - 1]
        return choose

class PlayerInput(Grid):
    def __init__(self, position, logic_grid):
        super().__init__()
        self.player_x = position[0]
        self.player_y = position[1]
        self.logic_grid = logic_grid

    def playerMove(self):
        logic_grid[self.player_x][self.player_y] = 1
        return logic_grid

choose = [0, 0]
grid = Grid()
logic_grid = grid.gridInit()

position = Coordinates(choose)
position = position.positionSelected()

jugada = PlayerInput(position, logic_grid)
jugada = jugada.playerMove()
for fila in range(len(jugada)):
    for columna in range(len(jugada)):
        print(jugada[fila][columna], end="")
        if columna >= 2:
            print(" ")

#print(jugada.playerMove())
