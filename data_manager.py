import json
from PIL import Image

class DataManager():

    def __init__(self):
        self.load_user_data()

    def load_user_data(self):
        file = open("./data/user.json", "r", encoding="utf-8")
        data = json.load(file)
        self.username = data["username"]
        picture_path = "./data/" + data["profile-picture"]
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
        
        file = open("./data/user.json", "w", encoding="utf-8")
        json.dump({
            "username": self.username,
            "profile-picture": "profile_picture." + self.profile_picture.format
        }, file, indent=4, ensure_ascii=False)

    def load_stats(self):
        file = open("./data/stats.json", "r", encoding="utf-8")
        data = json.load(file)
        return data
    
    def save_stats(self, games_played = None, wins = None, draws = None, losses = None):
        if games_played == None and wins == None and draws == None and losses == None:
            return
        stats = self.load_stats()
        if games_played != None:
            stats["games_played"] = games_played
        if wins != None:
            stats["wins"] = wins
        if draws != None:
            stats["draws"] = draws
        if losses != None:
            stats["losses"] = losses
        
        file = open("./data/stats.json", "w", encoding="utf-8")
        json.dump(stats, file, indent=4, ensure_ascii=False)

    def reset_all(self):
        self.save_user_data(username="Anonymní uživatel", profile_picture=Image.open("./data/default_profile_picture.png"))
        self.save_stats(games_played=0, wins=0, draws=0, losses=0)