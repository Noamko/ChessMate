from base64 import decode
from xmlrpc.client import boolean
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


class lichess:
    headers = {"Authorization": f"Bearer {TOKEN}"}

    def __init__(self, token=TOKEN) -> None:
        self.token = token

    def get_current_challenges(self)-> str:
        res = requests.get(f"{LICHESS_API_URL}/challenge" , headers=AUTH)
        if res.status_code == 200:
            return json.loads(res.text)

    def challenge_ai(self, ai_level: int = 1, clock_limit=300, clock_increment=1, days=1, variant="standard") -> str:
        res = requests.post(f"{LICHESS_API_URL}/challenge/ai", data={
                            "level": ai_level, "clock.limit": clock_limit, "clock.increment": clock_increment, "days": days, "variant": variant}, headers=AUTH)
        if res.status_code == 201:
            return json.loads(res.text)

    def cancel_challenge(self, game_id: str) -> bool:
        res = requests.post(
            f"{LICHESS_API_URL}/challenge/{game_id}/cancel", headers=AUTH)
        if res.status_code == 200:
            return True
        return False

    def create_challenge(self , username:str , rated:bool = False , clock_limit:int = 50 , 
    clock_increment:int =30 , days:int = 1 , color:str = 'random' ,variant:str = 'standard', keep_alive :bool = False)-> str:
        res = requests.post(f"{LICHESS_API_URL}/challenge/{username}",headers = AUTH , params = {'username' : username,
       'rated':rated , 'clock.limit':clock_limit , 'clock.increment':clock_increment , 'days':days,
       'color':color,'variant':variant , 'keepAliveStream':keep_alive })
        if res.status_code == 200:
            return json.loads(res.text)

    def accept_challenge(self,challenge_id: str)-> bool:
        res = requests.post(f"{LICHESS_API_URL}/challenge/{challenge_id}/accept",headers=AUTH , data = {'challengeId': challenge_id})
        if res.status_code == 200:
            return True
        return False

    def decline_challenge(self , challenge_id: str)-> bool:
        res = requests.post(f"{LICHESS_API_URL}/challenge/{challenge_id}/decline" , headers=AUTH , data = {'challengeId': challenge_id})
        if res.status_code == 200:
            return True
        return False

    def get_current_games(self)->str:
        res = requests.get(f"https://lichess.org/api/account/playing",headers=AUTH)
        if res.status_code == 200:
            return json.loads(res.text)

    def del_all_ongoing_games(self)->None:
        current_games = self.get_current_games()
        now_playing = current_games['nowPlaying']
        board = Board()
        for game in now_playing:
            board.resign_game(game['gameId'])
            

class Board:
    

    def seek(self , rated:bool = False ,time:int = 15,increment:int = 15 , days:int = 1 
    , varient:str = 'standard' , color:str = 'random' , rating_range:str='1000-1200' )->str:
        res = requests.post(f'{LICHESS_API_URL}/board/seek' , headers=AUTH , params= {"rated" : rated , "time": time , 
        "increment" : increment , "days" : days , "variant" : varient , "color" : color , "ratingRange" : rating_range},stream=True)
        if res.status_code == 200:
            for line in res.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    yield json.loads(data)
        

    def write_in_chat(self,game_id:str, message: str , room : str) -> bool:
        res = requests.post(f"{LICHESS_API_URL}/board/game/{game_id}/chat" , headers=AUTH ,data={'room' : room , 'text': message})
        if res.status_code == 200:
            return True
        return False

    def fetch_chat(self,game_id:str)-> str:
        res = requests.get(f'{LICHESS_API_URL}/board/game/{game_id}/chat' ,headers=AUTH)
        if res.status_code == 200:
            return json.loads(res.text)

    def abort_game(self,game_id:str) -> bool:
        res = requests.post(f"{LICHESS_API_URL}/board/game/{game_id}/abort",headers=AUTH , data = {'gameId':game_id})
        if res.status_code == 200:
            return True
        return False

    def make_move(self,game_id:str ,move: str) -> bool:
        res = requests.post(
            f"{LICHESS_API_URL}/board/game/{game_id}/move/{move}", headers=AUTH)
        if res.status_code == 200:
            return True
        return False

    def resign_game(self,game_id:str)->bool:
        res = requests.post(
            f"{LICHESS_API_URL}/board/game/{game_id}/resign" , headers=AUTH
        )
        if res.status_code == 200:
            return True
        return False

    def game_state(self,game_id:str)-> str:
        res = requests.get(f"{LICHESS_API_URL}/board/game/stream/{game_id}" , headers=AUTH ,  stream=True)
        if res.status_code == 200:
            for line in res.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    yield json.loads(data)

    def incoming_events(self)-> str:
        res = requests.get(f"{LICHESS_API_URL}/stream/event" , headers=AUTH , stream=True)
        if res.status_code == 200:
            for line in res.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    yield json.loads(data)
    
                    
        
            