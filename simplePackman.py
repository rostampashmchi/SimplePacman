import random
class PacManGameBoard:
    def __init__(self, board, pacman=None, ghosts=None):
        self.board = board
        self.size = len(board)
        self.score = 0
        self.dots = self.count_dots()

        if pacman is None:
            self.pacman = self.find_entity('P')
        else:
            self.pacman = pacman

        if ghosts is None:
            self.ghosts = self.find_entities('G')
        else:
            self.ghosts = ghosts

    def count_dots(self):
        return sum(row.count(10) for row in self.board)

    def find_entity(self, entity):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == entity:
                    return (i, j)
        return None

    def find_entities(self, entity):
        entities = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == entity:
                    entities.append((i, j))
        return entities


    def print_board(self):

        print(f'Score: {self.score}')
        print(f'Pac-Man Position: {self.pacman}')
        print(f'Ghost Positions: {self.ghosts}\n')
    def is_valid_move(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] != 'N'

    def get_possible_moves(self, entity):
        x, y = entity
        moves = [
            ((x + 1) % self.size, y),
            ((x - 1) % self.size, y),
            (x, (y + 1) % self.size),
            (x, (y - 1) % self.size),
        ]
        return [move for move in moves if self.is_valid_move(move)]

    def move_entity(self, entity, new_position):
        x, y = entity
        self.board[x][y] = 0 

        if entity == self.pacman and self.board[new_position[0]][new_position[1]] == 10:
            self.score += 10 
            self.dots -= 1  

        new_position = (new_position[0] % self.size, new_position[1] % self.size)  # Handle wrap-around movement

        if entity == self.pacman:
            self.pacman = new_position
        elif entity in self.ghosts:
            ghost_index = self.ghosts.index(entity)
            self.ghosts[ghost_index] = new_position

        self.board[new_position[0]][new_position[1]] = 'P' if entity == self.pacman else 'G'

    def is_game_over(self):
        if self.dots == 0  or any(ghost == self.pacman for ghost in self.ghosts):
            return True
        else:
            return False
def minimax(game, depth, alpha, beta, maximizing_player):
    if depth == 0 or game.is_game_over():
        return evaluate_board(game)
    if maximizing_player:
        max_eval = float('-inf')
        for move in game.get_possible_moves(game.pacman):
            game.move_entity(game.pacman, move)
            eval = minimax(game, depth - 1, alpha, beta, False)
            game.move_entity(game.pacman, move)  # Undo the move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for ghost in game.ghosts:
            for move in game.get_possible_moves(ghost):
                game.move_entity(ghost, move)
                eval = minimax(game, depth - 1, alpha, beta, True)
                game.move_entity(ghost, move) 
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def evaluate_board(game):
    if game.is_game_over():
        return -1 if any(entity == game.pacman for entity in game.ghosts) else 1
    return 0
def main():
    game_board = PacManGameBoard([
    [10, 10, 10, 10, 'N', 10, 10, 10, 10, 10, 10, 10, 10, 'N', 10, 10, 10, 10],
    [10, 'N', 'N', 10, 'N', 10, 'N', 'N', 'N', 'N', 'N', 'N', 10, 'N', 10, 'N', 'N', 10],
    [10, 'N', 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 'N', 10],
    [10, 'N', 10, 'N', 'N', 10, 'N', 'N', 0, 0, 'N', 'N', 10, 'N', 'N', 10, 'N', 10],
    [10, 10, 10, 10, 10, 10, 'N', 'G', 0, 0, 'G', 'N', 10, 10, 10, 10, 10, 10],
    [10, 'N', 10, 'N', 'N', 10, 'N', 'N', 'N', 'N', 'N', 'N', 10, 'N', 'N', 10, 'N', 10],
    [10, 'N', 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 'N', 10],
    [10, 'N', 'N', 10, 'N', 10, 'N', 'N', 'N', 'N', 'N', 'N', 10, 'N', 10, 'N', 'N', 10],
    [10, 10, 10, 10, 'N', 10, 10, 10, 'P', 10, 10, 10, 10, 'N', 10, 10, 10, 10],
    ], ghosts=[(4, 7), (4, 8)])  # Add a second ghost at (4, 8)


    while not game_board.is_game_over():
        game_board.print_board()

        # Use minimax for Pac-Man's move
        pacman_moves = game_board.get_possible_moves(game_board.pacman)
        best_move = None
        best_eval = float('-inf')

        for move in pacman_moves:
            game_board.move_entity(game_board.pacman, move)
            eval = minimax(game_board, 3, float('-inf'), float('inf'), False)
            game_board.move_entity(game_board.pacman, move)  # Undo the move

            if eval > best_eval:
                best_eval = eval
                best_move = move

        game_board.move_entity(game_board.pacman, best_move)

        # Use random move for ghost's move
        for ghost in game_board.ghosts:
            ghost_moves = game_board.get_possible_moves(ghost)
            random_ghost_move = random.choice(ghost_moves)
            game_board.move_entity(ghost, random_ghost_move)

    game_board.print_board()
    print("Game over!")

if __name__ == "__main__":
    main()
