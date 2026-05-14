from game import Game
from data_manager import DataManager
from typing import TYPE_CHECKING

import socketio
import threading
from tkinter import messagebox

if TYPE_CHECKING:
    from frames.menu_frame import MenuFrame
    from frames.game_frame import GameFrame

class Networking:
    def __init__(self, data_manager: DataManager, menu_frame: "MenuFrame", game_frame: "GameFrame"):
        self.game = None
        self.dm = data_manager
        self.menu_frame = menu_frame
        self.game_frame = game_frame

        self.sio = socketio.Client()
        self.networking_thread = threading.Thread(target=self.start_connection, daemon=True)
        #self.server_addr = 'https://piskvorky-online.onrender.com'
        self.server_addr = 'http://localhost:3000'

        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('error', self.on_error)
        
        self.networking_thread.start()

    def start_connection(self):
        self.sio.connect(self.server_addr, retry=True)
        self.sio.wait()

    def bind_to_game(self, game: Game):
        self.game = game

    def disconnect_from_server(self):
        self.sio.disconnect()

    def play(self, oponent):
        self.sio.emit("play", {"oponent": oponent})

    def on_error(self, data):
        self.disconnect_from_server()
        messagebox.showerror("Chyba", "Nepodařilo se připojit k serveru.\n" + data.get("type"))

    def on_connect(self):
        print("Connected to server")
        self.sio.emit("login", {"username": self.dm.username})
        self.menu_frame.play_online_bt.configure(text = "Odpojit se", command=self.disconnect_from_server, state="normal")
        self.menu_frame.play_with_random_bt.configure(state="normal")
        self.menu_frame.play_with_friend_bt.configure(state="normal")

    def on_disconnect(self):
        print("Disconnected from server")
        self.menu_frame.play_online_bt.configure(text = "Hrát online", command=lambda: self.menu_frame.play_bt_click(online=True), state="normal")
        self.menu_frame.play_with_random_bt.configure(state="disabled")
        self.menu_frame.play_with_friend_bt.configure(state="disabled")