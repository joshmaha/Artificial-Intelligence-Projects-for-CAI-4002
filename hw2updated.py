import random # used for heuristic 2
from copy import deepcopy # used to make a copy of the board instead of constantly rewriting the actual game board
from typing import List, Tuple
from tdTTT import TicTacToe3D

class playerAI: # initialize AI players
    def __init__(self, game: TicTacToe3D, player: str, heuristic: str = 'line', max_depth: int = 3, fw_prune: float = 0.3): 
        self.game = game # game instance
        self.player = player # AI player symbol ('X' or 'O')
        self.opponent = 'O' if player == 'X' else 'X'
        self.max_depth = max_depth # max search depth
        self.fw_prune = fw_prune # % of moves to consider
        self.heuristic = heuristic
        self.nodes_evaluated = 0 # nodes checked so far in pruning process
        
    def get_move(self) -> Tuple[int, int, int]: # get best move using alpha-beta search with forward pruning
        self.nodes_evaluated = 0
        best_score = float('-inf')  # set best score, alpha and beta to worst possible max/min value
        best_move = None
        alpha = float('-inf') 
        beta = float('inf')
        
        legal_moves = self.game.get_legal_moves()  # get all legal moves
        pruned_moves = self.prune_moves(legal_moves) # use forward pruning to keep only a percentage of the moves
        
        for move in pruned_moves:
            game_copy = deepcopy(self.game) # use deep to make a copy of the game to simulate moves
            x, y, z = move
            game_copy.make_move(x, y, z) # apply move to copy of board 
            
            score = self.minimax(game_copy, self.max_depth - 1, alpha, beta, False) # opponent turn, so we minimize their score            
            if score > best_score:
                best_score = score
                best_move = move           
            alpha = max(alpha, best_score)       
        return best_move
    
    def prune_moves(self, moves: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]: # use forward pruning to evaluate less than all legal moves
        if self.fw_prune >= 1.0: # pruning value to high
            return moves
               
        if self.heuristic == 'line': # use line heuristic 
            scored_moves = [(move, self.line_extension_score(move)) for move in moves] # call line extension method to apply this heuristic
            scored_moves.sort(key=lambda x: x[1], reverse=True)
        else:  # use random heuristic
            scored_moves = [(move, random.random()) for move in moves] # get a random move from the list of moves
        
        # use only a percentage of the highest-scoring moves
        num_moves_to_keep = max(1, int(len(moves) * self.fw_prune))
        pruned_moves = [move for move, score in scored_moves[:num_moves_to_keep]]        
        return pruned_moves # return pruned moves
    
    def minimax(self, game: TicTacToe3D, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:  # minimax method     
        self.nodes_evaluated += 1      
        winner = game.check_winner()# check if game is over or max depth reached
        if winner == self.player:
            return 1000 + depth  # win score is higher if found earlier
        elif winner == self.opponent:
            return -1000 - depth  # lose score is lower if found earlier
        elif winner == "Draw":
            return 0
        elif depth == 0: # at leaf nodes, apply given heuristic
            if self.heuristic == 'line': 
                return self.evaluate_board(game)
            else:  
                return random.uniform(-1, 1)
        
        legal_moves = game.get_legal_moves()
        pruned_moves = self.prune_moves(legal_moves)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in pruned_moves:
                game_copy = deepcopy(game)
                x, y, z = move
                game_copy.make_move(x, y, z)
                eval = self.minimax(game_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: # always take highest value for alpha
                    break  # beta cutoff
            return max_eval # best move based on heuristic value
        else: # minimizing
            min_eval = float('inf')
            for move in pruned_moves:
                game_copy = deepcopy(game)
                x, y, z = move
                game_copy.make_move(x, y, z)
                eval = self.minimax(game_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)  # always take lowest value for beta
                if beta <= alpha:
                    break  # alpha cutoff
            return min_eval # best move based on heuristic value
    
    def line_extension_score(self, move: Tuple[int, int, int]) -> float: # evaluate how well a move extends existing lines of player's pieces.
    
        game_copy = deepcopy(self.game)
        x, y, z = move
        game_copy.board[z][y][x] = self.player
        
        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),  # Axes
            (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1),  # Face diagonals
            (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)  # Space diagonals
        ]        
        score = 0
        size = game_copy.size       
        for dx, dy, dz in directions: # check both directions
            line_score = 0
            player_count = 0           
            for step in range(-(size-1), size):
                nx, ny, nz = x + step * dx, y + step * dy, z + step * dz
                if 0 <= nx < size and 0 <= ny < size and 0 <= nz < size:
                    cell = game_copy.board[nz][ny][nx]
                    if cell == self.player:
                        player_count += 1
                        # give higher score for consecutive pieces
                        if step != 0:  # don't count this move twice
                            line_score += player_count
            
            score += line_score        
        return score
    
    def evaluate_board(self, game: TicTacToe3D) -> float: # evaluate current board state using the line extension heuristic.
        
        score = 0
        size = game.size      
        # check all possible lines
        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),  # Axes
            (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1),  # Face diagonals
            (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)  # Space diagonals
        ]
        
        for z in range(size):
            for y in range(size):
                for x in range(size):
                    for dx, dy, dz in directions:
                        player_count = 0
                        opponent_count = 0
                        empty_count = 0
                        valid_line = True # assume line is valid                   
                        for step in range(size): # gather info on all cell positions in this direction, both empty and used spots 
                            nx, ny, nz = x + step * dx, y + step * dy, z + step * dz
                            if 0 <= nx < size and 0 <= ny < size and 0 <= nz < size:
                                cell = game.board[nz][ny][nx]
                                if cell == self.player:
                                    player_count += 1
                                elif cell == self.opponent:
                                    opponent_count += 1
                                else:
                                    empty_count += 1
                            else:
                                valid_line = False # line is invalid if any part of the line is out of bounds
                                break
                        
                        if valid_line:# score this line
                            if opponent_count == 0: # line with only our pieces and empty spaces
                                if player_count > 0:
                                    score += 10 ** player_count
                            elif player_count == 0: #line with only opponent pieces and empty spaces
                                if opponent_count > 0:
                                    score -= 10 ** opponent_count       
        return score

def run_game(size: int = 5, max_depth: int = 3, fw_prune: float = 0.5) -> str: # run 1 game at a time
    
    game = TicTacToe3D(size)
    line_ai = playerAI(game, 'X', heuristic='line', max_depth=max_depth, fw_prune=fw_prune) # player 1
    random_ai = playerAI(game, 'O', heuristic='random', max_depth=max_depth, fw_prune=fw_prune) # player 2
    
    while game.winner is None: # game is over only when winner is declared
        current_player = game.check_current_turn() # check which player's turn
        if current_player == 'X':
            move = line_ai.get_move()
        else:
            move = random_ai.get_move()
        
        if move: # move is legal
            x, y, z = move
            game.make_move(x, y, z) # make move
    return game.winner

def full_sim(num_games: int = 100, size: int = 5, max_depth: int = 3, fw_prune: float = 0.5) -> None: # simulate 100 games and print results
    
    results = {'X': 0, 'O': 0, 'Draw': 0} # store results for final output
    print(f"Starting Games: {num_games} games on a {size}x{size}x{size} board")
    print(f"Max depth: {max_depth} and forward pruning: {fw_prune}")
    print("Line-extension heuristic (X) vs. Random heuristic (O)")
    
    for i in range(num_games):# each player gets to go first half the time
        if i % 2 == 0: # line heuristic plays first
            game = TicTacToe3D(size=size)
            line_ai = playerAI(game, 'X', heuristic='line', max_depth=max_depth, fw_prune=fw_prune)
            random_ai = playerAI(game, 'O', heuristic='random', max_depth=max_depth, fw_prune=fw_prune)
        else: # random heuristic first
            game = TicTacToe3D(size=size)
            random_ai = playerAI(game, 'X', heuristic='random', max_depth=max_depth, fw_prune=fw_prune)
            line_ai = playerAI(game, 'O', heuristic='line', max_depth=max_depth, fw_prune=fw_prune)
        
        while game.winner is None:
            current_player = game.check_current_turn()
            ai = line_ai if current_player == line_ai.player else random_ai 
            move = ai.get_move()           
            if move:
                x, y, z = move
                game.make_move(x, y, z)
        
        if game.winner == 'Draw': # tally results
            results['Draw'] += 1
        elif (i % 2 == 0 and game.winner == 'X') or (i % 2 == 1 and game.winner == 'O'):
            results['X'] += 1  # line heuristic won
        else:
            results['O'] += 1  # random heuristic won
    
    print("Results:") #print results
    print(f"Games played: {num_games}")
    print(f"Line heuristic wins: {results['X']} ({results['X']/num_games*100:.1f}%)")
    print(f"Random heuristic wins: {results['O']} ({results['O']/num_games*100:.1f}%)")
    print(f"Draws: {results['Draw']} ({results['Draw']/num_games*100:.1f}%)")

if __name__ == "__main__":
    full_sim(100, 5, 2, 0.3)