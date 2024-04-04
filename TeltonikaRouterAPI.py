""""
import requests
import json
import sys

class TeltonikaRouterAPI:
    def __init__(self, router_config_file):
        self.router_config = self.load_config(router_config_file)
        self.base_url = self.router_config.get("base_url")
        self.username = self.router_config.get("username")
        self.password = self.router_config.get("password")
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
            print(f"Authentication failed: {e}", file=sys.stderr)
            sys.exit(1)

    def create_event_reporting_rule(self, rule_config_file):
        if not self.bearer_token:
            print("Error: Bearer token not available. Authentication may be required.", file=sys.stderr)
            sys.exit(1)
        
        rule_config = self.load_config(rule_config_file)
        endpoint = self.base_url + '/api/events_reporting/config'
        headers = {'Authorization': 'Bearer ' + self.bearer_token}
        try:
            response = self.session.post(endpoint, json=rule_config, headers=headers)
            response.raise_for_status()
            print("Event reporting rule created successfully.")
        except requests.RequestException as e:
            print(f"Failed to create event reporting rule: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    router_config_file = 'router_config.json'
    rule_config_file = 'event_reporting_rule.json'

    router_api = TeltonikaRouterAPI(router_config_file)
    router_api.authenticate()
    router_api.create_event_reporting_rule(rule_config_file)

if __name__ == "__main__":
    main()
"""