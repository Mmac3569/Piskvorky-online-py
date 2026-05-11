import socketio
import threading

class Networking:
    def __init__(self, game, data_manager):
        self.game = game
        self.dm = data_manager

        self.sio = socketio.Client()
        self.networking_thread = threading.Thread(target=self.start_connection, daemon=True)

        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        
        self.networking_thread.start()

    def start_connection(self):
        self.sio.connect('https://piskvorky-online.onrender.com', retry=True)
        self.sio.wait()

    def on_connect(self):
        print("Connected to server")

    def on_disconnect(self):
        print("Disconnected from server")