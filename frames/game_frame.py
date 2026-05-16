import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game

class GameFrame(ctk.CTkFrame):

    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.top_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.top_panel.pack(padx = 10, pady = 10)

        self.status_label = ctk.CTkLabel(self.top_panel, text = "X je na tahu!", width=300)
        self.status_label.pack(side = "left", expand = True, fill = "x", padx = 10)

        self.draw_bt = ctk.CTkButton(self.top_panel, text = "Remíza", command=self.draw_bt_click)
        self.draw_bt.pack(side = "left", padx = 5)

        self.resign_bt = ctk.CTkButton(self.top_panel, text = "Vzdát se", command=self.resign_bt_click)
        self.resign_bt.pack(side = "left", padx = 5)

        self.board_frame = ctk.CTkFrame(self, fg_color="gray", width=540, height=540)
        self.board_frame.pack(padx = 10, pady = 10)

        self.game: "Game" = None
        self.buttons = []
        self.used_buttons = set()
        self.win_positions = None

        self.create_grid()

    def create_grid(self):
        for i in range(10): #creates columns
            button_column = []
            for j in range(10): #creates rows
                button = ctk.CTkButton(self.board_frame, text = "", font=ctk.CTkFont(size=20), width=50, height=50, corner_radius=0, command=lambda x=i, y=j: self.board_button_click(x, y))
                button.grid(row=j, column=i, padx=2, pady=2)
                button_column.append(button)
            self.buttons.append(button_column)

    def board_button_click(self, x, y):
        symbol = self.game.eval_move(x, y)
        if symbol != None:
            self.buttons[x][y].configure(text = symbol)
            self.used_buttons.add((x, y))

    def resign_bt_click(self):
        if messagebox.askyesno("Vzdát se", "Opravdu chceš vzdát hru?"):
            self.game.resign()

    def draw_bt_click(self):
        if self.game.winner is None and messagebox.askyesno("Remíza", "Přijímáš remízu?"):
            self.game.draw()
        elif self.master.winner is not None:
            self.game.rematch()
            self.draw_bt.configure(text = "Remíza")
            self.resign_bt.configure(text = "Vzdát se", command=self.resign_bt_click)
            self.draw_win(color = ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.win_positions = None

    def end(self, symbol):
        if symbol is None:
            self.status_label.configure(text="Remíza!")
        else:
            self.status_label.configure(text=f"Vyhrál {symbol}!")
        self.master.data_manager.save_stats(games_played=self.master.data_manager.games_played + 1)
        self.draw_bt.configure(text = "Odveta")
        self.resign_bt.configure(text = "Zpět do menu", command=self.back_to_menu)

    def draw_win(self, color = "green"):
        if self.win_positions == None:
            return
        for x, y in self.win_positions:
            grid_x = x - self.game.x_offset
            grid_y = y - self.game.y_offset
            if 0 <= grid_x < 10 and 0 <= grid_y < 10:
                self.buttons[grid_x][grid_y].configure(fg_color=color)

    def draw_move(self, x, y, symbol, center = False):
        if symbol is None:
            return
        grid_x = x - self.game.x_offset
        grid_y = y - self.game.y_offset
        if 0 <= grid_x < 10 and 0 <= grid_y < 10:
            self.buttons[grid_x][grid_y].configure(text = self.game.symbol_str(symbol))
            self.used_buttons.add((grid_x, grid_y))
        elif center:
            self.game.center_board(x, y)
            pass
    
    def back_to_menu(self):
        self.master.switch_frame(self.master.menu_frame)
        self.master.unbind("<KeyPress>")
        self.draw_bt.configure(text = "Remíza")
        self.resign_bt.configure(text = "Vzdát se", command=self.resign_bt_click)
        for x, y in self.used_buttons:
            self.buttons[x][y].configure(text = "")
        self.draw_win(color = ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.win_positions = None
        self.used_buttons.clear()
        self.status_label.configure(text = "X je na tahu!")

    def redraw_board(self, moves):
        for x, y in self.used_buttons:
            self.buttons[x][y].configure(text = "", fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.used_buttons.clear()
        for (x, y), symbol in moves.items():
            self.draw_move(x, y, symbol)
        self.draw_win()
    
    def refresh(self):
        self.master.bind("<KeyPress>", lambda event: self.game.move_board(event.keysym))
        
