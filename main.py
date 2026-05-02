import customtkinter as ctk
import menu
import game
import profile

class Main(ctk.CTk):

    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.geometry("600x500")
        self.title("Piškvorky")

        self.menu_frame = menu.Menu(self, fg_color="transparent")
        self.menu_frame.pack(fill = "both", expand = True)
        self.active_frame = self.menu_frame

        self.game_frame = game.Game(self, fg_color="transparent")

        self.profile_frame = profile.Profile(self, fg_color="transparent")

    def switch_frame(self, new_frame: ctk.CTkFrame):
        self.active_frame.pack_forget()
        new_frame.pack(fill = "both", expand = True)

app = Main()
app.mainloop()