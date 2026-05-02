import customtkinter as ctk

class Game(ctk.CTkFrame):

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
