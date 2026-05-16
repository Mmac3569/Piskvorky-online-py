from typing import TYPE_CHECKING
from random import choice

if TYPE_CHECKING:
    from frames.game_frame import GameFrame
    from data_manager import DataManager
    from networking import Networking

class Game:
    def __init__(self, frame :"GameFrame", data_manager :"DataManager", networking: "Networking" = None, online = False, begins = False, opponent_name = None):
        self.frame = frame
        self.dm = data_manager
        self.online = online

        self.X_SYMBOL = True
        self.O_SYMBOL = False
        self.player = self.X_SYMBOL

        self.moves =  dict()

        self.x_offset = 0
        self.y_offset = 0

        if self.online is True:
            self.can_move = begins
            self.network = networking
            self.opponent_name = opponent_name
            self.update_status_lbl()

        self.winner = None

    def eval_move(self, x, y, opponent_move = False):
        if self.winner != None:
            return
        elif self.online and not self.can_move and not opponent_move:
            return
        
        if opponent_move: #opponent sends real coords
            real_x = x; real_y = y
        else:
            real_x = x + self.x_offset
            real_y = y + self.y_offset

        if self.moves.get((real_x, real_y)) is None:
            current_player = self.player
            self.moves[(real_x, real_y)] = current_player

            if self.online:
                self.can_move = not self.can_move
                if opponent_move:
                    self.frame.draw_move(real_x, real_y, current_player, center=True)
                else:
                    self.network.send_move(real_x, real_y)

            if self.check_win(real_x, real_y):
                self.winner = current_player
                self.frame.end(self.symbol_str(current_player))
                if self.winner == self.X_SYMBOL:
                    self.dm.save_stats(wins=self.dm.wins + 1)
                elif self.winner == self.O_SYMBOL:
                    self.dm.save_stats(losses=self.dm.losses + 1)
                return self.symbol_str(current_player)
            #else:
            self.player = not self.player
            self.update_status_lbl()
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
        if self.winner == self.X_SYMBOL:
            self.dm.save_stats(wins=self.dm.wins + 1)
        elif self.winner == self.O_SYMBOL:
            self.dm.save_stats(losses=self.dm.losses + 1)

    def draw(self):
        if self.winner != None:
            return

        self.winner = "" # draw
        self.frame.end(None)
        self.dm.save_stats(draws=self.dm.draws + 1)

    def rematch(self):
        self.moves.clear()
        self.x_offset = 0
        self.y_offset = 0
        if self.winner != "":
            self.player = not self.winner
        else:
            self.player = choice([self.X_SYMBOL, self.O_SYMBOL])
        self.winner = None
        self.update_status_lbl()
        self.frame.redraw_board(self.moves)

    def move_board(self, keysym):
        if keysym == "w":
            self.y_offset -= 1
        elif keysym == "a":
            self.x_offset -= 1
        elif keysym == "s":
            self.y_offset += 1
        elif keysym == "d":
            self.x_offset += 1
        self.frame.redraw_board(self.moves)

    def center_board(self, x, y):
        # Posuň zobrazení tak, aby bylo pole (x, y) viditelné v 10x10 mřížce.
        # Cílová pozice se snaží být v centru zobrazení.
        target_grid_x = 4
        target_grid_y = 4

        self.x_offset = x - target_grid_x
        self.y_offset = y - target_grid_y

        # Pokud by cílová buňka byla mimo viditelnou oblast, uzamkneme ji do rozsahu 0..9.
        if x - self.x_offset < 0:
            self.x_offset = x
        elif x - self.x_offset > 9:
            self.x_offset = x - 9

        if y - self.y_offset < 0:
            self.y_offset = y
        elif y - self.y_offset > 9:
            self.y_offset = y - 9

        self.frame.redraw_board(self.moves)

    def symbol_str(self, symbol_bool):
        if symbol_bool is self.X_SYMBOL:
            return "X"
        elif symbol_bool is self.O_SYMBOL:
            return "O"
        #else:
        return None
    
    def update_status_lbl(self, text = None):
        if text is None and self.online is False:
            text = f"{self.symbol_str(self.player)} je na tahu!"
        elif text is None and self.online is True:
            text = "Jsi na tahu!" if self.can_move else f"{self.opponent_name} je na tahu!"
        self.frame.status_label.configure(text = text)