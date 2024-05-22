import asyncio
from telethon import TelegramClient
import re
import datetime
import pytz  # Import pytz to handle timezone information
import json
import os  # Import os module to access environment variables
from dotenv import load_dotenv  # Import load_dotenv from python-dotenv

# Load environment variables from .env file
load_dotenv()

pattern = r"#خلاصه_معاملات دلار میدان فردوسی تهران.*?🔳 کلوز رسمی"

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
channel_url = 'https://t.me/DollarFerdowsii'

async def main():
    # Initialize the client with your session and API details
    client = TelegramClient('/home/aiusrdata/git_projects/bots', api_id, api_hash)
    await client.start()
    
    # Get the channel entity based on URL
    channel = await client.get_entity(channel_url)
    
    # Define the date range with timezone awareness, assuming UTC
    utc = pytz.UTC
    start_date = datetime.datetime(2022, 5, 1, tzinfo=utc)
    end_date = datetime.datetime(2024, 5, 21, tzinfo=utc)

    # Regex pattern to match messages containing 'خلاصه_معاملات'
    pattern = r"خلاصه_معاملات"
    
    async for message in client.iter_messages(channel, offset_date=end_date):
        # Ensure the message date is after the start_date
        if message.date.astimezone(utc) < start_date:
            break  # Stop if the message is older than the start date
        if message.text and re.search(pattern, message.text):
            # Extract details using split
            lines = message.text.split("\n\n")
            if len(lines) >= 7:
                closing_line = lines[6].split("\n")[0]
                data = {
                    "date": lines[2].strip() if len(lines) > 2 else "N/A",
                    "start_transaction": lines[3].split()[-1].strip() if len(lines) > 3 else "N/A",
                    "highest_transaction": lines[4].split()[-1].strip() if len(lines) > 4 else "N/A",
                    "lowest_transaction": lines[5].split()[-1].strip() if len(lines) > 5 else "N/A",
                    "closing_transaction": closing_line.split()[-1].strip() if closing_line else "N/A"
                }
                # Convert the data dictionary to JSON
                json_data = json.dumps(data, ensure_ascii=False, indent=4)
                with open('output.json', 'a', encoding='utf-8') as file:
                    file.write(json_data + '\n')
                # Output the JSON data
                print(json_data)
            else:
                print("Incomplete data: ", message.text)

# Run the main function within the asyncio event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
