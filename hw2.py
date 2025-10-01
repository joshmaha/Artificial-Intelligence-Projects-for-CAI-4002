import random
from typing import List, Tuple, Optional
from tdTTT import TicTacToe3D

def alpha_beta_search(game: TicTacToe3D, depth: int, alpha: float, beta: float, maximizing_player: bool, player: str) -> Tuple[int, Tuple[int, int, int]]:

    legal_moves = game.get_legal_moves()
    # base case if max depth, no legal moves left or winner is found
    if depth == 0 or not legal_moves or game.check_winner():
        heuristic_value = heuristic_1(game, player) if maximizing_player else heuristic_2(game, player)
        return heuristic_value, (-1, -1, -1)  # Return a dummy move since no move is made

    best_move = legal_moves[0] if legal_moves else (-1, -1, -1)  # use first legal move or dummy if none

    if maximizing_player:
        max_eval = float('-inf')  # worst possible score for max
        for move in legal_moves[:min(5, len(legal_moves))]:  # forward pruning (limit branches)
            x, y, z = move
            game.make_move(x, y, z)
            #print(f"Player {player} Move: {move}")

            eval_score, _ = alpha_beta_search(game, depth - 1, alpha, beta, False, player)  # ignore move
            game.board[z][y][x] = None  # undo move
            #print(f"Move {move} Score: {eval_score}")

            # update best move and score
            if eval_score > max_eval:
                max_eval, best_move = eval_score, move
                #print(f"New best move: {best_move} Score: {max_eval}")

            alpha = max(alpha, eval_score)  # Update alpha
            if beta <= alpha:
                #print(f"pruning beta {beta} <= alpha {alpha}\n")
                break # prune tree
        return max_eval, best_move

    else:  # min player
        min_eval = float('inf')  # min player worst score possible
        for move in legal_moves[:min(5, len(legal_moves))]: 
            x, y, z = move
            game.make_move(x, y, z)
            #print(f"Player {player} -> Move: {move}")

            eval_score, _ = alpha_beta_search(game, depth - 1, alpha, beta, True, player)  # Ignore move
            game.board[z][y][x] = None  # Undo move
            #print(f"Move {move} Score: {eval_score}")

            # Update best move and score
            if eval_score < min_eval:
                min_eval, best_move = eval_score, move
                #print(f"New best move: {best_move} Score: {max_eval}")

            beta = min(beta, eval_score)  # Update beta
            if beta <= alpha:
                #print(f"pruning beta {beta} <= alpha {alpha}\n")
                break
        return min_eval, best_move

# prioritize moves that extend an existing line of this player's pieces
def heuristic_1(game: TicTacToe3D, player: str) -> int:

    score = 0
    opponent = 'O' if player == 'X' else 'X'  # get player vs opponent

    #print(f"\nEvaluating heuristic for player {player}:")
    
    for move in game.get_legal_moves():
        x, y, z = move
        game.board[z][y][x] = player  # temporarily place piece
        move_score = 0

        # if move results in win
        if game.check_winner() == player:
            move_score += 1000  # win immediately
        
        # count how many lines this move extends
        for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1),  # Axes
                           (1, 1, 0), (1, 0, 1), (0, 1, 1),  # Face diagonals
                           (1, 1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1), (1, -1, -1)]:  # Space diagonals
            count = 1  # player pieces in this direction

            # extend forward
            for step in range(1, 5):  # 5 is max in a row
                nx, ny, nz = x + step * dx, y + step * dy, z + step * dz
                if 0 <= nx < game.size and 0 <= ny < game.size and 0 <= nz < game.size and game.board[nz][ny][nx] == player:
                    count += 1
                else:
                    break

            # extend backward
            for step in range(1, 5):
                nx, ny, nz = x - step * dx, y - step * dy, z - step * dz
                if 0 <= nx < game.size and 0 <= ny < game.size and 0 <= nz < game.size and game.board[nz][ny][nx] == player:
                    count += 1
                else:
                    break

            # scores based on line length
            if count == 2:
                move_score += 10  # 2 in a row
            elif count == 3:
                move_score += 50  
            elif count == 4:
                move_score += 200  
            elif count >= 5:
                move_score += 1000  # 5 in a row/winning move

        # Undo move after evaluation
        game.board[z][y][x] = None

        #print(f"Move: {move} Score: {move_score}")
        score += move_score  # get total score
    
    #print(f"total heuristic score for Player {player}: {score}")
    return score


    
# prioritizes moves that blocks opponent
def heuristic_2(game: TicTacToe3D, player: str) -> int:

    opponent = 'X' if player == 'O' else 'O'
    return heuristic_1(game, player) - heuristic_1(game, opponent)


def play_game(ai1_heuristic, ai2_heuristic):

    try:
        game = TicTacToe3D(size=5)
        ai1, ai2 = 'X', 'O'
        max_moves = 5 * 5 * 5  # max possible moves in 5x5x5 game
        move_count = 0

        while not game.winner and move_count < max_moves:
            move_count += 1
            
            # get legal moves before searching for next move
            legal_moves = game.get_legal_moves()
            if not legal_moves:
                return None  # draw 
            
            # current player's symbol
            current_player = ai1 if game.current_player == 0 else ai2
            
            try:
                # get best move using alpha beta search
                eval_score, move = alpha_beta_search(game, 3, float('-inf'), float('inf'), game.current_player == 0, current_player)
                
                # skip invalid moves
                if move == (-1, -1, -1) or move not in legal_moves:
                    print(f"Warning: Invalid move detected ({move}). Selecting random legal move instead.")
                    move = random.choice(legal_moves)
                
                # complete the move found from the alpha beta search
                game.make_move(*move)
                
                # check if winner exists after move
                if game.check_winner():
                    return game.winner
                    
            except Exception as e:
                print(f"Error during move selection: {e}")
                # random move instead of stopping the game
                try:
                    random_move = random.choice(legal_moves)
                    game.make_move(*random_move)
                    print(f"Falling back to random move: {random_move}")
                except Exception as random_move_error:
                    print(f"Even random move failed: {random_move_error}")
                    return None  # quit this game
        
        #return game.winner or None  # return winner/none to indicate a draw
        
    except Exception as e:
        print(f"Game error: {e}")
        return None  # error with game


def run_simulation(num_games=100):
    
    ai1_wins, ai2_wins, draws, errors = 0, 0, 0, 0
    for i in range(num_games):
        try:
            print(f"Game {i+1}/{num_games}...")
            winner = play_game(heuristic_1, heuristic_2)
            
            if winner == 'X':
                ai1_wins += 1
                print(f"Game {i+1}: AI 1 (X) wins")
            elif winner == 'O':
                ai2_wins += 1
                print(f"Game {i+1}: AI 2 (O) wins")
            elif winner is None:
                draws += 1
                print(f"Game {i+1}: Draw or error")
            else:
                print(f"Game {i+1}: Unexpected result: {winner}")
                errors += 1
                
        except Exception as e:
            print(f"Error in game {i+1}: {e}")
            errors += 1
    
    # final stats
    print("\n Final Results")
    print(f"Total Games: {num_games}")
    print(f"AI 1 (X) Wins: {ai1_wins}")
    print(f"AI 2 (O) Wins: {ai2_wins}")
    print(f"Draws: {draws}")
    print(f"Errors/Incomplete games: {errors}")

# main
if __name__ == "__main__":
    run_simulation(1)

[?2004l
Starting Games: 100 games on a 5x5x5 board
Max depth: 2 and forward pruning: 0.3
Line-extension heuristic (X) vs. Random heuristic (O)
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: X is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
Game Over: O is the winner!
