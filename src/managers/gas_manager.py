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
        return data["message"]

    def register_user(self, user_id, name):
        """
        Register a new user using the GAS API with a POST request.

        :param user_id: str, the userId for the new user
        :param name: str, the name of the new user
        :return: dict, the parsed JSON response from the API
        """
        payload = {"key": "putuser", "userId": user_id, "name": name}
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error registering user with GAS API: {e}")
            return None


# Example usage
if __name__ == "__main__":
    base_url = "https://script.google.com/macros/s/AKfycbybP4nB8hHYYGkAP8fYNrFnGQ4qY0D24-W407W5rSbXQ7DwMEop8-4kPrU4EzSw-eS3/exec"
    fetcher = GASManager(base_url)
    fetcher.register_user("idだよ","nameだよ")
    print(fetcher.get_user_name("saple"))
