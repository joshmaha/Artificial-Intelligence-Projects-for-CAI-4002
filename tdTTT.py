from typing import List, Tuple, Optional

class TicTacToe3D:
    def __init__(self, size: int = 3):
        """Initialize the 3D Tic Tac Toe board."""
        if not isinstance(size, int) or not (1 <= size <= 5):
            raise ValueError("Board size must be an integer between 1 and 5.")
        self.size: int = size
        self.board: List[List[List[Optional[str]]]] = [[[None for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.players: List[str] = ['X', 'O']
        self.current_player: int = 0
        self.winner: Optional[str] = None

    def display_board(self) -> None:
        """Print the board in a readable format."""
        for z, layer in enumerate(self.board):
            print(f"Layer {z}:")
            for row in layer:
                print(" ".join(cell if cell is not None else '.' for cell in row))
            print()

    def __str__(self) -> str:
        """Override the print() function to call display_board."""
        from io import StringIO
        output = StringIO()
        for z, layer in enumerate(self.board):
            output.write(f"Layer {z}:\n")
            for row in layer:
                output.write(" ".join(cell if cell is not None else '.' for cell in row) + "\n")
            output.write("\n")
        return output.getvalue()

    def get_legal_moves(self) -> List[Tuple[int, int, int]]:
        """Return a list of all legal moves as (x, y, z)."""
        moves: List[Tuple[int, int, int]] = []
        for z in range(self.size):
            for y in range(self.size):
                for x in range(self.size):
                    if self.board[z][y][x] is None:
                        moves.append((x, y, z))
        return moves

    def make_move(self, x: int, y: int, z: int) -> None:
        """Make a move for the current player at position (x, y, z)."""
        if not all(isinstance(i, int) for i in (x, y, z)):
            raise TypeError("Coordinates must be integers.")
        if self.winner is not None:
            raise ValueError("Game over. No more moves allowed.")
        if not (0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size):
            raise ValueError("Invalid move: Position out of bounds.")
        if self.board[z][y][x] is not None:
            raise ValueError("Invalid move: Position already taken.")

        self.board[z][y][x] = self.players[self.current_player]
        if self.check_winner():
            self.winner = self.players[self.current_player]
            print("Game Over:", self.check_winner(), "is the winner!")
        self.current_player = 1 - self.current_player

    def check_winner(self) -> Optional[str]:
        """Check if there is a winner or if the game is a draw."""
        for player in self.players:
            # Check all possible lines in the 3D grid
            for x in range(self.size):
                for y in range(self.size):
                    for z in range(self.size):
                        if self._check_lines(player, x, y, z):
                            return player

        if not self.get_legal_moves():
            self.winner = "Draw"
            return "Draw"

        return None

    def _check_lines(self, player: str, x: int, y: int, z: int) -> bool:
        """Check all lines passing through a given cell for a win."""
        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),  # Axes
            (1, 1, 0), (1, 0, 1), (0, 1, 1),  # Face diagonals
            (1, 1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1), (1, -1, -1)  # Space diagonals
        ]

        for dx, dy, dz in directions:
            if self._check_line(player, x, y, z, dx, dy, dz):
                return True
        return False

    def _check_line(self, player: str, x: int, y: int, z: int, dx: int, dy: int, dz: int) -> bool:
        """Check a specific line for a win."""
        count: int = 0
        for step in range(self.size):
            nx, ny, nz = x + step * dx, y + step * dy, z + step * dz
            if 0 <= nx < self.size and 0 <= ny < self.size and 0 <= nz < self.size:
                if self.board[nz][ny][nx] == player:
                    count += 1
                else:
                    break
            else:
                break

        return count == self.size

    def check_current_turn(self) -> Optional[str]:
        """Return the current player's turn, or None if the game is over."""
        if self.winner is not None:
            return None
        return self.players[self.current_player]

# Example usage
if __name__ == "__main__":
    game = TicTacToe3D(size=3)
    print(game)

    print("Current turn:", game.check_current_turn())
    game.make_move(0, 0, 0)
    print("Current turn:", game.check_current_turn())
    print(game)

    print("Legal moves:", game.get_legal_moves())
    print("Winner:", game.check_winner())
