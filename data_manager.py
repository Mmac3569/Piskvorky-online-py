import json
from datetime import datetime
from PIL import Image
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Main

class DataManager():

    def __init__(self, main: "Main"):
        self.main = main
        self.load_user_data()
        self.load_stats()
        self.load_game_history()

    def load_user_data(self):
        try:
            with open("./data/user.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            self.username = data["username"]
            picture_path = "./data/" + data["profile-picture"]
        except:
            self.username = "Anonymní uživatel"
            picture_path = "./data/default_profile_picture.png"
        try:
            self.profile_picture = Image.open(picture_path)
        except:
            self.profile_picture = Image.open("./data/default_profile_picture.png")
            self.save_user_data(profile_picture=self.profile_picture)

    def save_user_data(self, username = None, profile_picture = None):
        if self.username == None and self.profile_picture == None:
            return
        if username != None:
            self.username = username
        if profile_picture != None:
            self.profile_picture = profile_picture
            self.profile_picture.save("./data/profile_picture." + self.profile_picture.format.lower(), self.profile_picture.format)
            self.profile_picture = Image.open("./data/profile_picture." + self.profile_picture.format.lower())
        
        with open("./data/user.json", "w", encoding="utf-8") as file:
            json.dump({
                "username": self.username,
                "profile-picture": "profile_picture." + self.profile_picture.format.lower()
            }, file, indent=4, ensure_ascii=False)

    def load_stats(self):
        try:
            with open("./data/stats.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            self.games_played = data["games_played"]
            self.wins = data["wins"]
            self.draws = data["draws"]
            self.losses = data["losses"]
        except:
            self.games_played = 0
            self.wins = 0
            self.draws = 0
            self.losses = 0
    
    def save_stats(self, games_played = None, wins = None, draws = None, losses = None):
        if games_played == None and wins == None and draws == None and losses == None:
            return
        
        if games_played != None:
            self.games_played = games_played
        if wins != None:
            self.wins = wins
        if draws != None:
            self.draws = draws
        if losses != None:
            self.losses = losses
        
        with open("./data/stats.json", "w", encoding="utf-8") as file:
            json.dump({
                "games_played": self.games_played,
                "wins": self.wins,
                "draws": self.draws,
                "losses": self.losses
            }, file, indent=4, ensure_ascii=False)

    def load_game_history(self):
        try:
            with open("./data/game_history.json", "r", encoding="utf-8") as file:
                self.history = json.load(file)
        except:
            self.history = []

    def save_game_history(self):
        with open("./data/game_history.json", "w", encoding="utf-8") as file:
            json.dump(self.history, file, indent=4, ensure_ascii=False)

    def add_to_history(self, opponent: str, result: str):
        game_record = {
            "date": datetime.now().strftime("%Y-%m-%d-%H:%M"),
            "opponent_name": opponent,
            "result": result
        }
        self.history.append(game_record)
        self.main.profile_frame.add_to_history(game_record)
        self.save_game_history()

    def reset_all(self):
        self.save_user_data(username="Anonymní uživatel", profile_picture=Image.open("./data/default_profile_picture.png"))
        self.save_stats(games_played=0, wins=0, draws=0, losses=0)
        self.history = []; self.save_game_history()