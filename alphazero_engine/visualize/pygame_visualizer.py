from bitboard.bitboard import *
from bitboard.pieces import *
import pygame
import time

class PygameVisualizer:

    def __init__(self):

        self.first_visualize = True

    def full_init(self):
        self.pygame_instance = pygame
        self.pygame_instance.init()
        self.mixer_instance = pygame.mixer
        self.mixer_instance.init()
        


        self.width, self.height = 800, 800
        self.cell_width = self.width / 8
        self.cell_height = self.height / 8
        self.window = self.pygame_instance.display.set_mode((self.width, self.height))
        self.pygame_instance.display.set_caption("Chess")

        #load images
        self.white_pawn = pygame.image.load("visualize/piece_images/white_pawn.png").convert_alpha()
        self.white_pawn = pygame.transform.scale(self.white_pawn, (100, 100))
        self.white_knight = pygame.image.load("visualize/piece_images/white_knight.png").convert_alpha()
        self.white_knight = pygame.transform.scale(self.white_knight, (100, 100))

        self.white_bishop = pygame.image.load("visualize/piece_images/white_bishop.png").convert_alpha()
        self.white_bishop = pygame.transform.scale(self.white_bishop, (100, 100))
        self.white_rook = pygame.image.load("visualize/piece_images/white_rook.png").convert_alpha()
        self.white_rook = pygame.transform.scale(self.white_rook, (100, 100))
        
        self.white_queen = pygame.image.load("visualize/piece_images/white_queen.png").convert_alpha()
        self.white_queen = pygame.transform.scale(self.white_queen, (100, 100))
        self.white_king = pygame.image.load("visualize/piece_images/white_king.png").convert_alpha()
        self.white_king = pygame.transform.scale(self.white_king, (100, 100))

        #break

        self.black_pawn = pygame.image.load("visualize/piece_images/black_pawn.png").convert_alpha()
        self.black_pawn = pygame.transform.scale(self.black_pawn, (100, 100))
        self.black_knight = pygame.image.load("visualize/piece_images/black_knight.png").convert_alpha()
        self.black_knight = pygame.transform.scale(self.black_knight, (100, 100))

        self.black_bishop = pygame.image.load("visualize/piece_images/black_bishop.png").convert_alpha()
        self.black_bishop = pygame.transform.scale(self.black_bishop, (100, 100))
        self.black_rook = pygame.image.load("visualize/piece_images/black_rook.png").convert_alpha()
        self.black_rook = pygame.transform.scale(self.black_rook, (100, 100))
        
        self.black_queen = pygame.image.load("visualize/piece_images/black_queen.png").convert_alpha()
        self.black_queen = pygame.transform.scale(self.black_queen, (100, 100))
        self.black_king = pygame.image.load("visualize/piece_images/black_king.png").convert_alpha()
        self.black_king = pygame.transform.scale(self.black_king, (100, 100))

        self.white_piece_map = {
            WHITE_PAWN : self.white_pawn,
            WHITE_KNIGHT : self.white_knight,
            WHITE_BISHOP : self.white_bishop,
            WHITE_ROOK : self.white_rook,
            WHITE_QUEEN : self.white_queen,
            WHITE_KING : self.white_king
        }

        self.black_piece_map = {
            BLACK_PAWN : self.black_pawn,
            BLACK_KNIGHT : self.black_knight,
            BLACK_BISHOP : self.black_bishop,
            BLACK_ROOK : self.black_rook,
            BLACK_QUEEN : self.black_queen,
            BLACK_KING : self.black_king
        }

        self.move_sound =  self.mixer_instance.Sound("visualize/sounds/move.mp3")
        self.capture_sound =  self.mixer_instance.Sound("visualize/sounds/capture.mp3")
        self.castle_sound = self.mixer_instance.Sound("visualize/sounds/castle.mp3")

        self.WHITE = (195, 195, 195)
        self.BLACK = (100, 30, 10)
        self.RED = (255, 188, 181)
        self.GREEN = (185, 202, 136)
        self.PURPLE = (186,85,211)

        # Draw once
        self.window.fill((255, 255, 255))  # Fill background with white

        self.draw_background()
        self.pygame_instance.display.update()
        self.pygame_instance.display.set_caption("Chess")

    def draw_background(self, old_index=-1, new_index=-1, make_move=False):

        for i in range(8):
            for j in range(8):

                ind = 63 - ((j * 8) + i)

                if ind == old_index:
                    self.pygame_instance.draw.rect(self.window, self.PURPLE, (i*self.cell_width, j*self.cell_height, self.cell_width, self.cell_height))  

                elif ind == new_index:
                    self.pygame_instance.draw.rect(self.window, self.PURPLE, (i*self.cell_width, j*self.cell_height, self.cell_width, self.cell_height))

                elif (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):

                    self.pygame_instance.draw.rect(self.window, self.WHITE, (i*self.cell_width, j*self.cell_height, self.cell_width, self.cell_height)) 

                else:

                    if make_move:

                        self.pygame_instance.draw.rect(self.window, self.GREEN, (i*self.cell_width, j*self.cell_height, self.cell_width, self.cell_height)) 
                    else:

                        self.pygame_instance.draw.rect(self.window, self.BLACK, (i*self.cell_width, j*self.cell_height, self.cell_width, self.cell_height)) 



    def get_mouse_mouse(self, valid_moves, Left_Shift_to_Movement_type, state):

        # Default initialization
        action = -1
        attempted_from_square = -1

        # Loop until we make a valid move with our mouse...
        while action not in valid_moves:

            # Needed for pygame (ignore)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Get mouse position (relative to top-left corner of pygame window)
            mouse_x, mouse_y = self.pygame_instance.mouse.get_pos()
       

            # Transform so mouse position is relative to BOTTOM RIGHT corner of pygame window
            transformed_x = self.width - mouse_x
            transformed_y = self.height - mouse_y

            # Traslate mouse position to square coordinates
            cell_x = transformed_x // 100
            cell_y = transformed_y // 100

            # Translate square coordinates to square index
            square = (8 * cell_y) + cell_x

            # Get if mouse is currently being held down (boolean)
            left, _, _ = self.pygame_instance.mouse.get_pressed()
    
            # If mouse is held down AND we have not selected a square, then this is the FIRST loop of a press
            if left and attempted_from_square == -1:
                attempted_from_square = square

            # First loop AFTER letting go of mouse press
            if not left and attempted_from_square != -1:
          
                # Square mouse ORIGINALLY hovered over
                attempted_to_square = square

                # CONTINUE if we held in place / misclicked
                if attempted_from_square == attempted_to_square:
                    action = -1
                    continue

                # Calculating action value (preprocessing) TODO turn into function
                piece_type = state.type_at_each_square[attempted_from_square]
                left_shift_amount = attempted_to_square - attempted_from_square

                print("Attempted move's LEFT SHIFT AMOUNT", left_shift_amount)

                # Dummy initialization
                move_type = -9999999

                # Handle left_shift to move_type translation TODO turn into function
                if left_shift_amount == 7:
                    if attempted_from_square in [0,8,16,24,32,40,48,56]:
                        move_type = 48
                    else:
                        move_type = 7

                elif left_shift_amount == -7:
                    if attempted_from_square in [7, 15, 23, 31, 39, 47, 55, 63]:
                        move_type = 20
                    else:
                        move_type = 35

                elif left_shift_amount == 6:
                    if attempted_from_square in [0,8,16,24,32,40,48,56, 1, 9, 17, 25, 33, 41, 49, 57] and piece_type != WHITE_KNIGHT:
                        move_type = 47
                    else:
                        move_type = 57
                
                elif left_shift_amount == -6:
                    if attempted_from_square in [7, 15, 23, 31, 39, 47, 55, 63, 6, 14, 22, 30, 38, 46, 54, 62] and piece_type != WHITE_KNIGHT:
                        move_type = 19
                    else:
                        move_type = 61

                else:
                    if left_shift_amount in Left_Shift_to_Movement_type:
                        move_type = Left_Shift_to_Movement_type[left_shift_amount]

                # Compute action
                action = (move_type*64) + attempted_from_square

                # Reset attempted drag square
                attempted_from_square = -1

                # Print attempted action
                print("Attempted ACTION:", action)

            pygame.time.wait(10)
        
        return action

        

    #move sound, capture sound, castle sound, game over sound
    def play_sound(self, move_category):

        if move_category == 0:
            self.move_sound.play()
        elif move_category == 1:
            self.capture_sound.play()
        elif move_category == 2:
            self.castle_sound.play()


    def visualize(self, game, old_index, new_index, make_move=False, capture=False, sound=True):

        #TODO: init here IF FIRST CALL
        if self.first_visualize:
            self.full_init()
            self.first_visualize = False
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display background
        self.draw_background(old_index, new_index, make_move)
        

        # Draw white pieces
        for pieces_t in self.white_piece_map:
            pieces = game.pieces[pieces_t]
            bitboard_string = Bitboard.to_string(pieces.bitboard)
            for i in range(len(bitboard_string)):
                if bitboard_string[i] == '1':

                    #draw piece
                    piece = self.white_piece_map[pieces.type]
                    x = i % 8
                    y = i // 8
                    self.window.blit(piece, (x*self.cell_width, y*self.cell_height))

        # Draw black pieces
        for pieces_t in self.black_piece_map:
            pieces = game.pieces[pieces_t]
            bitboard_string = Bitboard.to_string(pieces.bitboard)
            for i in range(len(bitboard_string)):
                if bitboard_string[i] == '1':

                    #draw piece
                    piece = self.black_piece_map[pieces.type]
                    x = i % 8
                    y = i // 8
                    self.window.blit(piece, (x*self.cell_width, y*self.cell_height))
        
        # Refresh screen
        self.pygame_instance.display.update()
        self.pygame_instance.display.set_caption("Chess")