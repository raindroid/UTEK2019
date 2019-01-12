import re
import collections

# input format

def parse_input(lines):
    '''
    parses a header row: n_robots, n_items, n_obstacles
    items (x, y, product id, weight (in kg))
    followed by obstacles (x1, y1, x2, y2)
    '''
    header = next(lines)
    n_robots, n_items, n_obstacles = map(int, header.split(','))
    parsed_lines = [line.strip().strip('()').split(',') for line in lines]
    items = [(int(x), int(y), int(product_number), float(weight)) for x, y, product_number, weight in parsed_lines[:n_items]]
    obstacles = [[int(coord) for coord in line] for line in parsed_lines[n_items:]]

    return n_robots, items, obstacles

def parse_paths(paths, n_robots):
    '''
    parses the proposed path from a multi-line string
    returns a list of commands:
    move 1 3; pick 4; move 5 4   # there are 3 robots, we issue 2 move commands, 1 pick command
    '''
    commands = [line.strip().strip('()').split(';') for line in paths]

    # validate that all commands are valid
    for line in commands:
        for command in line:
            if not re.match(r'\s*(move\s+\d+\s+\d+|drop\s+\d+|pick\s+\d+|rest)\s*', command):
                raise ValueError('could not parse command', command)

    paths = [[command.split() for command in line] for line in commands]

    return paths

def validate_constraints(paths, items, obstacles=[]):
    '''
    validate the path with the following constraints:
    - max weight is never exceeded
    - the robot only takes one step at a time
    - all items are collected
    - robots never collide with object/ other robots
    returns whether it passes
    '''

    n_robots = len(paths[0])

    item_weights = {product_num: weight for (x, y, product_num, weight) in items}
    held_items = [[] for i in range(n_robots)] # list of item_ids held
    positions = [(i, 0) for i in range(n_robots)] # keep track of position for each robot

    item_locations = collections.defaultdict(list)  # {id: [(x, y), (x2, y2), ...]}

    for item in items:
        (x, y, product_num, weight) = item
        item_locations[product_num].append((x, y))

    for timestep in paths:
        for idx, command in enumerate(timestep):
            action, *operands = command

            if action == 'move':
                x, y = map(int, operands)

                if abs(positions[idx][0] - x) > 1 or abs(positions[idx][1] - y) > 1 or positions[idx][0] < 0 or positions[idx][1] < 0 or positions[idx][0] > 100 or positions[idx][1] > 100:
                    print('Invalid step')
                    return False # robot can't move more than one step

                positions[idx] = (x, y)

                # verify that we don't collide with an obstacle
                for obstacle in obstacles:
                    x1, y1, x2, y2 = obstacle
                    if x1 <= positions[idx][0] <= x2 and y1 <= positions[idx][1] <= y2:
                        print('Collision with obstacle')
                        return False
            elif action == 'pick':
                item_id = int(operands[0])

                if positions[idx] in item_locations[item_id]:
                    item_qty = item_locations[item_id].remove(positions[idx])
                    held_items[idx].append(item_id)
                else:
                    print('Tried to pick up an item that doesnt exist at that location.', item_id, item_locations[item_id])
                    return False

                # verify that the max weight isn't exceeded
                if sum(item_weights[item] for item in held_items[idx]) > 100:
                    print('Exceeded max weight.')
                    return False

            elif action == 'rest':
                pass

            elif action == 'drop':
                item_id = int(operands[0])

                try:
                    held_items[idx].remove(item_id)
                except:
                    print('tried to drop an item that the robot isnt holding.', item_id)
                    return False

                if positions[idx] != (0, 0):
                    print('placing items on the ground is not allowed.')
                    return False

        # verify that robots don't collide
        if len(set(positions)) != n_robots:
            print('robots collided')
            return False # robots collided

    if any(item_locations[item_id] for item_id in item_locations):
        print('Didnt fetch all items')
        return False

    return True

def score_output(path, items, obstacles):
    ''' generate a score'''
    if not validate_constraints(paths, items, obstacles):
        return 0
    else:
        score = len(path)
        return score

if __name__ == '__main__':
    scores = {num + ch: 0 for num in '2345' for ch in 'abc'}

    for num in '2345':
        for ch in 'abc':
            testcase_id = num + ch
            print('Running ', testcase_id)
            try:
                with open(testcase_id + '.in') as input_f, open(testcase_id + '.out') as output_f:
                    n_robots, items, obstacles = parse_input(input_f)
                    paths = parse_paths(output_f, n_robots)

                    scores[testcase_id] = score_output(paths, items, obstacles)
            except FileNotFoundError:
                scores[testcase_id] = 0

    print(scores)
