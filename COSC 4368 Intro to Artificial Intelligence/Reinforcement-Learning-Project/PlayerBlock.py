import pygame
import random
import copy

class PlayerBlock():
    def __init__(self, starting_x, starting_y, name, Q_Table={}):
        self.position = [starting_x, starting_y]
        self.has_food = False
        self.player_name = name

        # For game playback and troubleshooting
        self.move_history = []
        self.q_value_history = []

        self.game_piece_px = 105
        if self.player_name == 'M':
            self.block_img = pygame.image.load('graphics/M_Block.png')
            self.block_img_food = pygame.image.load('graphics/M_Block_Food.png')
        else: 
            self.block_img = pygame.image.load('graphics/F_Block.png')
            self.block_img_food = pygame.image.load('graphics/F_Block_Food.png')
        self.block_img = pygame.transform.scale(self.block_img,(self.game_piece_px, self.game_piece_px))
        self.block_img_food = pygame.transform.scale(self.block_img_food,(self.game_piece_px, self.game_piece_px))

        self.game_piece = self.block_img

        self.dropped_off_food = 0

        self.Q_Table = Q_Table
    
    def get_position(self):
        return self.position
    
    def get_name(self):
        return self.player_name
    
    def get_game_piece(self):
        return self.game_piece
    
    def get_move_history(self):
        return self.move_history
    
    def get_q_history(self):
        return self.q_value_history
    
    def get_has_food(self):
        return self.has_food
    
    def get_dropped_off_food(self):
        return self.dropped_off_food
    
    def set_has_food(self, val):
        if val == True:
            self.game_piece = self.block_img_food
        else:
            self.game_piece = self.block_img
        self.has_food = val

    def move(self, direction):
        possible_moves = {'left': [-1,0], 'right': [1,0], 'up': [0,-1], 'down': [0,1]}
        if direction not in possible_moves:
            raise KeyError(f'{direction} is not a possible move')
        
        new_x, new_y = self.position[0] + possible_moves[direction][0], self.position[1] + possible_moves[direction][1]
        self.position = [new_x, new_y]

        self.move_history.append(direction)

    def pickup(self, the_board):        # Returns bool indicating whether the move was successful or not
        if self.has_food == True:
            print('Has food already')
            return False
        # Make sure it's a legal move to do so
        for pickup_square in the_board.get_pickup_squares():
            if pickup_square[0] == self.position[0] and pickup_square[1] == self.position[1] and pickup_square[2] != 0:
                self.set_has_food(True)
                pickup_square[2] -= 1
                self.move_history.append('pickup')
                return True
        print('Cannot pickup')
        return False
    
    def dropoff(self, the_board):       # Returns bool indicating whether the move was successful or not
        # Can only dropoff if agent has food
        if self.has_food == False:
            print('Has no food to dropoff')
            return False
        # Make sure it's a legal move to do so
        for dropoff_square in the_board.get_dropoff_squares():
            if (dropoff_square[0] == self.position[0] and dropoff_square[1] == self.position[1]) and dropoff_square[2] != 0:     # If the agent is on an available dropoff square
                self.set_has_food(False)
                dropoff_square[2] -= 1
                self.move_history.append('dropoff')
                return True
        print('Cannot dropoff')
        return False

    def display_position(self, screen, row_height, column_width, grid_padding, square_padding):
        screen.blit(self.game_piece, (self.position[0] * column_width + grid_padding + square_padding, self.position[1] * row_height + grid_padding + square_padding))

    # Where the magic happens
    def choose_move(self, Q_Table, Board, inactive_player, policy='PRANDOM'):
        initial_position = tuple(self.position)
        q_values = Q_Table.get_q_values(self.has_food, initial_position, Board)

        # PRANDOM/PEXPLIOT/PGREEDY: If agent can pickup or dropoff, always do so.
        if policy in ["PRANDOM", "PEXPLOIT", "PGREEDY"]:
            if self.has_food and Board.check_dropoff_legal(self.position):
                return 'dropoff'
            
            if (not self.has_food) and Board.check_pickup_legal(self.position):
                return "pickup"
        
        # PRANDOM POLICY
        if policy == "PRANDOM":
            possible_moves = list(q_values.keys())
            random.shuffle(possible_moves)
            for move in possible_moves:
                if move == "pickup" and (not self.has_food) and Board.check_pickup_legal(self.position):
                    return move
                if move == "dropoff" and self.has_food and Board.check_dropoff_legal(self.position):
                    return move
                if move == "pickup" or move == "dropoff":
                    continue
                if Board.check_legal_move(self, move, inactive_player):
                    return move
        
        if policy == "PEXPLOIT":
            # Make copy of q_values without pickup and dropoff options
            cardinal_q_vals = copy.deepcopy(q_values)
            cardinal_q_vals.pop('pickup')
            cardinal_q_vals.pop('dropoff')

            # Get the best move key and get all the other possible cardinal movement values in a list
            best_move = max(cardinal_q_vals, key=cardinal_q_vals.get)
            best_moves = [k for k, v in cardinal_q_vals.items() if v == cardinal_q_vals[best_move]]
            random.shuffle(best_moves)      # Random tiebreaks
            best_move = best_moves[0]
            if not Board.check_legal_move(self, best_move, inactive_player):    # If best move interferes with other player, choose second best
                cardinal_q_vals.pop(best_move)
                best_move = max(cardinal_q_vals, key=cardinal_q_vals.get)
            cardinal_q_vals.pop(best_move)
            cardinal_q_vals = list(cardinal_q_vals.keys())

            # 80% chance to choose the best move, 20% choose to randomly choose another possible move
            rand_num = random.randint(1,101)
            if rand_num <= 80:
                return best_move
            else:
                random.shuffle(cardinal_q_vals)
                for move in cardinal_q_vals:
                    if Board.check_legal_move(self, move, inactive_player):
                        return move
                return best_move    # When only best move is legal
        
        if policy == "PGREEDY":
            # Make copy of q_values without pickup and dropoff options
            cardinal_q_vals = copy.deepcopy(q_values)
            cardinal_q_vals.pop('pickup')
            cardinal_q_vals.pop('dropoff')

            # Get the best move key and get all the other possible cardinal movement values in a list
            best_move = max(cardinal_q_vals, key=cardinal_q_vals.get)
            best_moves = [k for k, v in cardinal_q_vals.items() if v == cardinal_q_vals[best_move]]
            random.shuffle(best_moves)      # Random tiebreaks
            best_move = best_moves[0]
            if not Board.check_legal_move(self, best_move, inactive_player):    # If best move interferes with other player, choose second best
                cardinal_q_vals.pop(best_move)
                best_move = max(cardinal_q_vals, key=cardinal_q_vals.get)
            return best_move
    
    def make_move(self, the_move, Q_Table, Board, policy):
        
        # Save initial state (so can update Q-Table with info once move is made)
        initial_position = tuple(self.position)
        initial_availability = Board.get_pickup_dropoff_availability(self.has_food)
        initial_has_food = self.has_food

        # Save current q-values of actions for current state
        self.q_value_history.append(copy.deepcopy(Q_Table.get_q_values(initial_has_food, initial_position, Board)))

        # Make the move
        if the_move == 'pickup':
            self.pickup(Board)
            reward = 13.0
        elif the_move == 'dropoff':
            self.dropoff(Board)
            reward = 13.0
        else:
            self.move(the_move)
            reward = -1.0
        
        # Save new state information
        new_position = tuple(self.position)
        new_availability = Board.get_pickup_dropoff_availability(self.has_food)
        new_has_food = self.has_food

        # Update Q-Table using new and old state information
        Q_Table.update_old_q_value(reward, the_move, initial_has_food, initial_availability, initial_position, new_has_food, new_availability, new_position, Board, policy)
        # print(Q_Table.get_q_values(initial_has_food, initial_position, Board))
        return
