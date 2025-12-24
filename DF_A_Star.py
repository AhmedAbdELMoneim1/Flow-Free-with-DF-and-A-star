import numpy as np

moves = np.array([[0, -1], [0, 1], [-1, 0], [1, 0]])  # left right bottom top
opposite_directions = [1, 0, 3, 2]

empty_squares_weights = [3, 3, 2, 1, 1]


class FlowFree:
    def __init__(self, squares_arr: np.array):
        self.squares_arr: np.array = squares_arr
        self.colors_num: int = (squares_arr > 0).sum() // 2

        self.x_length, self.y_length = self.squares_arr.shape

        self.colors_status: dict = {}
        self.sorted_colors_order: list = []  # small paths length first start
        self.get_goal = lambda color_id: self.colors_status[color_id]["end"]

        self.check_directions_boundaries = [
            lambda y_arr_idx: y_arr_idx > 0,
            lambda y_arr_idx: y_arr_idx < self.y_length - 1,
            lambda x_arr_idx: x_arr_idx > 0,
            lambda x_arr_idx: x_arr_idx < self.x_length - 1
        ]
        self.__trash_stack = []
        self.__get_initial_colors_indexes()

        self.result_id = 2
        self.steps_number = 0
        self.states = []
        self.states.append(self.squares_arr.copy())
        self.track_back_tracking_steps = []

    def __get_initial_colors_indexes(self):
        xs, ys = np.where(self.squares_arr > 0)

        for x, y in zip(xs, ys):
            color = int(self.squares_arr[x, y])
            if color in self.colors_status:
                self.colors_status[color]["end"] = np.array([x, y])
                x1, y1 = self.colors_status[color]["start"]
                self.colors_status[color]["length"] = abs(y-y1) + abs(x-x1)
            else:
                self.colors_status[color] = {
                    "start": (x, y),
                    "end": None,
                    "length": 0,
                    "paths": []
                }
        self.sorted_colors_order = sorted(self.colors_status, key=lambda k: self.colors_status[k]["length"])

    def __draw(self, x, y, color_id):
        self.squares_arr[x, y] = color_id
        self.__trash_stack.append((x, y))
        self.steps_number += 1

    def __clear(self):
        x, y = self.__trash_stack[-1]
        self.squares_arr[x, y] = 0
        self.track_back_tracking_steps.append(self.steps_number)
        self.__trash_stack.pop()

    def __check_wasted_squares(self, x_arr_idx, y_arr_idx, last_color_direction, color_direction, color_id):
        opposite_last_direction_idx = opposite_directions[last_color_direction]
        opposite_last_direction = moves[opposite_last_direction_idx]

        opposite_direction_square = opposite_last_direction + [x_arr_idx, y_arr_idx]

        empty_squares = 0
        same_color_detection = 0
        wall_empty_square_detection = 0

        for _ in range(5):
            x, y = opposite_direction_square
            check_boundary_axis = y if opposite_last_direction_idx < 2 else x

            if self.squares_arr[x, y] == color_id:
                same_color_detection += 1
                break

            if self.squares_arr[x, y] > 0 and self.squares_arr[x, y] != color_id:
                break
            else:
                opposite_direction_square += opposite_last_direction
                empty_squares += 1

            if not self.check_directions_boundaries[opposite_last_direction_idx](check_boundary_axis):
                if empty_squares == 1:
                    wall_empty_square_detection += 1
                break

        if wall_empty_square_detection == 1:
            return True
        if same_color_detection == 1:
            if 3 > empty_squares > 0:
                return True
            else:  # empty_squares == 3 or 4
                mid_square = [x_arr_idx, y_arr_idx] + opposite_last_direction*2 + moves[color_direction]
                if self.check_directions_boundaries[color_direction](mid_square[1] if color_direction < 2 else mid_square[0]):
                    if self.squares_arr[mid_square[0], mid_square[1]] == 0:
                        return True
                    mid_square_neighbor = mid_square + opposite_last_direction
                    if empty_squares == 4 and self.squares_arr[mid_square_neighbor[0], mid_square_neighbor[1]] == 0:
                        return True
                else:
                    return True
        return False

    # heuristic A*
    def __create_next_order(self,  x_arr_idx, y_arr_idx, directions, color_goal):
        weights = [0, 0, 0, 0]  # left right top bottom

        dx = color_goal[0] - x_arr_idx
        dy = color_goal[1] - y_arr_idx

        vertical = 3 if dx > 0 else 2
        horizontal = 1 if dy > 0 else 0

        if abs(dx) > abs(dy):
            weights[vertical] += 3
            weights[horizontal] += 2
        else:
            weights[horizontal] += 3
            weights[vertical] += 2

        for d_idx in range(4):  # check left right bottom left   d_idx --> direction_index

            direction = directions[d_idx]
            check_boundary = self.check_directions_boundaries[d_idx](y_arr_idx if d_idx < 2 else x_arr_idx)

            if check_boundary and self.squares_arr[direction[0], direction[1]] == 0:
                x_dir, y_dir = direction
                directions_dir = moves + direction
                empty_squares = 0
                for d_idx_dir in range(4):
                    direction = directions_dir[d_idx_dir]
                    check_boundary = self.check_directions_boundaries[d_idx_dir](y_dir if d_idx_dir < 2 else x_dir)
                    if check_boundary and self.squares_arr[direction[0], direction[1]] == 0:
                        empty_squares += 1
                weights[d_idx] += empty_squares_weights[empty_squares]

            else:
                weights[d_idx] = 0

        indices = [i for i in range(len(weights)) if weights[i] != 0]
        return sorted(indices, key=lambda i: weights[i], reverse=True)

    def start_the_game(self):

        def depth_first_recursive_func(x_arr_idx,
                                       y_arr_idx,
                                       color_idx: int = 0,
                                       color_direction: int = None,
                                       last_color_direction: int = None):

            self.states.append(self.squares_arr.copy())

            if self.steps_number > 200000:
                return 0, 0

            color_id = self.sorted_colors_order[color_idx]

            directions = moves + [x_arr_idx, y_arr_idx]

            color_goal = self.colors_status[color_id]["end"]

            # if direction changed from (top or bottom) to (right or left) or the opposite
            check_direction_changed = (last_color_direction is not None and  # check not new color
                                       opposite_directions[last_color_direction] != color_direction and  # check direction form left to right or opposite :)
                                       last_color_direction != color_direction)  # check not same direction

            #  -------------------------------
            #  check if the color touch itself
            #  -------------------------------
            number_of_same_color_id_near_to_head = 0  # it must be 1
            for d_idx in range(4):  # check left right bottom left   d_idx --> direction_index
                direction = directions[d_idx]
                check_boundary = self.check_directions_boundaries[d_idx](y_arr_idx if d_idx < 2 else x_arr_idx)
                if (check_boundary and self.squares_arr[direction[0], direction[1]] == color_id
                        and not np.array_equal(direction, color_goal)):
                    number_of_same_color_id_near_to_head += 1
            if number_of_same_color_id_near_to_head > 1:
                return 1, None  #
            #  -------------------------------

            #  ---------------------------------------------------------------
            #  check empty wasted squares create by change the color direction
            #  ---------------------------------------------------------------
            if (check_direction_changed and
                    self.__check_wasted_squares(x_arr_idx, y_arr_idx, last_color_direction, color_direction, color_id)):
                return 1, None
            #  ---------------------------------------------------------------

            #  ----------------------------------
            #  check if the color touch it's goal
            #  ----------------------------------
            for d_idx in range(4):  # check left right bottom left   d_idx --> direction_index
                direction = directions[d_idx]
                if not np.array_equal(direction, color_goal):
                    continue

                if (d_idx != color_direction
                        and self.__check_wasted_squares(color_goal[0], color_goal[1], color_direction, d_idx, color_id)):
                    return 1, None

                self.__draw(x_arr_idx, y_arr_idx, color_id)
                color_idx += 1

                if color_idx == self.colors_num:
                    return 0, 1
                else:
                    color_id = self.sorted_colors_order[color_idx]

                    new_color_node = self.colors_status[color_id]["start"]

                    back_tracking, find_goal = depth_first_recursive_func(new_color_node[0], new_color_node[1], color_idx)

                    if find_goal is not None:
                        return 0, find_goal

                    if back_tracking:
                        color_idx -= 1
                        self.__clear()
                        return 1, None
            #  ----------------------------------

            # sort the next order by but weight into (nearest and little expands)
            next_order = self.__create_next_order(x_arr_idx, y_arr_idx, directions, color_goal)
            for d_idx in next_order:  # check left right bottom left   d_idx --> direction_index
                direction = directions[d_idx]

                self.__draw(direction[0], direction[1], color_id)
                back_tracking, find_goal = depth_first_recursive_func(direction[0], direction[1], color_idx,
                                                                      d_idx, color_direction)

                if find_goal is not None:
                    return 0, find_goal

                if back_tracking:
                    self.__clear()
            return 1, None

        first_color_id = self.sorted_colors_order[0]
        x1, y1 = self.colors_status[first_color_id]["start"]
        result = depth_first_recursive_func(x1, y1, 0)[1]

        if result is None:  # can't solve this game
            self.result_id = 2
        if result == 0:  # there are more steps than 200K
            self.result_id = 1
        if result == 1:  # ok i find the solution :)
            self.result_id = 0

        self.states.append(self.squares_arr.copy())
