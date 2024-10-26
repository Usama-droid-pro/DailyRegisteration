import json
import sys
import time
from datetime import datetime
from http.client import HTTPSConnection
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

# Credentials stored in a dictionary
CREDENTIALS = {
    "user_id": "838767540133560321",  # Replace with actual user ID
    "token": "ODM4NzY3NTQwMTMzNTYwMzIx.GzrS9m.-bNmdWLWr5JzRJOzIIllv3AMeW_6Qfutj4QbcY",  # Replace with actual token
    "channel_1_url": "https://discord.com/channels/1121134385530404995/1121134386058903634",
    "channel_1_id": "1121134386058903634",
    "channel_2_url": "https://discord.com/channels/1121134385530404995/1121134386058903634",  # Replace with actual URL for 5:20 PM channel
    "channel_2_id": "1121134386058903634"  # Replace with actual channel ID for 5:20 PM message
}

def get_timestamp():
    """Returns a timestamp in the format YYYY-MM-DD HH:MM:SS."""
    return "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]"

def send_message(conn, channel_id, message_data, header_data):
    try:
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()
        if 199 < resp.status < 300:
            print(f"{get_timestamp()} Message sent successfully: {message_data}")
            return True
        else:
            print(f"{get_timestamp()} Failed to send message. Response: {resp.status} - {resp.read()}")
            return False
    except Exception as e:
        print(f"{get_timestamp()} Error sending message: {e} | {message_data}")
        return False

def get_connection():
    return HTTPSConnection("discordapp.com", 443)

def send_daily_message(channel_id, referrer_url, user_mention):
    # Define your message as a single formatted string
    message = f"""%register
Team Name: Leocious Esports
Team Tag: LEO
IGL Discord ID: {user_mention}"""

    message_data = json.dumps({"content": message})

    header_data = {
        "content-type": "application/json",
        "user-id": CREDENTIALS["user_id"],
        "authorization": CREDENTIALS["token"],
        "host": "discordapp.com",
        "referrer": referrer_url
    }

    conn = get_connection()
    success = False
    attempts = 0
    
    while not success and attempts < 10:
        success = send_message(conn, channel_id, message_data, header_data)
        attempts += 1
        if not success:
            print(f"{get_timestamp()} Retrying... Attempt {attempts}/10")
            time.sleep(2)  # Wait before retrying
    conn.close()
    
    print(f"{get_timestamp()} Finished sending the message!")

def main():
    # Set up scheduler
    scheduler = BlockingScheduler(timezone=pytz.timezone("Asia/Karachi"))
    
    # Schedule the 5:00 PM message
    scheduler.add_job(
        send_daily_message, 
        'cron', 
        args=(CREDENTIALS["channel_1_id"], CREDENTIALS["channel_1_url"], "<@767021373972414475>"),  # Replace with actual IGL ID
        hour=19, 
        minute=14,
        second=0
    )

    # Schedule the 5:20 PM message
    scheduler.add_job(
        send_daily_message, 
        'cron', 
        args=(CREDENTIALS["channel_2_id"], CREDENTIALS["channel_2_url"], "<@767021373972414475>"),  # Replace with actual IGL ID
        hour=19, 
        minute=14,
        second=30
    )

    print(f"{get_timestamp()} Scheduler set up to send messages daily at 5:00 PM and 5:20 PM PKT.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()
