from functools import partial
import threading
import requests


class GASManager:

    def __init__(self, base_url):
        """
        Initialize the GASApiFetcher with the base URL of the GAS API.

        :param base_url: str, the base URL of the GAS API
        """
        self.base_url = base_url
        print(f"Initialized GASApiFetcher with base_url: {self.base_url}")

    def get_data(self, params):
        """
        Fetch data from the GAS API using the provided key and userId.

        :param key: str, the key parameter for the API
        :param user_id: str, the userId parameter for the API
        :return: dict, the parsed JSON response from the API
        """
        print(f"Fetching data with params: {params}")
        try:
            response = requests.get(self.base_url, params=params)
            print(f"HTTP GET request sent. URL: {response.url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from GAS API: {e}")
            return None

    def get_user_name(self, user_id):
        data = self.get_data({"key": "getusername", "userId": user_id})
        print(data)
        return data["message"]

    def register_user(self, user_id, name):
        # ユーザー登録のためのペイロードを準備
        payload = {"key": "putuser", "userId": user_id, "name": name}
        # GAS APIへのPOSTリクエストを送信
        self.post_method(payload)
    
    def post_method(self, payload):
        """
        GAS APIへのPOSTリクエストを送信します。
        """
        try:
            print(payload)
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error with GAS API: {e}")
            return None
    


# Example usage
if __name__ == "__main__":
    base_url = "https://script.google.com/macros/s/AKfycbybP4nB8hHYYGkAP8fYNrFnGQ4qY0D24-W407W5rSbXQ7DwMEop8-4kPrU4EzSw-eS3/exec"
    fetcher = GASManager(base_url)
    fetcher.register_user("new","nameだよ")
    print(fetcher.get_user_name("new"))

    ## 登録
    # 値を束縛した新しい関数を作成
    target = partial(fetcher.register_user, None, None)
    # スレッドを作成して非同期で実行
    thread = threading.Thread(target=target)
    thread.start()

