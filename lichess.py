import requests
import json

TOKEN = "lip_8ZplIKWkEUprINd1vKQ6"

# TODO: make requests calls async

headers = {"authorization": f"Bearer {TOKEN}"}
class lichess:
    headers = {"Authorization": f"Bearer {TOKEN}"}

    def __init__(self, token=TOKEN) -> None:
        self.token = token

    def getAccount(self):
        res = requests.get("https://lichess.org/api/account", headers=headers)
        if res.status_code == 200:
            return json.loads(res.text)

    def getEmail(self):
        res = requests.get("https://lichess.org/api/account/email", headers=headers)
        if res.status_code == 200:
            return json.loads(res.text)

    def get_current_challenges(self):
        res = requests.get("https://lichess.org/api/challenge", headers=headers)
        if res.status_code == 200:
            return json.loads(res.text)
            
    def challange_ai(self, ai_level: int=1, clock_limit=300, clock_increment=1, days=1, variant="standard") -> str:
        res = requests.post("https://lichess.org/api/challenge/ai", data={"level": ai_level, "clock.limit": clock_limit, "clock.increment": clock_increment, "days": days, "variant": variant}, headers=headers)
        if res.status_code == 201:
            return json.loads(res.text)

    def cancel_challenge(self, game_id: str) -> bool:
        res = requests.post(f"https://lichess.org/api/challenge/{game_id}/cancel", headers=headers)
        if res.status_code == 200:
            return True
        return False

    def make_move():
        raise NotImplemented

class Game:
    def __init__(self, game_id: str) -> None:
        self.game_id = game_id

    def get_game_state(self):
        res = requests.get(f"https://lichess.org/api/board/game/stream/{self.game_id}", headers=headers)
        if res.status_code == 200:
            return json.loads(res.text)

    def make_move(self, move: str) -> bool:
        res = requests.post(f"https://lichess.org/api/board/game/{self.game_id}/{move}", headers=headers)
        if res.status_code == 200:
            return True
        return False

        
        