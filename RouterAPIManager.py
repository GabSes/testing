"""
import requests
import json

class RouterAPIManager:
    def __init__(self, api_config_file):
        self.api_config = self.load_config(api_config_file)
        self.base_url = self.api_config.get("base_url")
        self.username = self.api_config.get("username")
        self.password = self.api_config.get("password")
        self.session = requests.Session()

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            print("Config file not found.")
            exit(1)
        except json.JSONDecodeError:
            print("Error decoding JSON config file.")
            exit(1)

    def authenticate(self):
        login_url = self.base_url + '/api/login'
        data = {
            "username": self.username,
            "password": self.password
        }
        try:
            response = self.session.post(login_url, json=data)
            response.raise_for_status()
            print("Authentication successful.")
        except requests.RequestException as e:
            print(f"Authentication failed: {e}")
            exit(1)

    def change_access_point_configuration(self, new_configuration):
        endpoint = self.base_url + '/wireless/devices/config'
        try:
            response = self.session.put(endpoint, json=new_configuration)
            response.raise_for_status()
            print("Access point configuration updated successfully.")
        except requests.RequestException as e:
            print(f"Failed to update access point configuration: {e}")
            exit(1)

def main():
    api_config_file = 'router_config.json'
    access_point_config_file = 'access_point_config.json'

    api_manager = RouterAPIManager(api_config_file)
    api_manager.authenticate()

    new_configuration = api_manager.load_config(access_point_config_file)
    api_manager.change_access_point_configuration(new_configuration)

if __name__ == "__main__":
    main()
"""