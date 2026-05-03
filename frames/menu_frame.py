from PIL import Image
import customtkinter as ctk
import game

class MenuFrame(ctk.CTkFrame):

    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        #self.master = master
        self.menu_title = ctk.CTkLabel(self, text = "Piškvorky", font = ctk.CTkFont("Arial", 100))
        self.menu_title.pack(pady = 50)

        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.pack(side = "left", fill = "both", expand = True)
        
        self.picture = ctk.CTkImage(Image.open("./blank-profile-picture.png"), Image.open("./blank-profile-picture.png"), (100, 100))
        self.profile_picture = ctk.CTkLabel(self.left_frame, image=self.picture, text=None)
        self.profile_picture.pack(pady = 10)

        self.username_lbl = ctk.CTkLabel(self.left_frame, text = "Username")
        self.username_lbl.pack()

        self.view_profile_bt = ctk.CTkButton(self.left_frame, text = "Zobrazit profil", command=self.view_profile_bt_click)
        self.view_profile_bt.pack(pady = 10)

        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.pack(side = "left", fill = "both", expand = True)

        self.play_offline_bt = ctk.CTkButton(self.right_frame, text = "Hrát offline", command=lambda: self.play_bt_click(online=False), width=200)
        self.play_offline_bt.pack(pady = 5, padx = 20)

        self.play_online_bt = ctk.CTkButton(self.right_frame, text = "Hrát online", command=lambda: self.play_bt_click(online=True), width=200)
        self.play_online_bt.pack(pady = 5, padx = 20)

    def play_bt_click(self, online = False):
        if online:
            print("Online play not implemented yet.")
            self.master.game = game.Game(online=True)
        else:
            self.master.switch_frame(self.master.game_frame)
            self.master.game = game.Game(self.master.game_frame, online=False)

    def view_profile_bt_click(self):
        self.master.switch_frame(self.master.profile_frame)