from frames.game_frame import GameFrame

class Game:
    def __init__(self, frame :GameFrame, data_manager, online = False):
        self.frame = frame
        self.data_manager = data_manager
        self.online = online

        self.X_SYMBOL = True
        self.O_SYMBOL = False

        self.moves =  dict()

        self.x_offset = 0
        self.y_offset = 0
        
        if self.online is False:
            self.player = self.X_SYMBOL

        self.winner = None

    def eval_move(self, x, y):
        if self.winner != None:
            return

        real_x = x + self.x_offset
        real_y = y + self.y_offset

        if self.moves.get((real_x, real_y)) is None:
            print(f"Move at ({real_x}, {real_y}) is valid.")
            current_player = self.player
            self.moves[(real_x, real_y)] = current_player

            if self.check_win(real_x, real_y):
                self.winner = current_player
                self.frame.end(self.symbol_str(current_player))
                if self.winner == self.X_SYMBOL:
                    self.data_manager.save_stats(wins=self.data_manager.load_stats()["wins"] + 1)
                elif self.winner == self.O_SYMBOL:
                    self.data_manager.save_stats(losses=self.data_manager.load_stats()["losses"] + 1)
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
            checked = set([(x, y)])
            for step in (1, -1): # check in both directions (positive and negative)
                nx, ny = x + dx * step, y + dy * step # offset from the last move in the current direction
                while self.moves.get((nx, ny)) == symbol:
                    count += 1
                    checked.add((nx, ny))
                    nx += dx * step # move further in the same direction
                    ny += dy * step # move further in the same direction
            if count >= win_length:
                self.frame.win_positions = checked
                self.frame.draw_win()
                return True

        return False
    
    def resign(self):
        if self.winner != None:
            return

        self.winner = not self.player
        self.frame.end(self.symbol_str(self.winner))
        self.data_manager.save_stats(losses=self.data_manager.load_stats()["losses"] + 1)

    def draw(self):
        if self.winner != None:
            return

        self.winner = 0 # draw
        self.frame.end(None)
        self.data_manager.save_stats(draws=self.data_manager.load_stats()["draws"] + 1)

    def move_board(self, keysym):
        if keysym == "w":
            self.y_offset -= 1
        elif keysym == "a":
            self.x_offset -= 1
        elif keysym == "s":
            self.y_offset += 1
        elif keysym == "d":
            self.x_offset += 1
        self.frame.redraw_board(self.moves, self.x_offset, self.y_offset)


    def symbol_str(self, symbol_bool):
        if symbol_bool is self.X_SYMBOL:
            return "X"
        elif symbol_bool is self.O_SYMBOL:
            return "O"
        #else:
        return None
    
    def upadte_status_lbl(self):
        self.frame.status_label.configure(text = f"{self.symbol_str(self.player)} je na tahu!")