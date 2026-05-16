import customtkinter as ctk
from frames import game_frame, menu_frame, profile_frame
from data_manager import DataManager

class Main(ctk.CTk):

    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.geometry("600x500")
        self.title("Piškvorky")

        self.data_manager = DataManager()
        self.networking = None

        self.menu_frame = menu_frame.MenuFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill = "both", expand = True)
        self.active_frame = self.menu_frame

        self.game_frame = game_frame.GameFrame(self, fg_color="transparent")

        self.profile_frame = profile_frame.ProfileFrame(self, self.data_manager, fg_color="transparent")

    def switch_frame(self, new_frame: ctk.CTkFrame):
        self.active_frame.pack_forget()
        new_frame.refresh()
        new_frame.pack(fill = "both", expand = True)
        self.active_frame = new_frame

app = Main()
app.mainloop()