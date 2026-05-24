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

        self.room: str = None

        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('error', self.on_error)
        self.sio.on('opponent_disconnected', self.on_opponent_disconnected)
        self.sio.on('opponent_left', self.on_opponent_left)
        self.sio.on('challenge', self.on_challenge)
        self.sio.on('start', self.on_start)
        self.sio.on('reject', self.on_reject)
        self.sio.on('move', self.on_move)
        self.sio.on('draw', self.on_draw)
        self.sio.on('resign', self.on_resign)
        self.sio.on('rematch', self.on_rematch)
        
        self.sio.on('*', lambda event, data: print(f"Received event '{event}' with data: {data}"))
        
        self.networking_thread.start()

    def start_connection(self):
        self.sio.connect(self.server_addr, retry=True)
        self.sio.wait()

    def disconnect_from_server(self):
        self.sio.disconnect()

    def play(self, oponent):
        self.sio.emit("play", {"opponent": oponent})

    def send_move(self, x, y):
        self.sio.emit("move", {"room": self.room, "x": x, "y": y})

    def send_draw_offer(self):
        self.sio.emit("draw", {"room": self.room, "type": "offer"})

    def send_rematch_offer(self):
        if self.room is not None:
            self.sio.emit("rematch", {"room": self.room, "type": "offer"})
        else:
            messagebox.showinfo("Odveta", "Soupeř už opustil hru, vyzvěte ho v menu.")

    def send_resign(self):
        self.sio.emit("resign", {"room": self.room})

    def send_leave(self):
        self.sio.emit("leave", {"room": self.room})
        self.room = None

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
        self.game = Game(self.game_frame, self.dm, networking=self, online=True, begins=begins, opponent_name=opponent_name)
        self.game_frame.game = self.game
        self.menu_frame.reset_play_with_bts()

    def on_reject(self):
        messagebox.showinfo("Výzva zamítnuta", f"Hráč odmítnul vaši výzvu.")
        self.menu_frame.reset_play_with_bts()

    def on_move(self, data):
        self.game.eval_move(data.get("x"), data.get("y"), opponent_move=True)

    def on_draw(self, data):
        if data.get("type") == "offer":
            if messagebox.askyesno("Nabídka remízy", "Soupeř nabízí remízu. Přijímáš remízu?"):
                self.sio.emit("draw", {"room": self.room, "type": "accept"})
                self.game.draw()
            else:
                self.sio.emit("draw", {"room": self.room, "type": "reject"})
        elif data.get("type") == "accept":
            self.game.draw()
        elif data.get("type") == "reject":
            messagebox.showinfo("Soupeř zamítnul remízu.")

    def on_resign(self, data):
        self.game.resign(opponent_move=True)

    def on_rematch(self, data):
        if data.get("type") == "accept":
            self.game.rematch()
            self.game_frame.reset_game()
        elif data.get("type") == "reject":
            messagebox.showinfo("Odveta", "Soupeř odmítl vaši odvetu.")
            self.room = None
        elif data.get("type") == "offer":
            if messagebox.askyesno("Odveta", "Soupeř nabízí odvetu. Přijímáš odvetu?"):
                self.sio.emit("rematch", {"room": self.room, "type": "accept"})
                self.game.rematch()
                self.game_frame.reset_game()
            else:
                self.sio.emit("rematch", {"room": self.room, "type": "reject"})
                self.room = None

    def on_opponent_disconnected(self):
        self.game.resign(opponent_move=True, disconnect=True)
        self.room = None

    def on_opponent_left(self):
        self.room = None

    def on_connect(self):
        print("Connected to server")
        self.sio.emit("login", {"username": self.dm.username})
        self.menu_frame.play_online_bt.configure(text = "Odpojit se", command=self.disconnect_from_server, state="normal")
        self.menu_frame.reset_play_with_bts()

    def on_disconnect(self):
        print("Disconnected from server")
        self.menu_frame.play_online_bt.configure(text = "Hrát online", command=lambda: self.menu_frame.play_bt_click(online=True), state="normal")
        self.menu_frame.reset_play_with_bts(state="disabled")