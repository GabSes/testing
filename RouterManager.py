import paramiko

# Update the next three lines with your router's information
host = "192.168.1.1"
username = "root"
password = "Admin123"
# Define the commands for modifying the wireless access point
commands = [
    'ubus call uci get \'{"config":"wireless","section":"default_radio0","option":"ssid","ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\'',
    'ubus call uci set \'{"config":"wireless","section":"default_radio0","values":{"ssid":"change2"},"ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\'',
    'ubus call uci commit \'{"config":"wireless","ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\'',
    'ubus call uci apply \'{"rollback":"false","timeout":"1","ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\''
]

# Establish SSH connection
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, username=username, password=password)
    print("Connected to the router.")

    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        print(f"Command '{command}' executed.")

        # Print command output
        output = stdout.read().decode()
        if output:
            print("Output:", output.strip())

        # Print command error
        error = stderr.read().decode()
        if error:
            print("Error:", error.strip())

    print("Changes applied successfully.")

except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
except paramiko.SSHException as e:
    print(f"SSH connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()
