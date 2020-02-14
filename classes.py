from collections import namedtuple
import pygame

import colors

class GameObject:
    def __init__(self, x, y, width, height):
        self.color = colors.ALMOST_WHITE_COLOR
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
    
    def draw(self, background):
        pygame.draw.rect(background, self.color, (self.x_pos, self.y_pos, self.width, self.height))

    def is_mouse_over(self, mouse_pos):
        if mouse_pos[0] > self.x_pos and mouse_pos[0] < self.x_pos + self.width:
            if mouse_pos[1] > self.y_pos and mouse_pos[1] < self.y_pos + self.height:
                return True
        return False

class Text(GameObject):
    def __init__(self, x, y, width, height, text, font_size):
        GameObject.__init__(self, x, y, width, height)
        self.text = text
        self.font_size = font_size
    
    def draw(self, background):
        super().draw(background)
        font = pygame.font.SysFont('comicsans', self.font_size)
        text = font.render(self.text, 1, colors.BLACK_COLOR)
        text_pos = (int(self.x_pos + (self.width/2 - text.get_width()/2)), int(self.y_pos + (self.height/2 - text.get_height()/2)))
        background.blit(text, text_pos)

class Button(GameObject):
    def __init__(self, x, y, width, height, on_click):
        GameObject.__init__(self, x, y, width, height)
        self.on_click = on_click
    
    def click(self):
        self.on_click()

class TextButton(Text, Button):
    def __init__(self, x, y, width, height, text, font_size, on_click):
        Text.__init__(self, x, y, width, height, text, font_size)
        Button.__init__(self, x, y, width, height, on_click)
        self.color = colors.LIGHT_GRAY_COLOR

class GameBoardButton(Button):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, lambda : False)
        self.image_path = image_path
        self.is_mine = False
        self.is_flagged = False
        self.num_of_surrounding_mines = 0

    def draw(self, background):
        object_image = pygame.image.load(self.image_path)
        image = pygame.transform.scale(object_image, (self.width, self.height))
        background.blit(image, (self.x_pos, self.y_pos))

    def click(self, board):
        if self.image_path == 'Images/Unknown.png':
            self.reveal()
        elif self.image_path != 'Images/Flag.png':
            self.expand(board)

    def reveal(self):
        if self.is_mine:
            self.image_path = 'Images/Mine.png'
        elif self.num_of_surrounding_mines == 0:
            self.image_path = 'Images/Blank.png'
        elif self.num_of_surrounding_mines == 1:
            self.image_path = 'Images/One.png'
        elif self.num_of_surrounding_mines == 2:
            self.image_path = 'Images/Two.png'
        elif self.num_of_surrounding_mines == 3:
            self.image_path = 'Images/Three.png'
        elif self.num_of_surrounding_mines == 4:
            self.image_path = 'Images/Four.png'
        elif self.num_of_surrounding_mines == 5:
            self.image_path = 'Images/Five.png'
        elif self.num_of_surrounding_mines == 6:
            self.image_path = 'Images/Six.png'
        elif self.num_of_surrounding_mines == 7:
            self.image_path = 'Images/Seven.png'
        elif self.num_of_surrounding_mines == 8:
            self.image_path = 'Images/Eight.png'

    def expand(self, board):
        surrounding_board = get_surrounding_board(self, board)
        can_expand = self.can_square_expand(surrounding_board)
        if can_expand:
            for i in range(len(surrounding_board)):
                for j in range(len(surrounding_board[0])):
                    if surrounding_board[i] == []:
                        continue
                    square = surrounding_board[i][j]
                    if square is not None:
                        if square.image_path == 'Images/Unknown.png':
                            square.reveal()
                            square.expand(board)

    def can_square_expand(self, surrounding_board):
        if self.num_of_surrounding_mines == 0:
            return True
        else:
            for i in range(len(surrounding_board)):
                for j in range(len(surrounding_board[0])):
                    if surrounding_board[i] == []:
                        continue
                    square = surrounding_board[i][j]
                    if square is not None:
                        if square.is_mine and not square.is_flagged:
                            return False
            return True

def get_surrounding_board(square, board):
    BoardLoc = namedtuple('BoardLoc', 'x y')
    b_loc = None
    for j in range(len(board)):
        if b_loc is not None:
            break
        for i in range(len(board[0])):
            if board[i][j] == square:
                b_loc = BoardLoc(i, j)
                break
    new_board = []
    new_row0 = [None,None,None]
    new_row1 = [None,None,None]
    new_row2 = [None,None,None]
    if b_loc.y - 1 >= 0:
        if b_loc.x - 1 >= 0:
            new_row0[0] = board[b_loc.x-1][b_loc.y-1]
        new_row0[1] = board[b_loc.x][b_loc.y-1]
        if b_loc.x + 1 < len(board):
            new_row0[2] = board[b_loc.x+1][b_loc.y-1]
    if b_loc.x - 1 >= 0:
        new_row1[0] = board[b_loc.x-1][b_loc.y]
    #new_row1[1] stays 'None' so that we don't get infinite recursion
    if b_loc.x + 1 < len(board):
        new_row1[2] = board[b_loc.x+1][b_loc.y]
    if b_loc.y + 1 < len(board):
        if b_loc.x - 1 >= 0:
            new_row2[0] = board[b_loc.x-1][b_loc.y+1]
        new_row2[1] = board[b_loc.x][b_loc.y+1]
        if b_loc.x + 1 < len(board):
            new_row2[2] = board[b_loc.x+1][b_loc.y+1]
    new_board.append(new_row0)
    new_board.append(new_row1)
    new_board.append(new_row2)
    return new_board
