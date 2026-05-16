from typing import TYPE_CHECKING
from game import Game
import socketio
import threading
from tkinter import messagebox

if TYPE_CHECKING:
    from frames.menu_frame import MenuFrame
    from frames.game_frame import GameFrame
    from data_manager import DataManager

class Networking:
    def __init__(self, data_manager: "DataManager", menu_frame: "MenuFrame", game_frame: "GameFrame"):
        self.game = None
        self.dm = data_manager
        self.menu_frame = menu_frame
        self.game_frame = game_frame

        self.sio = socketio.Client()
        self.networking_thread = threading.Thread(target=self.start_connection, daemon=True)
        self.server_addr = 'https://piskvorky-online.onrender.com'
        #self.server_addr = 'http://localhost:3000'

        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('error', self.on_error)
        self.sio.on('challenge', self.on_challenge)
        self.sio.on('start', self.on_start)
        self.sio.on('reject', self.on_reject)
        self.sio.on('move', self.on_move)
        
        self.sio.on('*', lambda event, data: print(f"Received event '{event}' with data: {data}"))
        
        self.networking_thread.start()

    def start_connection(self):
        self.sio.connect(self.server_addr, retry=True)
        self.sio.wait()

    def bind_to_game(self, game: "Game"):
        self.game = game

    def disconnect_from_server(self):
        self.sio.disconnect()

    def play(self, oponent):
        self.sio.emit("play", {"opponent": oponent})

    def send_move(self, x, y):
        self.sio.emit("move", {"room": self.room, "x": x, "y": y})

    def on_error(self, data):
        self.disconnect_from_server()
        self.on_disconnect()
        messagebox.showerror("Chyba", "Nepodařilo se připojit k serveru.\n" + data.get("type"))

    def on_challenge(self, data):
        print("Received challenge:", data)
        opponent = data.get("from")
        if messagebox.askyesno("Výzva", f"Obdrželi jste výzvu od hráče {opponent}. Chcete ji přijmout?"):
            self.sio.emit("accept", {"from": opponent})
        else:
            self.sio.emit("reject", {"from": opponent})

    def on_start(self, data):
        print("Game started with data:", data)
        self.room = data.get("room")
        begins = True if data.get("x_player") == self.dm.username else False
        opponent_name = data.get("o_player") if begins else data.get("x_player")
        self.menu_frame.master.switch_frame(self.game_frame)
        game = Game(self.game_frame, self.dm, networking=self, online=True, begins=begins, opponent_name=opponent_name)
        self.game_frame.game = game
        self.bind_to_game(game)

    def on_reject(self, data):
        messagebox.showinfo("Výzva zamítnuta", f"Hráč odmítnul vaši výzvu.")
        self.menu_frame.master.switch_frame(self.menu_frame)

    def on_move(self, data):
        self.game.eval_move(data.get("x"), data.get("y"), opponent_move=True)

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