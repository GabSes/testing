import requests
import json

class TeltonikaRouterAPI:
    def __init__(self, router_config_file):
        self.router_config = self.load_config(router_config_file)
        self.base_url = self.router_config.get("base_url")
        self.username = self.router_config.get("username")
        self.password = self.router_config.get("password")
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

    def create_event_reporting_rule(self, rule_config_file):
        rule_config = self.load_config(rule_config_file)
        endpoint = self.base_url + '/api/events_reporting/config'
        try:
            response = self.session.post(endpoint, json=rule_config)
            response.raise_for_status()
            print("Event reporting rule created successfully.")
        except requests.RequestException as e:
            print(f"Failed to create event reporting rule: {e}")
            exit(1)

def main():
    router_config_file = 'router_config.json'
    rule_config_file = 'event_reporting_rule.json'

    router_api = TeltonikaRouterAPI(router_config_file)
    router_api.authenticate()
    router_api.create_event_reporting_rule(rule_config_file)

if __name__ == "__main__":
    main()
