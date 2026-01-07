import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

default_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
default_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
default_image_path = "test_image.png"  # Place a test image in your project directory

async def send_basic_telegram_image(bot_token, chat_id, image_path, caption="Test image from script"):
    bot = Bot(token=bot_token)
    with open(image_path, "rb") as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption)

if __name__ == "__main__":
    asyncio.run(send_basic_telegram_image(default_bot_token, default_chat_id, default_image_path))
    print("Image sent!")