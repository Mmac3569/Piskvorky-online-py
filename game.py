from frames.game_frame import GameFrame

class Game:
    def __init__(self, frame :GameFrame, online = False):
        self.frame = frame
        self.online = online

        self.X_SYMBOL = True
        self.O_SYMBOL = False

        self.moves =  dict()

        self.x_offset = 0
        self.y_offset = 0
        
        if self.online is False:
            self.player = self.X_SYMBOL

    def eval_move(self, x, y):
        real_x = x + self.x_offset
        real_y = y + self.y_offset

        if self.moves.get((real_x, real_y)) is None:
            print(f"Move at ({real_x}, {real_y}) is valid.")
            current_player = self.player
            self.moves[(real_x, real_y)] = current_player

            if self.check_win(real_x, real_y):
                self.frame.status_label.configure(text=f"Vyhrál {self.symbol_str(current_player)}!")
                return self.symbol_str(current_player)

            self.player = not self.player
            self.upadte_status_lbl()
            return self.symbol_str(current_player)

    def check_win(self, x, y):
        symbol = self.moves.get((x, y))
        if symbol is None:
            return False

        win_length = 5
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)] # horizontal, vertical, diagonal down-right, diagonal up-right

        for dx, dy in directions:
            count = 1
            for step in (1, -1): # check in both directions (positive and negative)
                nx, ny = x + dx * step, y + dy * step # offset from the last move in the current direction
                while self.moves.get((nx, ny)) == symbol:
                    count += 1
                    nx += dx * step # move further in the same direction
                    ny += dy * step # move further in the same direction
            if count >= win_length:
                return True

        return False

    def symbol_str(self, symbol_bool):
        if symbol_bool is self.X_SYMBOL:
            return "X"
        elif symbol_bool is self.O_SYMBOL:
            return "O"
        #else:
        return None
    
    def upadte_status_lbl(self):
        if self.player is self.X_SYMBOL:
            self.frame.status_label.configure(text = "Jsi na tahu!")
        elif self.player is self.O_SYMBOL:
            self.frame.status_label.configure(text = "2. hráč na tahu!")