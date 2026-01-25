from panda3d.core import TextNode
from panda3d.core import loadPrcFileData
from panda3d.core import LineSegs
from panda3d.core import LColor
from panda3d.core import CardMaker, TextureStage, TransparencyAttrib, Texture
from direct.gui.DirectGui import DirectButton, DirectEntry, DirectLabel, DirectFrame
from direct.showbase.ShowBase import ShowBase

loadPrcFileData("", "win-size 1000 1000")
loadPrcFileData("", "window-title Tic Tac Toe")

class Grid: # Initialize the 3x3 structure.
    def __init__(self):
        self.grid = [[0 for i in range(3)] for j in range(3)]

    def is_free_cell(self, coordinates: tuple): # Checks if a cell is already ocupped. 
        x, y = coordinates
        return (True if self.grid[x][y] == 0 else False)

    def chosen_cell(self, coordinates: tuple, mark): # Set the mark on the cell.
        x, y = coordinates
        self.grid[x][y] = mark

class Player: 
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

class Winner():
    def __init__(self, grid: Grid, player: Player):
        self.grid = grid
        self.player = player

    def draw(self): # Draw case.
        mark_counter = 0
        for i in range(len(self.grid.grid)):
            for j in range(len(self.grid.grid[i])):
                if self.grid.grid[i][j] != 0:
                    mark_counter += 1
        if mark_counter == 9:
            return 2
        return 0

    def verify_winner(self): # Check for every win case.
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

    def add_line(self, start, end, color = (1, 1, 1, 1), z = 0):
        self.line.setColor(*color)
        self.line.moveTo(start[0], z, start[1])
        self.line.drawTo(end[0], z, end[1])

    def build(self):
        return self.parent.attachNewNode(self.line.create())

class CreateText:
    def __init__(self, parent):
        self.parent = parent

    def create_text(self, content, pos, color, scale):
        text = TextNode("text node")
        text.setText(content)
        text.setAlign(TextNode.ACenter)
        nodepath = self.parent.attachNewNode(text)
        nodepath.setColor(*color)
        nodepath.setScale(scale)
        nodepath.setPos(pos[0], 0, pos[1])
        return nodepath

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera.setPos(0, 0, -10)
        self.camera.lookAt(0, 0, 0)

        card_maker = CardMaker("background_card")
        card_maker.setFrameFullscreenQuad()

        self.background = self.render2d.attachNewNode(card_maker.generate())

        texture_ = self.loader.loadTexture("purple_galaxy.png")
        self.background.setTexture(texture_)
        self.background.setTransparency(TransparencyAttrib.M_alpha)

        self.background.setBin("background", 0)
        self.background.setDepthTest(False)
        self.background.setDepthWrite(False)

        lines = Line3D(self.aspect2d) # NodePath for lines.
        lines.add_line((-0.555, -0.484), (0.555, -0.484), (0, 0, 0, 1), z = 0) # x up 
        lines.add_line((0.555, 0), (-0.555, 0), (0, 0, 0, 1), z = 0)           # x down
        lines.add_line((-0.240, 0.312), (-0.240, -0.798), (0, 0, 0, 1), z = 0) # y left
        lines.add_line((0.240, 0.312), (0.240, -0.792), (0, 0, 0, 1), z = 0)   # y right
        self.line_node_path = lines.build()
        self.line_node_path.hide()

        self.bg_sqd_container = self.aspect2d.attachNewNode("frames")
        self.background_button_frame()
        self.bg_sqd_container.hide()

        self.buttons_container = self.aspect2d.attachNewNode("Grid") # NodePath for buttons.

        self.button1 = DirectButton( # top left corner
            scale = (1.521, 0.01, 1.521), pos = (-0.405, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button1), parent = self.buttons_container)

        self.button2 = DirectButton( #  top center
            scale = (2.3, 0.01, 1.521), pos = (0, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button2), parent = self.buttons_container)

        self.button3 = DirectButton( # top right corner
            scale = (1.521, 0.01, 1.521), pos = (0.405, 0, 0.163), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button3), parent = self.buttons_container)

        self.button4 = DirectButton( # left center
            scale = (1.521, 0.01, 2.3), pos = (-0.405, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button4), parent = self.buttons_container)

        self.button5 = DirectButton( # center
            scale = (2.3, 0.01, 2.3), pos = (0, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button5), parent = self.buttons_container)

        self.button6 = DirectButton( # right center
            scale = (1.521, 0.01, 2.3), pos = (0.405, 0, -0.245), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button6), parent = self.buttons_container)

        self.button7 = DirectButton( # bottom left corner
            scale = (1.521, 0.01, 1.521), pos = (-0.405, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button7), parent = self.buttons_container)

        self.button8 = DirectButton( #  bottom center
            scale = (2.3, 0.01, 1.521), pos = (0, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button8), parent = self.buttons_container)

        self.button9 = DirectButton( # bottom right corner
            scale = (1.521, 0.01, 1.521), pos = (0.405, 0, -0.65), frameColor = (0, 0, 0, 0), 
            command = lambda: self.set_mark(self.button9), parent = self.buttons_container)

        self.buttons_container.hide()

        self.button_to_coordinates = {
            self.button1 : (0, 0), self.button2 : (0, 1), self.button3 : (0, 2), 
            self.button4 : (1, 0), self.button5 : (1, 1), self.button6 : (1, 2), 
            self.button7 : (2, 0), self.button8 : (2, 1), self.button9 : (2, 2),
        }

        self.loading_menu()

    def set_mark(self, button):
        try:
            btn_coords = self.button_to_coordinates[button]

            if self.grid.is_free_cell(btn_coords) == True:
                self.grid.chosen_cell(btn_coords, self.current_player.mark)
            else: 
                return

            button["state"] = "disabled"
            if self.current_player.mark == 1:
                button["image"] = "o_sign.png"
            else:
                button["image"] = "x_sign.png"
            button["image_scale"] = 0.1
            button.setTransparency(TransparencyAttrib.M_alpha)
            button.show()

            winner_instance = Winner(self.grid, self.current_player)
            win_result, winner_player, winner_mark = winner_instance.verify_winner()

            if win_result == 1:
                self.end_game_screen(winner_player)
                self.disable_all_buttons()
                self.review_button = DirectButton(
                text = "Review", pos = (0, 0, -0.6), frameColor = (1, 0.992, 0.816, 0.5), scale = 0.09, 
                command = lambda: (self.review_match(win_result), self.return_to_menu.destroy(), 
                                    self.end_text.removeNode(), self.review_button.destroy())
                )
                return
            elif winner_instance.draw() == 2:
                self.end_game_screen("draw")
                self.disable_all_buttons()
                self.review_button = DirectButton(
                text = "Review", pos = (0, 0, -0.6), frameColor = (1, 0.992, 0.816, 0.5), scale = 0.09, 
                command = lambda: (self.review_match("draw"), self.return_to_menu.destroy(), 
                                    self.end_text.removeNode(), self.review_button.destroy())
                )
                return
            else:
                self.turn += 1
                if self.turn % 2 == 0:
                    self.label_p2.hide(); self.name_two.show()
                    self.label_p1.show(); self.name_one.hide()
                    self.current_player = self.player1
                else:
                    self.label_p1.hide(); self.name_one.show()
                    self.label_p2.show(); self.name_two.hide()
                    self.current_player = self.player2
        except ValueError:
            print("Invalid coordinates.")

    def loading_menu(self):
        game_tittle_node = CreateText(self.aspect2d)
        self.game_tittle = game_tittle_node.create_text("Tic Tac Toe", (0, 0.7), (0, 0, 0, 1), 0.2)
        self.game_mode_1_button = DirectButton(
            text = "Two players", pos = (0, 0, 0.3), frameColor = (1, 0.992, 0.816, 0.5), scale = 0.09, 
            command = lambda: (self.game_tittle.removeNode(), self.game_mode_1_button.destroy(), 
                                self.exit_game_button.destroy(), self.start_game_screen()))

        self.exit_game_button = DirectButton(
            text = "Salir ", pos = (0, 0, 0), frameColor = (1, 0.992, 0.816, 0.5), scale = 0.09, 
            command = lambda: (self.userExit()))

    def start_game_screen(self):
        self.player1 = Player("", 1)
        self.player2 = Player("", 2)
        self.current_player = self.player1
        self.names_done = 0

        for btn in self.button_to_coordinates.keys():
            btn["image"] = None

        self.text_entry1 = DirectEntry(
            initialText = "Player one", scale = 0.05, pos = (-0.60, 0, 0.85), numLines = 1, focus = 0, 
            focusInCommand = self.clear_placeholder1, command = self.set_player_1
            )

        self.text_entry2 = DirectEntry(
            initialText = "Player two", scale = 0.05, pos = (0.15, 0, 0.85), numLines = 1, focus = 0, 
            focusInCommand = self.clear_placeholder2, command = self.set_player_2
        )

        self.grid = Grid()
        self.turn = 0

        self.enable_all_buttons()

        text = CreateText(self.aspect2d) # NodePath
        self.name_one = text.create_text(self.player1.name, (-0.50, 0.75), (0, 0, 0, 1), 0.07)
        self.name_two = text.create_text(self.player2.name, (0.50, 0.75), (0, 0, 0, 1), 0.07)

        self.label_p1 = self.create_name_label(self.player1.name, (-0.50, 0.75))
        self.label_p2 = self.create_name_label(self.player2.name, (0.50, 0.75))
        self.label_p1.hide(); self.label_p2.hide()

    def end_game_screen(self, text):
        self.buttons_container.hide()
        self.name_one.hide()
        self.name_two.hide()
        self.label_p1.hide()
        self.label_p2.hide()
        self.line_node_path.hide()
        self.bg_sqd_container.hide()

        end_text_node = CreateText(self.aspect2d) # NodePath
        if text == "draw":
            self.end_text = end_text_node.create_text("Draw!!!", (0, 0), (1, 0, 0, 1), 0.1)
        else:
            end_text = "The winner is {}!!!".format(text)
            self.end_text = end_text_node.create_text(end_text, (0,0), (1, 0, 0, 1), 0.1)

        self.return_to_menu = DirectButton(
            text = "Menu", pos = (0, 0, -0.8), frameColor = (1, 0.992, 0.816, 0.5), scale = 0.09, 
            command = lambda: (self.end_text.removeNode(), self.review_button.destroy(), 
                                self.return_to_menu.destroy(), self.loading_menu()))

    def review_match(self, text):
        self.buttons_container.show()
        self.name_one.show()
        self.name_two.show()
        self.label_p1.hide()
        self.label_p2.hide()
        self.line_node_path.show()
        self.bg_sqd_container.show()

        self.end_review_button = DirectButton(
            text = "End review", pos = (0, 0, -0.9), frameColor = (1, 0.992, 0.816, 0.5), scale = 0.09, 
            command = lambda: (self.end_text.removeNode(), self.end_review_button.destroy(), self.end_game_screen(text)))

    def clear_placeholder1(self):
        if self.text_entry1.get() == "Player one":
            self.text_entry1.enterText("")

    def clear_placeholder2(self):
        if self.text_entry2.get() == "Player two":
            self.text_entry2.enterText("")

    def disable_all_buttons(self):
        for btn in self.button_to_coordinates.keys():
            btn["state"] = "disabled"

    def enable_all_buttons(self):
        for btn in self.button_to_coordinates.keys():
            btn["state"] = "normal"

    def set_player_1(self, text):
        if text.strip() == "":
            text = "Player one"
        self.player1 = Player(text, 1)
        self.label_p1["text"] = text
        bounds_p1 = self.label_p1.getBounds()
        left_p1, right_p1, bottom_p1, top_p1 = bounds_p1
        padding = 0.1
        self.label_p1["frameSize"] = (
            left_p1 - padding, right_p1 + padding, 
            bottom_p1 - padding, top_p1 + padding
        )
        self.current_player = self.player1
        self.text_entry1.destroy()
        self.name_one.node().setText(text)
        self.names_done += 1
        self.show_board()

    def set_player_2(self, text):
        if text.strip() == "":
            text = "Player two"
        self.player2 = Player(text, 2)
        self.label_p2["text"] = text
        bounds_p2 = self.label_p2.getBounds()
        left_p2, right_p2, bottom_p2, top_p2 = bounds_p2
        padding = 0.1
        self.label_p2["frameSize"] = (
            left_p2 - padding, right_p2 + padding, 
            bottom_p2 - padding, top_p2 + padding
        )
        self.text_entry2.destroy()
        self.name_two.node().setText(text)
        self.names_done += 1
        self.show_board()

    def show_board(self):
        if self.names_done == 2:
            self.bg_sqd_container.show()
            self.line_node_path.show()
            self.buttons_container.show()
            self.label_p1.show()

    def create_name_label(self, text, pos):
        display_text = text[:15]
        return DirectLabel(
        text = display_text, text_align = TextNode.ACenter, pos = (pos[0], 0, pos[1]), 
        frameColor = (1, 0, 0, 1), frameSize = None, scale = 0.07
        )

    def background_button_frame(self):
        self.bg_sqd_1 = DirectFrame(
            frameSize = (-0.15, 0.15, -0.15, 0.15), frameColor = (1, 1, 1, 0.3), 
            pos = (-0.405, 0, 0.163), parent = self.bg_sqd_container)

        self.bg_sqd_2 = DirectFrame(
            frameSize = (-0.23, 0.23, -0.15, 0.15), frameColor = (1, 1, 1, 0.3), 
            pos = (0, 0, 0.163), parent = self.bg_sqd_container)

        self.bg_sqd_3 = DirectFrame(
            frameSize = (-0.15, 0.15, -0.15, 0.15), frameColor = (1, 1, 1, 0.3), 
            pos = (0.405, 0, 0.163), parent = self.bg_sqd_container)

        self.bg_sqd_4 = DirectFrame(
            frameSize = (-0.15, 0.15, -0.23, 0.23), frameColor = (1, 1, 1, 0.3), 
            pos = (-0.405, 0, -0.245), parent = self.bg_sqd_container)

        self.bg_sqd_5 = DirectFrame(
            frameSize = (-0.23, 0.23, -0.23, 0.23), frameColor = (1, 1, 1, 0.3), 
            pos = (0, 0, -0.245), parent = self.bg_sqd_container)

        self.bg_sqd_6 = DirectFrame(
            frameSize = (-0.15, 0.15, -0.23, 0.23), frameColor = (1, 1, 1, 0.3), 
            pos = (0.405, 0, -0.245), parent = self.bg_sqd_container)

        self.bg_sqd_7 = DirectFrame(
            frameSize = (-0.15, 0.15, -0.15, 0.15), frameColor = (1, 1, 1, 0.3), 
            pos = (-0.405, 0, -0.65), parent = self.bg_sqd_container)

        self.bg_sqd_8 = DirectFrame(
            frameSize = (-0.23, 0.23, -0.15, 0.15), frameColor = (1, 1, 1, 0.3), 
            pos = (0, 0, -0.65), parent = self.bg_sqd_container)

        self.bg_sqd_9 = DirectFrame(
            frameSize = (-0.15, 0.15, -0.15, 0.15), frameColor = (1, 1, 1, 0.3), 
            pos = (0.405, 0, -0.65), parent = self.bg_sqd_container)

game = Game()
game.run()