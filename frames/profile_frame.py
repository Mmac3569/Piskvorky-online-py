import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

class ProfileFrame(ctk.CTkFrame):

    def __init__(self, master, data_manager, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.dm = data_manager

        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.pack(pady = 0, side = "left", fill = "both", expand = True)

        self.back_bt = ctk.CTkButton(self.left_frame, text = "Zpět do menu", command=lambda: self.master.switch_frame(self.master.menu_frame))
        self.back_bt.pack(pady = 20)

        self.picture = ctk.CTkImage(self.dm.profile_picture, size = (100, 100))
        self.profile_picture_bt = ctk.CTkButton(self.left_frame, image=self.picture, text = None, corner_radius=0, width=110, height=110, command=self.select_image)
        self.profile_picture_bt.pack(pady = 10)

        self.username_lbl = ctk.CTkLabel(self.left_frame, text = "Uživatelské jméno:")
        self.username_lbl.pack(pady = 5)

        self.username = tk.StringVar(value=self.dm.username)
        self.username_entry = ctk.CTkEntry(self.left_frame, textvariable=self.username)
        self.username_entry.pack(pady = 10)
        self.username_entry.bind("<Return>", lambda event: self.dm.save_user_data(username=self.username.get()))

        self.stats_lbl = ctk.CTkLabel(self.left_frame, text = f"Odehrané hry: {self.dm.games_played}\nVýhry: {self.dm.wins}\nRemízy: {self.dm.draws}\nProhry: {self.dm.losses}")
        self.stats_lbl.pack(pady = 10)

        self.save_bt = ctk.CTkButton(self.left_frame, text = "Uložit změny", command=lambda: self.dm.save_user_data(username=self.username.get()))
        self.save_bt.pack(pady = 5)

        self.reset_bt = ctk.CTkButton(self.left_frame, text = "Resetovat profil", fg_color="red", hover_color="darkred", command=self.reset_stats)
        self.reset_bt.pack(pady = 5)

        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.pack(side = "left", fill = "both", expand = True)
        
        self.history_title = ctk.CTkLabel(self.right_frame, text = "Historie her")
        self.history_title.pack(pady = 10)

        self.history_frame = ctk.CTkScrollableFrame(self.right_frame)
        self.history_frame.pack(pady = 10, padx = 10, fill = "both", expand = True)

    def reset_stats(self):
        if messagebox.askyesno("Resetovat profil", "Opravdu chcete resetovat svůj profil? Tuto akci nelze vrátit zpět!"):
            self.dm.reset_all()
            self.stats_lbl.configure(text = "Odehrané hry: 0\nVýhry: 0\nRemízy: 0\nProhry: 0")
            self.username.set(self.dm.username)
            self.picture = ctk.CTkImage(self.dm.profile_picture, size=(100, 100))
            self.profile_picture_bt.configure(image=self.picture)

    def select_image(self):
        filetypes = (("Images", ["*.png", "*.jpg", "*.jpeg", "*.jpe", "*.jfif", "*.j2c", "*.j2k", "*.jp2", "*.jpc", "*.jpf", "*.jpx", "*.ico", "*.webp", "*.gif"]), ("All files", "*.*"))
        img_path = filedialog.askopenfilename(title="Zvolte profilový obrázek", filetypes=filetypes)
        if img_path == "":
            return
        img = Image.open(img_path)
        self.dm.save_user_data(profile_picture=img)
        self.picture = ctk.CTkImage(img, size=(100, 100))
        self.profile_picture_bt.configure(image = self.picture)

    def refresh(self):
        self.stats_lbl.configure(text = f"Odehrané hry: {self.dm.games_played}\nVýhry: {self.dm.wins}\nRemízy: {self.dm.draws}\nProhry: {self.dm.losses}")