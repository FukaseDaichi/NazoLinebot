import os
import requests


class GASManager:
    _instance = None
    _initialized = False

    def __new__(cls, base_url, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GASManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_url):
        # すでに初期化済みなら何もしない
        if self._initialized:
            return
        self.base_url = base_url
        print(f"Initialized GASApiFetcher with base_url: {self.base_url}")
        self._initialized = True

    def get_data(self, params):
        print(f"Fetching data with params: {params}")
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            print(f"HTTP GET request sent. URL: {response.url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from GAS API: {e}")
            return None

    def get_user_name(self, user_id):
        data = self.get_data({"key": "getusername", "userId": user_id})
        return data.get("message", None)

    def get_user(self, user_id):
        data = self.get_data({"key": "getuser", "userId": user_id})
        return data.get("message", None)

    def get_user_score(self, user_id, title):
        data = self.get_data({"key": "getscore", "userId": user_id, "title": title})
        return data.get("message", None)

    def get_score(self, title):
        data = self.get_data({"key": "getscore", "title": title})
        return data.get("message", None)

    def register_user(self, user_id, name=None, mode=None):
        payload = {"key": "putuser", "userId": user_id}
        if name is not None:
            payload["name"] = name
        if mode is not None:
            payload["mode"] = mode
        self.post_method(payload)

    def start_game(self, title, user_id):
        payload = {"key": "start", "title": title, "userId": user_id}
        self.post_method(payload)

    def end_game(self, title, user_id):
        payload = {"key": "end", "title": title, "userId": user_id}
        self.post_method(payload)

    def post_method(self, payload):
        try:
            print(payload)
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error with GAS API: {e}")
            return None

    def get_method(self, payload):
        try:
            print(payload)
            response = requests.get(self.base_url, params=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error with GAS API: {e}")
            return None


# Example usage
if __name__ == "__main__":
    base_url = os.environ["GAS_API_URL"]
    manager1 = GASManager(base_url)
    # 例として、get_userメソッドを呼び出す
    print(manager1.get_user("whitefranc1"))
