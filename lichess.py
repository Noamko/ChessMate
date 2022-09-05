import requests
import json

TOKEN = "lip_IwkkMuJRrd2LbiHC5Dyq"
LICHESS_API_URL = "https://lichess.org/api"

# TODO: make requests calls async

AUTH = {"authorization": f"Bearer {TOKEN}"}

class LichessAccount:
    def __init__(self, token=TOKEN):
        self.token = token
    
    def get_my_account(self) -> dict:
        response = requests.get(f"{LICHESS_API_URL}/account", headers=AUTH)
        return response.json()

    def getEmail(self):
        res = requests.get(f"{LICHESS_API_URL}/account/email", headers=AUTH)
        if res.status_code == 200:
            return json.loads(res.text)
 

class blinchess:
    headers = {"Authorization": f"Bearer {TOKEN}"}

    def __init__(self, token=TOKEN) -> None:
        self.token = token

    def get_current_challenges(self):
        res = requests.get("https://lichess.org/api/challenge", headers=AUTH)
        if res.status_code == 200:
            return json.loads(res.text)

    def challange_ai(self, ai_level: int=1, clock_limit=300, clock_increment=1, days=1, variant="standard") -> str:
        res = requests.post("https://lichess.org/api/challenge/ai", data={"level": ai_level, "clock.limit": clock_limit, "clock.increment": clock_increment, "days": days, "variant": variant}, headers=AUTH)
        if res.status_code == 201:
            return json.loads(res.text)

    def cancel_challenge(self, game_id: str) -> bool:
        res = requests.post(f"https://lichess.org/api/challenge/{game_id}/cancel", headers=AUTH)
        if res.status_code == 200:
            return True
        return False

    def make_move(self , game_id: str , move: str) -> bool:
        res = requests.post(f'https://lichess.org/api/board/game/{game_id}/move/{move}',headers=AUTH)
        if res.status_code == 200:
            return True
        return False

class Board:
    def __init__(self , game_id: str) -> None:
        self.game_id = game_id
    def seek(self):
        raise NotImplemented
    def writeInChat(self, message: str) -> bool:
        raise NotImplemented
    def fetchChat(self):
        raise NotImplemented
    def abortGame(self) -> bool:
        raise NotImplemented
    def resignGame(self) -> bool:
        raise NotImplemented
    def __init__(self, game_id: str) -> None:
        self.game_id = game_id
    def fetchGameState(self):
        res = requests.get(f"https://lichess.org/api/board/game/stream/{self.game_id}", headers=AUTH)
        if res.status_code == 200:
            return json.loads(res.text)

    def make_move(self, move: str) -> bool:
        res = requests.post(f"https://lichess.org/api/board/game/{self.game_id}/move/{move}", headers=AUTH)
        if res.status_code == 200:
            return True
        return False