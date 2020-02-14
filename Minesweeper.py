import os
import pygame
import random

import classes
import colors

class Game:
    def __init__(self):
        self.title = 'Minesweeper'
        self.width = 800
        self.height = 800
        self.game_screen = pygame.display.set_mode((self.width, self.height))
        self.game_screen.fill(colors.LIGHT_GRAY_COLOR)
        pygame.display.set_caption(self.title)
            
    def show_main_menu(self):
        start_button = classes.TextButton(250, 375, 300, 50, 'Start Game', 60, lambda : self.start_game())
        self.game_screen.fill(colors.ALMOST_WHITE_COLOR)
        start_button.draw(self.game_screen)
        pygame.display.update()
        self.wait_for_quit_or_click(start_button)

    def start_game(self):
        self.setup_game()
        self.run_game_loop()

        ending_text = ''
        if self.game_is_won:
            ending_text = 'You won!'
        else:
            ending_text = 'You lose!'
        self.game_screen.fill(colors.ALMOST_WHITE_COLOR)
        classes.Text(325, 300, 150, 50, ending_text, 48).draw(self.game_screen)
        quit_button = classes.TextButton(350, 375, 100, 50, 'Quit', 24, lambda : self.quit_game())
        quit_button.draw(self.game_screen)
        pygame.display.update()
        self.wait_for_quit_or_click(quit_button)

    def wait_for_quit_or_click(self, button):
        button_clicked = False

        while not button_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button.is_mouse_over(mouse_pos):
                        button_clicked = True
                        button.click()

    def setup_game(self):
        self.game_is_won = False
        self.board_game = []
        self.rows = 20
        self.columns = 20
        self.num_mines = 100
        self.num_mines_left = self.num_mines

        self.help_button = classes.TextButton(450, 50, 50, 25, 'Help', 24, lambda : self.get_help())

        self.create_board()
        self.place_mines()
        sm_board = self.calculate_surrounding_mines()
        self.board_game = self.set_surrounding_mines(self.board_game, sm_board)

        # find a blank square and reveal and expand it
        self.get_help()

        self.game_screen.fill(colors.ALMOST_WHITE_COLOR)
        self.draw_things()
        pygame.display.update()
    
    def create_board(self):
        starting_x_pos = 100
        starting_y_pos = 100
        square_width = 30
        square_height = 30
        for y in range(self.columns):
            row = []
            y_pos = starting_y_pos + (y * square_height)
            for x in range(self.rows):
                x_pos = starting_x_pos + (x * square_width)
                row.append(classes.GameBoardButton(x_pos, y_pos, square_width, square_height, 'Images/Unknown.png'))
            self.board_game.append(row)
    
    def place_mines(self):
        temp_mines_left = self.num_mines
        while temp_mines_left > 0:
            rand_row = random.randint(0, self.rows-1)
            rand_col = random.randint(0, self.columns-1)
            rand_square = self.board_game[rand_row][rand_col]
            if not rand_square.is_mine:
                rand_square.is_mine = True
                temp_mines_left -= 1
    
    def calculate_surrounding_mines(self):
        board = self.board_game
        new_board = []
        for i in range(len(board)):
            new_row = []
            for j in range(len(board[0])):
                count = 0

                if i-1 >= 0:
                    if j-1 >= 0:
                        if board[i-1][j-1].is_mine:
                            count += 1
                    if board[i-1][j].is_mine:
                        count += 1
                    if j+1 < len(board):
                        if board[i-1][j+1].is_mine:
                            count += 1
                if j-1 >= 0:
                    if board[i][j-1].is_mine:
                        count += 1
                if j+1 < len(board):
                    if board[i][j+1].is_mine:
                        count += 1
                if i+1 < len(board):
                    if j-1 >= 0:
                        if board[i+1][j-1].is_mine:
                            count += 1
                    if board[i+1][j].is_mine:
                        count += 1
                    if j+1 < len(board):
                        if board[i+1][j+1].is_mine:
                            count += 1
                
                new_row.append(count)
            new_board.append(new_row)
        return new_board
    
    def set_surrounding_mines(self, board, sm_board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j].num_of_surrounding_mines = sm_board[i][j]
        return board
    
    def draw_things(self):
        classes.Text(275, 50, 150, 25, 'Mines left: %s' % self.num_mines_left, 24).draw(self.game_screen)
        self.help_button.draw(self.game_screen)
        for row in self.board_game:
            for square in row:
                square.draw(self.game_screen)
    
    def get_help(self):
        found_blank = False

        found_blank = self.get_help_reveal_blank(found_blank)

        if not found_blank:
            self.get_help_flag_mine()

    def get_help_reveal_blank(self, found_blank):
        for row in self.board_game:
            if found_blank:
                break
            for square in row:
                if not square.is_mine and square.num_of_surrounding_mines == 0 and square.image_path == 'Images/Unknown.png':
                    found_blank = True
                    square.reveal()
                    square.expand(self.board_game)
                    break
        return found_blank
    
    def get_help_flag_mine(self):
        random_mine_num = random.randint(1, self.num_mines_left)
        found_mine = False
        for row in self.board_game:
            if found_mine:
                break
            for square in row:
                if square.is_mine and square.image_path == 'Images/Unknown.png':
                    random_mine_num -= 1
                    if random_mine_num == 0:
                        found_mine = True
                        square.is_flagged = True
                        square.image_path = 'Images/Flag.png'
                        self.num_mines_left -= 1
                        break
    
    def run_game_loop(self):
        is_game_over = False

        while not is_game_over:
            #if all mines are flagged, end the game with a win
            if self.all_mines_are_flagged():
                is_game_over = True
                self.game_is_won = True
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button = pygame.mouse.get_pressed()
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_button = None
                    if self.help_button.is_mouse_over(mouse_pos):
                        clicked_button = self.help_button
                    for i in range(len(self.board_game)):
                        if clicked_button is not None:
                            break
                        for j in range(len(self.board_game[0])):
                            square = self.board_game[i][j]
                            if square.is_mouse_over(mouse_pos):
                                clicked_button = square
                                break
                    if clicked_button is None:
                        break
                    if isinstance(clicked_button, classes.TextButton):
                        clicked_button.click()
                    elif button[0] == 1: # left click
                        clicked_button.click(self.board_game)
                        if clicked_button.image_path == 'Images/Mine.png':
                            is_game_over = True
                            break
                    elif button[2] == 1: # right click
                        if clicked_button.image_path == 'Images/Unknown.png':
                            clicked_button.is_flagged = True
                            clicked_button.image_path = 'Images/Flag.png'
                            self.num_mines_left -= 1
                            break
                        elif clicked_button.image_path == 'Images/Flag.png':
                            clicked_button.is_flagged = False
                            clicked_button.image_path = 'Images/Unknown.png'
                            self.num_mines_left += 1
                            break
                    
            self.game_screen.fill(colors.ALMOST_WHITE_COLOR)
            self.draw_things()
            pygame.display.update()
    
    def all_mines_are_flagged(self):
        for i in range(len(self.board_game)):
            for j in range(len(self.board_game[0])):
                square = self.board_game[i][j]
                if square.is_mine and not square.is_flagged:
                    return False
        return True

    def quit_game(self):
        pygame.quit()
        quit()

# set window pos on main(?) screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
pygame.init()

game = Game()
game.show_main_menu()
game.quit_game()
