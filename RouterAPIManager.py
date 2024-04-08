"""""
import requests
import json
import sys

class RouterAPIManager:
    def __init__(self, api_config_file):
        self.api_config = self.load_config(api_config_file)
        self.base_url = self.api_config.get("base_url")
        self.username = self.api_config.get("username")
        self.password = self.api_config.get("password")
        self.session = requests.Session()
        self.bearer_token = None

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            print("Error: Config file not found.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in config file.", file=sys.stderr)
            sys.exit(1)

    def authenticate(self):
        login_url = self.base_url + '/api/login'
        data = {
            "username": self.username,
            "password": self.password
        }
        try:
            response = self.session.post(login_url, json=data)
            response.raise_for_status()
            auth_response_data = response.json()
            if auth_response_data.get('success'):
                token_data = auth_response_data.get('data')
                if token_data:
                    self.bearer_token = token_data.get('token')
                    if self.bearer_token:
                        print("Authentication successful. Bearer token:", self.bearer_token)
                        return  # Exit method after successful authentication
                print("Error: Bearer token not found in authentication response.", file=sys.stderr)
            else:
                print("Error: Authentication unsuccessful.", file=sys.stderr)
            sys.exit(1)
        except requests.RequestException as e:
            print(f"Error: Authentication failed - {e}", file=sys.stderr)
            sys.exit(1)

    def change_access_point_configuration(self, new_configuration):
        if not self.bearer_token:
            print("Error: Bearer token not available. Authentication may be required.", file=sys.stderr)
            sys.exit(1)
            
        endpoint = self.base_url + '/api/wireless/interfaces/config/default_radio1'
        headers = {'Authorization': 'Bearer ' + self.bearer_token}
        try:
            # Ensure that the payload includes the "data" object
            payload = {"data": new_configuration}
            response = self.session.put(endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for non-200 status codes
            print("Access point configuration updated successfully.")
        except requests.RequestException as e:
            print(f"Error: Failed to update access point configuration - {e}", file=sys.stderr)
            sys.exit(1)


def main():
    api_config_file = 'router_config.json'
    access_point_config_file = 'access_point_config.json'

    api_manager = RouterAPIManager(api_config_file)
    api_manager.authenticate()

    try:
        with open(access_point_config_file, 'r') as f:
            new_configuration = json.load(f)
    except FileNotFoundError:
        print("Error: Access point config file not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in access point config file.", file=sys.stderr)
        sys.exit(1)
    print("Loaded Access Point Configuration:", new_configuration)
    api_manager.change_access_point_configuration(new_configuration)

if __name__ == "__main__":
    main()
"""""