import requests
import json
import time

# Global variable to store previous player count
previous_player_count = None

# Function to get the player count from the website
def get_player_count():
    url = "https://growtopiagame.com/detail/"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()  # Parse the JSON response
            player_count = data.get("online_user")  # Extract the player count
            if player_count is not None:
                return int(player_count)  # Convert to integer
            else:
                print("Could not find the player count in the JSON response.")
                return None
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return None
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None

# Function to send a message to the Discord webhook
def send_to_discord(message):
    webhook_url = "https://discord.com/api/webhooks/1260191230772379649/qE4zRpGwp9CmFoGZW2YZp-tAv5x4qIdCgRIfuEwN-4XWS6wJGGGmu4pH_pliqahF_7Ik"
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code}")

# Main loop to periodically check the player count and send to Discord
while True:
    player_count = get_player_count()
    if player_count is not None:
        if previous_player_count is not None:
            difference = player_count - previous_player_count
            print(f"Player count: {player_count}, Previous count: {previous_player_count}, Difference: {difference}")  # Debug print
            
            if difference > 0:
                if difference > 15000:
                    change_message = f"Current Growtopia player count: {player_count} [__**+{difference}, server is up !**__ @everyone]"
                else:
                    change_message = f"Current Growtopia player count: {player_count} [__**+{difference}**__]"
            elif difference < 0:
                if difference < -1500:
                    change_message = f"Current Growtopia player count: {player_count} [__**{difference}, probably a banwave!**__ @everyone]"
                else:
                    change_message = f"Current Growtopia player count: {player_count} [__**{difference}**__]"
            else:
                change_message = f"Current Growtopia player count: {player_count} [__**No change**__]"
            
            print(change_message)
            send_to_discord(change_message)
        
        # Update previous player count
        previous_player_count = player_count
    else:
        print("Failed to retrieve player count.")
    
    time.sleep(30)
