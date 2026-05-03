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

        if self.moves.get((real_x, real_y)) == None:
            print(f"Move at ({real_x}, {real_y}) is valid.")
            self.moves[(real_x, real_y)] = self.player
            self.player = not self.player
            self.upadte_status_lbl()
            return self.symbol_str(not self.player) #player variable is being changed before because of return
    
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