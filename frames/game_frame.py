import customtkinter as ctk

class GameFrame(ctk.CTkFrame):

    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.top_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.top_panel.pack(padx = 10, pady = 10)

        self.status_label = ctk.CTkLabel(self.top_panel, text = "Jsi na tahu!", width=300)
        self.status_label.pack(side = "left", expand = True, fill = "x", padx = 10)

        self.draw_bt = ctk.CTkButton(self.top_panel, text = "Remíza")
        self.draw_bt.pack(side = "left", padx = 5)

        self.resign_bt = ctk.CTkButton(self.top_panel, text = "Vzdát se")
        self.resign_bt.pack(side = "left", padx = 5)

        self.board_frame = ctk.CTkFrame(self, fg_color="gray", width=540, height=540)
        self.board_frame.pack(padx = 10, pady = 10)

        self.buttons = []
        self.create_grid()

    def create_grid(self):
        for i in range(10): #creates columns
            button_column = []
            for j in range(10): #creates rows
                button = ctk.CTkButton(self.board_frame, text = f"", width=50, height=50, command=lambda x=i, y=j: self.board_button_click(x, y))
                button.grid(row=j, column=i, padx=2, pady=2)
                button_column.append(button)
            self.buttons.append(button_column)

    def board_button_click(self, x, y):
        print(f"Button at ({x}, {y}) clicked.")
        symbol = self.master.game.eval_move(x, y)
        if symbol != None:
            self.buttons[x][y].configure(text = symbol)

    def win(self, symbol):
        self.status_label.configure(text=f"Vyhrál {symbol}!")
        self.draw_bt.pack_forget()
        self.resign_bt.configure(text = "Zpět do menu", command=self.back_to_menu)
    
    def back_to_menu(self):
        self.master.switch_frame(self.master.menu_frame)
        self.draw_bt.pack(side = "left", padx = 5, after = self.status_label)
        self.resign_bt.configure(text = "Vzdát se", command=lambda: self.master.game.resign())
        for i in range(10):
            for j in range(10):
                self.buttons[i][j].configure(text = "")
        self.status_label.configure(text = "Jsi na tahu!")
        
