class Game:
    def __init__(self):
        self.grid_size = 5
        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.players = ["A", "B"]
        self.current_player = self.players[0]
        self.pieces = {"P": 1, "H1": 2, "H2": 2}
        self.init_game()

    def init_game(self):
        # Initialize pieces on the board
        for i, player in enumerate(self.players):
            for j, piece in enumerate(["P1", "P2", "H1", "H2", "P3"]):
                if player == "A":
                    self.grid[0][j] = f"{player}-{piece}"
                else:
                    self.grid[self.grid_size-1][j] = f"{player}-{piece}"

    def print_board(self):
        for row in self.grid:
            print(row)
        print("\n")

    def get_piece_position(self, piece):
        for i, row in enumerate(self.grid):
            if piece in row:
                return i, row.index(piece)
        return None, None

    def is_valid_move(self, piece, direction):
        x, y = self.get_piece_position(piece)
        if x is None or y is None:
            return False
        
        if "P" in piece or "H1" in piece:
            if direction == "L" and y > 0:
                return True
            elif direction == "R" and y < self.grid_size - 1:
                return True
            elif direction == "F" and x > 0:
                return True
            elif direction == "B" and x < self.grid_size - 1:
                return True
        elif "H2" in piece:
            if direction == "FL" and x > 0 and y > 0:
                return True
            elif direction == "FR" and x > 0 and y < self.grid_size - 1:
                return True
            elif direction == "BL" and x < self.grid_size - 1 and y > 0:
                return True
            elif direction == "BR" and x < self.grid_size - 1 and y < self.grid_size - 1:
                return True
        
        return False

    def move_piece(self, piece, direction):
        if not self.is_valid_move(piece, direction):
            return False

        x, y = self.get_piece_position(piece)
        if direction == "L":
            self.grid[x][y-1], self.grid[x][y] = self.grid[x][y], ""
        elif direction == "R":
            self.grid[x][y+1], self.grid[x][y] = self.grid[x][y], ""
        elif direction == "F":
            self.grid[x-1][y], self.grid[x][y] = self.grid[x][y], ""
        elif direction == "B":
            self.grid[x+1][y], self.grid[x][y] = self.grid[x][y], ""
        elif direction == "FL":
            self.grid[x-1][y-1], self.grid[x][y] = self.grid[x][y], ""
        elif direction == "FR":
            self.grid[x-1][y+1], self.grid[x][y] = self.grid[x][y], ""
        elif direction == "BL":
            self.grid[x+1][y-1], self.grid[x][y] = self.grid[x][y], ""
        elif direction == "BR":
            self.grid[x+1][y+1], self.grid[x][y] = self.grid[x][y], ""

        self.switch_turns()
        return True

    def switch_turns(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def check_winner(self):
        player_a_pieces = sum([1 for row in self.grid for piece in row if piece.startswith("A-")])
        player_b_pieces = sum([1 for row in self.grid for piece in row if piece.startswith("B-")])

        if player_a_pieces == 0:
            return "B"
        elif player_b_pieces == 0:
            return "A"
        else:
            return None
