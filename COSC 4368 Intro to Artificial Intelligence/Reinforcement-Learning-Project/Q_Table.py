import numpy as np
import copy
from abc import abstractmethod
from GameBoard import GameBoard
import random

class LearningTable():
    def __init__(self, rows, columns, gamma=0.5, alpha=0.3):
        # The Q-table needs to take into account the following:
        # Whether or not the agent has food (Top level)
        # Pickup spot availability if agent has no food, Dropoff spot availability if agent has food (second to top)
        # Agent Position (second to bottom)
        # Agent movement action (Bottom level)
        self.gamma = gamma
        self.alpha = alpha
        
        Board = GameBoard(rows, columns)    # Only for checking out of bounds
        x = 0
        possible_actions = ['up', 'down', 'left', 'right']      # pickup/dropoff action unneeded because agent always does if available
        position_dict = {}      # Position tuple as key, action_q_val dict as values
        for i in range(rows):
            for j in range(columns):
                possible_actions_dict = {'pickup': 0.0, 'dropoff': 0.0}
                for move in possible_actions:
                    if Board.check_out_of_bounds([i, j], move):
                        possible_actions_dict[move] = 0.0
                position_dict[(i, j)] = copy.deepcopy(possible_actions_dict)
        
        # Now one position dict for each tuple of available pickup or dropoffs

        # Pickup - 2 for loops because 2 pickup locations
        pickup_avail_dict = {(a, b): copy.deepcopy(position_dict) for a in range(2) for b in range(2)}

        # Dropoff - 4 for loops because 4 dropoff locations
        dropoff_avail_dict = {(a,b,c,d): copy.deepcopy(position_dict) for a in range(2) for b in range(2) for c in range(2) for d in range(2)}
        
        self.q_table = {False: copy.deepcopy(pickup_avail_dict), True: copy.deepcopy(dropoff_avail_dict)}

    def get_q_values(self, has_food_bool, position_tuple, the_board):
        availability_tuple = the_board.get_pickup_dropoff_availability(has_food_bool)

        q_values = self.q_table[has_food_bool][availability_tuple][position_tuple]
        return q_values
    
    def q_table_size(self):
        """Returns number of states and state-action pairs"""
        states = 0
        state_action_pairs = 0
        for tf in self.q_table:
            for perm in self.q_table[tf]:
                for pos in self.q_table[tf][perm]:
                    states += 1
                    for act in self.q_table[tf][perm][pos]:
                        state_action_pairs += 1
        return [states, state_action_pairs]
    
    def set_alpha(self, new_alpha):
        self.alpha = new_alpha
    
    def set_gamma(self,new_gamma):
        self.gamma = new_gamma
    
    def delete_pickup_qvals(self):
        for tf in self.q_table:
            for perm in self.q_table[tf]:
                for pos in self.q_table[tf][perm]:
                    self.q_table[tf][perm][pos]['pickup'] = 0.0
    
    def choose_move_lt(self, policy, has_food_bool, position_tuple, Board):   ### initial_position must be a list
        position_list = list(position_tuple)
        q_values = self.get_q_values(has_food_bool, position_tuple, Board)

        # PRANDOM/PEXPLIOT/PGREEDY: If agent can pickup or dropoff, always do so.
        if policy in ["PRANDOM", "PEXPLOIT", "PGREEDY"]:
            if has_food_bool and Board.check_dropoff_legal(position_list):
                return 'dropoff'
            
            if (not has_food_bool) and Board.check_pickup_legal(position_list):
                return "pickup"
        
        if policy == "PRANDOM":
            possible_moves = list(q_values.keys())
            random.shuffle(possible_moves)
            for move in possible_moves:
                if move == "pickup" and (not has_food_bool) and Board.check_pickup_legal(position_list):
                    return move
                if move == "dropoff" and has_food_bool and Board.check_dropoff_legal(position_list):
                    return move
                if move == "pickup" or move == "dropoff":
                    continue
                return move     # No need to check legality because other player's future location is indeterminate.
        
        if policy == "PEXPLOIT":
            # Create copy of move list, minus pickup and dropof
            cardinal_q_vals = copy.deepcopy(q_values)
            cardinal_q_vals.pop('pickup')
            cardinal_q_vals.pop('dropoff')

            # Get the best move key and get all the other possible cardinal movement values in a list
            best_move = max(cardinal_q_vals, key=cardinal_q_vals.get)
            cardinal_q_vals.pop(best_move)
            cardinal_q_vals = list(cardinal_q_vals.keys())

            # 80% chance to choose the best move, 20% choose to randomly choose another possible move
            rand_num = random.randint(1,101)
            if rand_num <= 80:
                return best_move
            else:
                random.shuffle(cardinal_q_vals)
                return cardinal_q_vals[0]
            
        if policy == "PGREEDY":
            # Make copy of q_values without pickup and dropoff options
            cardinal_q_vals = copy.deepcopy(q_values)
            cardinal_q_vals.pop('pickup')
            cardinal_q_vals.pop('dropoff')

            # return the best move
            return max(cardinal_q_vals, key=cardinal_q_vals.get)
    
    @abstractmethod
    def update_old_q_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def TD(self, *args, **kwargs):
        pass

    @abstractmethod
    def Bellman_Eq(self, *args, **kwargs):
        pass

class QTable(LearningTable):
    def __init__(self, rows, columns, gamma=0.5, alpha=0.3):
        super().__init__(rows, columns, gamma, alpha)

    def TD(self, reward, current_max_q, previous_q):
        return reward + self.gamma * current_max_q - previous_q

    def Bellman_Eq(self, previous_q, temporal_difference):
        return previous_q + self.alpha * temporal_difference

    def update_old_q_value(self, reward, move, old_has_food, old_availability, old_position, new_has_food, new_availability, new_position, Board, policy='PGREEDY'):
        old_q_val = self.q_table[old_has_food][old_availability][old_position][move]
        new_state_q_vals = self.q_table[new_has_food][new_availability][new_position]
        new_state_max_q = max(new_state_q_vals.values())

        td = self.TD(reward, new_state_max_q, old_q_val)
        updated_q_val = self.Bellman_Eq(old_q_val, td)
        
        self.q_table[old_has_food][old_availability][old_position][move] = updated_q_val

class SARSATable(LearningTable):
    def __init__(self, rows, columns, gamma=0.5, alpha=0.3):
        super().__init__(rows, columns, gamma, alpha)

    def TD(self, reward, next_q, previous_q):
        return reward + self.gamma * next_q - previous_q

    def Bellman_Eq(self, previous_q, temporal_difference):
        return previous_q + self.alpha * temporal_difference

    def update_old_q_value(self, reward, move, old_has_food, old_availability, old_position, new_has_food, new_availability, new_position, Board, policy="PGREEDY"):
        old_q_val = self.q_table[old_has_food][old_availability][old_position][move]
        new_state_q_vals = self.q_table[new_has_food][new_availability][new_position]
        policy_move = self.choose_move_lt(policy, new_has_food, new_position, Board)
        policy_q_val = new_state_q_vals[policy_move]
        
        td = self.TD(reward, policy_q_val, old_q_val)
        updated_q_val = self.Bellman_Eq(old_q_val, td)

        self.q_table[old_has_food][old_availability][old_position][move] = updated_q_val

# # For checking size of q-table
# Test_obj = Alt_Q_Table(5, 5)
# print(Test_obj.q_table_size())

# # EXAMPLE INTERACTION WITH Q_TABLE
# # Get the q values for actions when:
# # -Agent has food (True)
# # -All dropoff points are available (1,1,1,1)
# # -Agent is at position (0,0)
# print(Test_obj.q_table[True][(1,1,1,1)][(0,0)])

