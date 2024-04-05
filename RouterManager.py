import paramiko
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_ssh_commands(host, username, password, commands):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username=username, password=password)
        logger.info("Connected to the router.")

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            logger.info(f"Command '{command}' executed.")

            output = stdout.read().decode().strip()
            if output:
                logger.info(f"Output: {output}")

            error = stderr.read().decode().strip()
            if error:
                logger.error(f"Error: {error}")

        logger.info("Changes applied successfully.")

    except paramiko.AuthenticationException:
        logger.error("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        logger.error(f"SSH connection failed: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    host = "192.168.1.1"
    username = "root"
    password = "Admin123"

    commands = [
        'ubus call uci get \'{"config":"wireless","section":"default_radio0","option":"ssid","ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\'',
        'ubus call uci set \'{"config":"wireless","section":"default_radio0","values":{"ssid":"change2"},"ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\'',
        'ubus call uci commit \'{"config":"wireless","ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\'',
        'ubus call uci apply \'{"rollback":"false","timeout":"1","ubus_rpc_session":"2a199235cbf7d4f52ed0c0413e2b168a"}\''
    ]

    execute_ssh_commands(host, username, password, commands)
