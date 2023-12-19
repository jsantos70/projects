import pygame
import numpy as np
from sys import exit
from time import sleep, time

from GameBoard import GameBoard
from PlayerBlock import PlayerBlock
from Q_Table import QTable, SARSATable
from visualize import to_csv

# Takes Learn_Table as an argument, and returns it, so the same Q-values can be continuously updated as we simulate more games.
# Conceptual for now and subject to change.
def simulate_game(Learn_Table, turns_remaining, policy='PRANDOM', pickup_squares=[[1, 3, 10], [4, 2, 10]]):
    # Instantiate Board and Agents
    Board = GameBoard(5, 5)
    Board.set_pickup_squares(pickup_squares)
    Male_Player = PlayerBlock(2, 4, 'M', Learn_Table)
    Female_Player = PlayerBlock(2, 0, 'F', Learn_Table)

    terminal_state_reached = False
    number_of_moves = 0

    # The while loop handles each players turns until a terminal state is reached.
    while True:
        f_move = Female_Player.choose_move(Learn_Table, Board, Male_Player, policy)
        Female_Player.make_move(f_move, Learn_Table, Board, policy)

        m_move = Male_Player.choose_move(Learn_Table, Board, Female_Player, policy)
        Male_Player.make_move(m_move, Learn_Table, Board, policy)
        
        turns_remaining -= 2    # Maybe vestigial
        number_of_moves += 2
        
        # Ends the game once we reach a terminal state or the turn limit.
        if Board.check_terminal_state(Female_Player, Male_Player):
            terminal_state_reached = True
            break

        if turns_remaining <= 0:
            break
        

    female_agent_moves = Female_Player.get_move_history()
    male_agent_moves = Male_Player.get_move_history()
    female_agent_q_history = Female_Player.get_q_history()
    male_agent_q_history = Male_Player.get_q_history()
    game_information = {
        'agent_policy': policy,
        'number_of_moves': number_of_moves,
        'terminal_state_reached': terminal_state_reached,
        'game_transcript': [female_agent_moves, male_agent_moves],
        'pickup_squares': pickup_squares,
        'q_history': [female_agent_q_history, male_agent_q_history]
    }
    return game_information, Learn_Table, turns_remaining

def playback_recorded_game(game, speed=0.25):

    # Playback speed - time between moves
    seconds_to_wait = speed

    print('Recorded Game: ')
    print("Policy: " + game['agent_policy'])
    print("Number of moves: " + str(game['number_of_moves']))
    print("Terminal state reached: " + str(game['terminal_state_reached']))
    female_agent_moves = game['game_transcript'][0]
    male_agent_moves = game['game_transcript'][1]
    female_agent_q = game['q_history'][0]
    male_agent_q = game['q_history'][1]
    pickup_squares = game['pickup_squares']

    all_moves = []
    all_q = []

    for i in range(len(female_agent_moves)):
        all_moves.append(female_agent_moves[i])
        all_moves.append(male_agent_moves[i])
        all_q.append(female_agent_q[i])
        all_q.append(male_agent_q[i])

    pygame.init()

    # Set parameters for width, height, background color, and title of the window.
    screen_width = 1400
    screen_height = 750
    background_color = (255, 255, 255)  #RGB
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('PD World')
    screen.fill(background_color)   # Background color

    # Load graphics
    f_block = pygame.image.load('graphics/F_Block.png')
    m_block = pygame.image.load('graphics/M_Block.png')
    f_block_food = pygame.image.load('graphics/F_Block_Food.png')
    m_block_food = pygame.image.load('graphics/M_Block_Food.png')

    # Allows to regulate tick rate
    clock = pygame.time.Clock()

    # Instantiate Board and Agents
    Board = GameBoard(5, 5)
    Board.set_pickup_squares(pickup_squares)
    Male_Player = PlayerBlock(2, 4, 'M')
    Female_Player = PlayerBlock(2, 0, 'F')

    active_player = Female_Player
    successful_move = False
    current_move = 0

    last_time = time()
    game_ongoing = True

    # Main loop
    play = True
    while play:
        
        for event in pygame.event.get():    # Quit and speed controls
            if event.type == pygame.QUIT:
                # pygame.quit()
                # exit()
                pygame.display.quit()
                return
            if event.type == pygame.KEYDOWN:    # Detects that a key was pressed
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:     # Detects Left Arrow Key Press
                    seconds_to_wait = seconds_to_wait * 2
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:     # Detects Right Arrow Key Press
                    seconds_to_wait = seconds_to_wait / 2
        
        if time() - last_time > seconds_to_wait and game_ongoing:
            last_time = time()
            if all_moves[current_move] == 'pickup':
                active_player.pickup(Board)
                successful_move = True
            
            if all_moves[current_move] == 'dropoff':
                active_player.dropoff(Board)
                successful_move = True

            if all_moves[current_move] not in ['pickup','dropoff']:
                active_player.move(all_moves[current_move])
                successful_move = True

        
        if successful_move:
            current_move += 1
            if active_player == Male_Player:
                active_player = Female_Player
            else:
                active_player = Male_Player
        successful_move = False

        if current_move >= len(all_moves):
            game_ongoing = False
            pygame.display.quit()
            break

        # Update the display at 60 frames per second
        Board.display_board(Male_Player, Female_Player, active_player, screen, current_move, all_q[current_move], seconds_to_wait)
        clock.tick(60)

def test_and_debug(Learn_Table):
    print(Learn_Table.q_table[True][(1,1,1,1)][(4,1)])
    exit = 'n'
    while exit == 'n':
        has_food_dict = {'y': True, 'n': False}
        has_food_inp = input('Has food? y/n: ')
        posx = int(input('X-coordinate?'))
        posy = int(input('Y-coordinate?'))
        print(Learn_Table.q_table[has_food_dict[has_food_inp]][(1,1,1,1)][(posx,posy)])
        exit = input('exit? y/n: ')
    return

def reinitialize(learning_method, rows, columns):
    if learning_method == 'Q_LEARNING':
        Learn_Table = QTable(rows,columns)
    elif learning_method == 'SARSA':
        Learn_Table = SARSATable(rows, columns)
    
    return Learn_Table, [], 0, 0

def experiment(exp_number, rows, columns):

    num_games = 0

    # Experiment 1
    if exp_number == '1':
        # Part A
        
        learning_mode = 'Q_LEARNING'
        Learn_Table, game_list, terminal_states_reached, total_terminal_states_reached = reinitialize(learning_mode, rows, columns)
        info_string = f'\nExperiment 1\nPart A Games: {num_games + 1} to '

        policy = 'PRANDOM'
        steps = 8000
        while steps > 0:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        
        print(policy + ' - Terminal States Reached: ' + str(terminal_states_reached))
        total_terminal_states_reached += terminal_states_reached
        print('Total Terminal States Reached: ' + str(total_terminal_states_reached))
        to_csv(Learn_Table, learning_mode, 'Experiment_1A')     # Sends Q-Table results to csv
        info_string += f'{num_games}'

        # Part B

        learning_mode = 'Q_LEARNING'
        Learn_Table, none, terminal_states_reached, total_terminal_states_reached = reinitialize(learning_mode, rows, columns)
        info_string += f'\nPart B Games: {num_games + 1} to '

        policy = 'PRANDOM'
        steps = 500
        while steps > 0:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        
        policy = 'PGREEDY'
        steps = 7500
        while steps > 0:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        
        print(policy + ' - Terminal States Reached: ' + str(terminal_states_reached))
        total_terminal_states_reached += terminal_states_reached
        print('Total Terminal States Reached: ' + str(total_terminal_states_reached))
        to_csv(Learn_Table, learning_mode, 'Experiment_1B')     # Sends Q-Table results to csv
        info_string += f'{num_games}'
    
        # Part C

        learning_mode = 'Q_LEARNING'
        Learn_Table, none, terminal_states_reached, total_terminal_states_reached = reinitialize(learning_mode, rows, columns)
        info_string += f'\nPart C Games: {num_games + 1} to '

        policy = 'PRANDOM'
        steps = 500
        while steps > 0:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        
        policy = 'PEXPLOIT'
        steps = 7500
        while steps > 0:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        
        print(policy + ' - Terminal States Reached: ' + str(terminal_states_reached))
        total_terminal_states_reached += terminal_states_reached
        print('Total Terminal States Reached: ' + str(total_terminal_states_reached))
        to_csv(Learn_Table, learning_mode, 'Experiment_1C')     # Sends Q-Table results to csv
        info_string += f'{num_games}'
    
    if exp_number in ['2', '3']:
        game_list = []
        info_string = f'\nExperiment {exp_number} Games: '
        alpha_list = [0.3] if exp_number == '2' else [0.15, 0.45]
        for i, alpha in enumerate(alpha_list):
            learning_mode = 'SARSA'
            Learn_Table, none, terminal_states_reached, total_terminal_states_reached = reinitialize(learning_mode, rows, columns)
            Learn_Table.set_alpha(alpha)

            info_string += f'\nalpha {alpha} games: {num_games + 1} to '

            policy = 'PRANDOM'
            steps = 500
            while steps > 0:
                res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
                game_list.append(res)
                if res['terminal_state_reached'] == True:
                    terminal_states_reached += 1
                num_games += 1
            
            policy = 'PEXPLOIT'
            steps = 7500
            while steps > 0:
                res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
                game_list.append(res)
                if res['terminal_state_reached'] == True:
                    terminal_states_reached += 1
                num_games += 1
            
            print(policy + ' - Terminal States Reached: ' + str(terminal_states_reached))
            total_terminal_states_reached += terminal_states_reached
            print('Total Terminal States Reached: ' + str(total_terminal_states_reached))
            to_csv(Learn_Table, learning_mode, f'Experiment_{exp_number}')     # Sends Q-Table results to csv
            info_string += f'{num_games}'

    if exp_number == '4':
        learning_mode = 'Q_LEARNING'
        Learn_Table, game_list, terminal_states_reached, total_terminal_states_reached = reinitialize(learning_mode, rows, columns)
        info_string = f'\nExperiment 4\nPRANDOM Games: {num_games + 1} to '

        policy = 'PRANDOM'
        steps = 500
        while steps > 0:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        info_string += f'{num_games}\nPEXPLOIT Games: {num_games + 1} to '
        
        policy = 'PEXPLOIT'
        steps = 10000   # infinite basically - steps not the constraint on number of games here
        terminal_states_reached = 0
        while terminal_states_reached < 3:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        info_string += f'{num_games}\nPEXPLOIT Games With New Pickup Squares: {num_games + 1} to '
        
        policy = 'PEXPLOIT'
        Learn_Table.delete_pickup_qvals()   # Reinit pickup q-values since pickup is now illegal at old squares
        new_pickup_states = [[1, 0, 10], [4, 3, 10]]
        steps = 10000   # infinite basically - steps not the constraint on number of games here
        terminal_states_reached = 0
        while terminal_states_reached < 3:
            res, Learn_Table, steps = simulate_game(Learn_Table, steps, policy, new_pickup_states)
            game_list.append(res)
            if res['terminal_state_reached'] == True:
                terminal_states_reached += 1
            num_games += 1
        info_string += f'{num_games}'
        
        print(policy + ' - Terminal States Reached: ' + str(terminal_states_reached))
        total_terminal_states_reached += terminal_states_reached
        print('Total Terminal States Reached: ' + str(total_terminal_states_reached))
        to_csv(Learn_Table, learning_mode, 'Experiment_4')     # Sends Q-Table results to csv

    # FIXME: Return all games run during the experiment so they can be played back and analyzed.
    # Print information about which games are part a, b, and c.
    print(info_string)
    return game_list


def main():
    # Need a simple interface that allows to simulate games or select a game and display it.
    print('\nWelcome to PD World')
    # sleep(1)
    rows = 5 
    columns = 5

    print('\nCurrent Mode: Q-LEARNING')
    learning_mode = 'Q_LEARNING'
    Learn_Table = QTable(rows,columns)

    game_list = []
    playback_speed = 1.0
    total_terminal_states_reached = 0
    
    while True:
        menu_options = ['1', '2', '3', '4', '5', '7', '9', 'q']
        menu_choice = '0'
        while menu_choice not in menu_options:
            print('\n1: Simulate Games, 2: Playback Recorded Game, 3: Print Recorded Game, 4: Experiment Suites, 5: Settings, 9: Test and Debug, q: quit')
            menu_choice = input('Enter 1, 2, 3, 4, 5, 9, or q: ')
        
        if menu_choice == '1':      # 1: SIMULATE GAME
            terminal_states_reached = 0
            steps = -1
            while steps < 1:
                try:
                    steps = int(input('Simulate how many steps? '))
                except ValueError:
                    continue
            allowed_policies = {1: 'PRANDOM', 2: 'PEXPLOIT', 3: 'PGREEDY'}
            policy = 0
            while policy not in allowed_policies.keys():
                policy = int(input('Policy? 1: PRANDOM, 2: PEXPLOIT, 3: PGREEDY '))
            while steps > 0:
                res, Learn_Table, steps = simulate_game(Learn_Table, steps, allowed_policies[policy])
                game_list.append(res)
                if res['terminal_state_reached'] == True:
                    terminal_states_reached += 1
            print(allowed_policies[policy] + ' - Terminal States Reached: ' + str(terminal_states_reached))
            total_terminal_states_reached += terminal_states_reached
            print('Total Terminal States Reached: ' + str(total_terminal_states_reached))
        
        if menu_choice == '2':      # 2: PLAYBACK
            if len(game_list) < 1:
                print('\nThere are no games recorded.')
                continue
            print('\nThere are currently ' + str(len(game_list)) + ' game(s) recorded.')
            game_playback_choice = '0'
            while int(game_playback_choice) <= 0 or int(game_playback_choice) > len(game_list):
                game_playback_choice = input('Choose which to playback (Enter 1 for oldest, enter ' + str(len(game_list)) + ' for latest): ')
                if not game_playback_choice.isnumeric():
                    game_playback_choice = '0'
            
            int_playback_choice = int(game_playback_choice)
            playback_recorded_game(game_list[int_playback_choice - 1], playback_speed)
        
        if menu_choice == '3':      # 3: PRINT
            if len(game_list) < 1:
                print('\nThere are no games recorded.')
                continue
            print('\nThere are currently ' + str(len(game_list)) + ' games recorded.')
            game_print_choice = '0'
            while int(game_print_choice) <= 0 or int(game_print_choice) > len(game_list):
                game_print_choice = input('Choose which to print (Enter 1 for oldest, enter ' + str(len(game_list)) + ' for latest): ')
                if not game_print_choice.isnumeric():
                    game_print_choice = '0'
            
            int_print_choice = int(game_print_choice)
            print('\nGame #' + game_print_choice)
            print("Policy: " + game_list[int_print_choice - 1]['agent_policy'])
            print("Number of moves: " + str(game_list[int_print_choice - 1]['number_of_moves']))
            print("Terminal state reached: " + str(game_list[int_print_choice - 1]['terminal_state_reached']))
            # print(game_list[int_print_choice - 1]['game_transcript'])     # Uncomment to view full game transcript
        
        if menu_choice == '4':      # 4: Experiment Suites

            learning_mode = 'Q_LEARNING'
            Learn_Table, game_list, terminal_states_reached, total_terminal_states_reached = reinitialize(learning_mode, rows, columns)
            experiment_choice = '0'
            while experiment_choice not in ['1', '2', '3', '4']:
                experiment_choice = input('Experiment Suites: Enter 1, 2, 3, or 4: ')

            game_list += experiment(experiment_choice, rows, columns)

        
        if menu_choice == '5':      # 5: Settings
            print('Settings')
            print(f'Current Learning Mode: {learning_mode}')
            settings_choice = input('1: Switch Learning Mode, 2: Reinitialize Q-Table, 3: Set alpha, 4: Set gamma\n')
            if settings_choice == '1':
                if learning_mode == 'Q_LEARNING':
                    Learn_Table = SARSATable(rows, columns)
                    learning_mode = 'SARSA'
                elif learning_mode == 'SARSA':
                    Learn_Table = QTable(rows, columns)
                    learning_mode = 'Q_LEARNING'
            if settings_choice == '2':
                Learn_Table, game_list, terminal_states_reached, total_terminal_states_reached = reinitialize(learning_mode, rows, columns)
                print('Table reinitialized!')
                print("All games deleted. ")
            if settings_choice == '3':
                Learn_Table.set_alpha(float(input('New alpha value? ')))
            if settings_choice == '4':
                Learn_Table.set_gamma(float(input('New gamma value? ')))
            
        # if menu_choice == '9':      # 9: Test and Debug
        #     test_and_debug(Learn_Table)
        
        if menu_choice == 'q':      # q: QUIT
            print('\nBye\n')
            break

if __name__ == "__main__":
    main()
