import csv
import os
from datetime import datetime
from Q_Table import LearningTable, QTable


def to_csv(Learning_Table, learning_mode, experiment=''):
    if not os.path.exists('./experiment_logs'):
        os.makedirs('./experiment_logs')

    if experiment == '':
        filename = f'./experiment_logs/{learning_mode}__{datetime.now().strftime("%m_%d_%Y__%H_%M_%S.csv")}'
    else:
        filename = f'./experiment_logs/{experiment}_{datetime.now().strftime("%m_%d_%Y__%H_%M_%S.csv")}'
    q_table = Learning_Table.q_table
    move_list = ['left', 'right', 'up', 'down', 'pickup', 'dropoff']

    # Create Header String
    fieldnames = ['Carrying Food', 'Pickup/Dropoff Availability', 'Position', 'Left Q-Value', 'Right Q-Value', 'Up Q-Value', 'Down Q-Value', 'Pickup', 'Dropoff']

    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for food in q_table:
            for avail in q_table[food]:
                for position in q_table[food][avail]:
                    move_dict = {move: q_table[food][avail][position][move] if move in q_table[food][avail][position] else -999.99 for move in move_list}
                    writer.writerow({
                        'Carrying Food': food,
                        'Pickup/Dropoff Availability': avail,
                        'Position': position,
                        'Left Q-Value': move_dict['left'],
                        'Right Q-Value': move_dict['right'],
                        'Up Q-Value': move_dict['up'],
                        'Down Q-Value': move_dict['down'],
                        'Pickup': move_dict['pickup'],
                        'Dropoff': move_dict['dropoff'],
                    })

