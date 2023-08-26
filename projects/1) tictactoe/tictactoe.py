"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == O:
                count_o += 1
            if board[i][j] == X:
                count_x += 1

    if count_x > count_o:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = list()

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                actions_set.append([i, j])

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception

    board_copy = [row_list.copy() for row_list in board]
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    def has_win(player_name):
        for i in board:
            if i == [player_name] * 3:
                return True

        for i in range(len(board[0])):
            if [board[0][i], board[1][i], board[2][i]] == [player_name] * 3:
                return True

        if [board[0][0], board[1][1], board[2][2]] == [player_name] * 3:
            return True

        if [board[0][2], board[1][1], board[2][0]] == [player_name] * 3:
            return True

        return False

    if has_win(X):
        return X
    if has_win(O):
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    count_empty = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                count_empty += 1

    # for i in board:
    #     count_empty = i.count(EMPTY)

    if count_empty == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def mini_max(board, action):
    result_board = result(board, action) if action is not None else board

    if terminal(result_board):
        return None, utility(result_board)

    act = actions(result_board)
    values: list = [mini_max(result_board, act[i])[1] for i in range(len(act))]

    if player(result_board) == X:
        return act[values.index(max(values))], max(values)
    if player(result_board) == O:
        return act[values.index(min(values))], min(values)


def mini_max_alpha_beta(board, action, alpha, beta):
    board = result(board, action) if action is not None else board

    if terminal(board):
        return None, utility(board)

    acts = actions(board)

    if player(board) == X:
        max_value = -1
        max_value_action = None
        for action in acts:
            value = mini_max_alpha_beta(board, action, alpha, beta)[1]
            if value > max_value:
                max_value = value
                max_value_action = action
            alpha = max(alpha, max_value)
            if beta <= alpha:
                break
        return max_value_action, max_value

    elif player(board) == O:
        min_value = +1
        min_value_action = None
        for action in acts:
            value = mini_max_alpha_beta(board, action, alpha, beta)[1]
            if value < min_value:
                min_value = value
                min_value_action = action
            beta = min(beta, min_value)
            if alpha >= beta:
                break
        return min_value_action, min_value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    act = actions(board)

    if len(act) == 1:
        return act[0]

    return mini_max_alpha_beta(board, None, -1, +1)[0]
