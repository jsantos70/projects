import pygame
import numpy as np
import copy

class GameBoard():
    def __init__(self, rows, columns):
        # Grid Parameters
        self.rows = rows
        self.columns = columns
        self.grid_height = 700
        self.grid_width = 700
        self.row_height = self.grid_height // self.rows
        self.column_width = self.grid_width // self.columns
        self.grid_color = (0,0,0)
        self.grid_padding = 20
        self.square_padding = 18

        self.background_color = (100,100,100)

        # Pickup and Dropoff Point Parameters
        self.pickup_squares = [[1, 3, 10], [4, 2, 10]]               # Array of arrays [x position, y position, quantity of food]
        self.dropoff_squares = [[0, 0, 5], [2, 2, 5], [4, 0, 5], [4, 4, 5]]    # Array of arrays [x position, y position, remaining capacity]
        self.pickup_availability = [1, 1]
        self.dropoff_availability = [1, 1, 1, 1]

        # Pickup and Dropoff Point Graphics
        self.square_px = 105
        self.food1 = pygame.image.load('graphics/nana1.png')
        self.food2 = pygame.image.load('graphics/nana2.png')
        self.food3 = pygame.image.load('graphics/nana3.png')
        self.food4 = pygame.image.load('graphics/nana4.png')
        self.food5 = pygame.image.load('graphics/nana5.png')
        self.food6 = pygame.image.load('graphics/nana6.png')
        self.food7 = pygame.image.load('graphics/nana7.png')
        self.food8 = pygame.image.load('graphics/nana8.png')
        self.food9 = pygame.image.load('graphics/nana9.png')
        self.food10 = pygame.image.load('graphics/nana10.png')
        self.dropoff_img = pygame.image.load('graphics/Dropoff.png')
        self.food1 = pygame.transform.scale(self.food1,(self.square_px,self.square_px))
        self.food2 = pygame.transform.scale(self.food2,(self.square_px,self.square_px))
        self.food3 = pygame.transform.scale(self.food3,(self.square_px,self.square_px))
        self.food4 = pygame.transform.scale(self.food4,(self.square_px,self.square_px))
        self.food5 = pygame.transform.scale(self.food5,(self.square_px,self.square_px))
        self.food6 = pygame.transform.scale(self.food6,(self.square_px,self.square_px))
        self.food7 = pygame.transform.scale(self.food7,(self.square_px,self.square_px))
        self.food8 = pygame.transform.scale(self.food8,(self.square_px,self.square_px))
        self.food9 = pygame.transform.scale(self.food9,(self.square_px,self.square_px))
        self.food10 = pygame.transform.scale(self.food10,(self.square_px,self.square_px))
        self.dropoff_img = pygame.transform.scale(self.dropoff_img,(self.square_px,self.square_px))

    def get_pickup_squares(self):
        return self.pickup_squares
    
    def set_pickup_squares(self, pickup_squares):
        self.pickup_squares = copy.deepcopy(pickup_squares)
    
    def get_dropoff_squares(self):
        return self.dropoff_squares
    
    def get_pickup_dropoff_availability(self, player_has_food):
        avail_tuple = ()
        if player_has_food:
            for dropoff in self.dropoff_squares:
                x = int(dropoff[2] > 0)
                avail_tuple += (x,)
        else:
            for pickup in self.pickup_squares:
                x = int(pickup[2] > 0)
                avail_tuple += (x,)
        
        return avail_tuple
    
    def check_legal_move(self, player, the_move, inactive_player):
        player_position = player.get_position()

        if not self.check_interference(player, the_move, inactive_player):
            return False
        if not self.check_out_of_bounds(player_position, the_move):
            return False
        return True
    
    def check_interference(self, player, the_move, inactive_player):
        moves = {'left': [-1,0], 'right': [1,0], 'up': [0,-1], 'down': [0,1]}
        player_position = player.get_position()
        next_pos = np.add(player_position, moves[the_move])

        # Check overlap with other player
        if np.array_equal(next_pos, inactive_player.get_position()):
            #print('Illegal move. Cannot overlap opponent player.')
            return False
        else:
            return True

    def check_out_of_bounds(self, current_position, the_move):
        moves = {'left': [-1,0], 'right': [1,0], 'up': [0,-1], 'down': [0,1]}
        next_position = np.add(current_position, moves[the_move])
        # Check that the move is within grid
        if next_position[0] < 0 or next_position[0] >= self.columns or next_position[1] < 0 or next_position[1] >= self.columns:
            # print('Illegal move. Cannot exit grid.')
            return False
        else:
            # print('Legal Move: Not OOB')
            return True
    
    def check_pickup_legal(self, player_position):
        for pickup_square in self.pickup_squares:
            if player_position[0] == pickup_square[0] and player_position[1] == pickup_square[1] and pickup_square[2] > 0:
                return True
        return False
    
    def check_dropoff_legal(self, player_position):
        for dropoff_square in self.dropoff_squares:
            if player_position[0] == dropoff_square[0] and player_position[1] == dropoff_square[1] and dropoff_square[2] > 0:
                return True
        return False

    def get_pickup_img(self, quantity):
        if quantity == 1:
            return self.food1
        if quantity == 2:
            return self.food2
        if quantity == 3:
            return self.food3
        if quantity == 4:
            return self.food4
        if quantity == 5:
            return self.food5
        if quantity == 6:
            return self.food6
        if quantity == 7:
            return self.food7
        if quantity == 8:
            return self.food8
        if quantity == 9:
            return self.food9
        if quantity == 10:
            return self.food10

    def display_board(self, M_Player, F_Player, active_player, screen, move_num, q_vals, game_speed):
        screen.fill(self.background_color)
        # Draw grid
        x = 0
        y = 0
        line_width = 3
        for l in range(self.rows + 1):
            # pygame.draw.line(screen, grid_color, (x, 0), (x, grid_height))  # Without padding
            # pygame.draw.line(screen, grid_color, (0, y), (grid_width, y))   # Without padding
            pygame.draw.line(screen, self.grid_color, (x + self.grid_padding, self.grid_padding), (x + self.grid_padding, self.grid_height + self.grid_padding), width=line_width)  # With padding
            pygame.draw.line(screen, self.grid_color, (self.grid_padding, y + self.grid_padding), (self.grid_width + self.grid_padding, y + self.grid_padding), width=line_width)   # With padding
            x += self.row_height
            y += self.column_width
        
        # FIXME: Display Pickup and Dropoff Squares
        for pickup in self.pickup_squares:
            if pickup[2] != 0:      # Checks availability of pickup square
                pickup_img = self.get_pickup_img(pickup[2])
                screen.blit(pickup_img, (pickup[0] * self.column_width + self.grid_padding + self.square_padding, pickup[1] * self.row_height + self.grid_padding + self.square_padding))
        
        for dropoff in self.dropoff_squares:
            if dropoff[2] != 0:     # Checks availability of dropoff square
                screen.blit(self.dropoff_img, (dropoff[0] * self.column_width + self.grid_padding + self.square_padding, dropoff[1] * self.row_height + self.grid_padding + self.square_padding))

        # Display M and F agents
        M_Player.display_position(screen, self.row_height, self.column_width, self.grid_padding, self.square_padding)
        F_Player.display_position(screen, self.row_height, self.column_width, self.grid_padding, self.square_padding)

        # Display auxilliary information
        if game_speed >= 0.25:      # Epilepsy prevention
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(' Player\'s Turn: ', True, 'white', 'black')
            textRect = text.get_rect()
            text_x = 900
            text_y = 200
            textRect.center = (text_x, text_y)
            screen.blit(text, textRect)
            screen.blit(active_player.get_game_piece(), (text_x + 130, text_y - self.square_px // 2))
        
        # Display move information
        font_size = 22
        font = pygame.font.SysFont('arial', font_size)
        move_text = font.render('Move #: ' + str(move_num), True, 'black')
        move_text_x = 750
        move_text_y = 300
        screen.blit(move_text, (move_text_x, move_text_y))

        q_text_string = ''
        q_text_x = 750
        q_text_y = 350
        screen.blit(font.render('q_values: ', True, 'black'), (q_text_x, q_text_y))

        player_q_values = copy.deepcopy(q_vals)
        
        if player_q_values['pickup'] == 0.0: player_q_values.pop('pickup') 
        if player_q_values['dropoff'] == 0.0: player_q_values.pop('dropoff')
        highest_q_key = max(player_q_values, key = player_q_values.get)

        for i, key in enumerate(player_q_values.keys()):
            q_text_string = (key + ': ' + str(player_q_values[key]))
            if highest_q_key == key:
                q_text = font.render(q_text_string, True, 'green')
            else:
                q_text = font.render(q_text_string, True, 'black')
            screen.blit(q_text, (q_text_x, q_text_y + font_size*(i+1)))
        
        screen.blit(font.render(('Speed Control: Left/Right A/D; Seconds per turn: ' + str(game_speed)), True, 'black'), (900, 700))

        pygame.display.update()
    
    def check_terminal_state(self, f_player, m_player):
        if f_player.get_has_food() or m_player.get_has_food():      # If either player is carrying food, we're not in a terminal state.
            return False

        for pickup in self.pickup_squares:
            if pickup[2] > 0:       # If any pickup squares have at least one piece of food left, we're not in terminal state.
                return False

        return True     # If there is no food anywhere on the board or with the players, we're in a terminal state


# testobj = GameBoard(5,5)
# print(testobj.get_dropoff_availability())
