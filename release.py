import subprocess
import requests
import os
from config import config

class release:

    def __init__(self):
        self.config = config.config('config')

    def send_ntfy_message(self,message,tags):
        response = requests.post(
                self.config.get_item('release','NTFY_SERVER_ALERT'),  # Replace with your ntfy topic
                data=message,
                headers={
                    'Title': 'Prodtools Auto Release',
                    'Priority': '3',  # Normal priority
                    'Tags': tags
                }
        )
        if response.status_code != 200:
            print(f"Failed to send notification: {response.status_code}")

    def git_pull_and_notify(self):
        try:
            # Execute git pull
            git_result = subprocess.run(['git', 'pull'], capture_output=True,text=True,check=True)

            # Send notification to ntfy server
            self.send_ntfy_message(f"Git pull successful: {git_result.stdout}",'git,update')

        except subprocess.CalledProcessError as e:
            # Handle git pull errors
            self.send_ntfy_message(f"Git pull failed: {e.stderr}",'git,error')
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def run_command_and_notify(self,command):
        try:
            # Execute the command and capture output
            result = subprocess.run(command, shell=True, check=True,capture_output=True, text=True)
            
            # Command succeeded
            self.send_ntfy_message(f"Command '{command}' completed successfully\nOutput: {result.stdout}","computer,terminal")

        except subprocess.CalledProcessError as e:
            # Send notification to ntfy server
            self.send_ntfy_message(f"Command '{command}' failed with error:\n{e.stderr}","computer,terminal")

if __name__ == "__main__":
    current_release = release()
    current_release.git_pull_and_notify()
    current_release.run_command_and_notify('service prodtools restart')