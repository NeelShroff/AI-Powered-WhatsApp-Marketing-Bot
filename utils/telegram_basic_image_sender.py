import asyncio
from telegram import Bot

# Replace these with your actual values
default_bot_token = "7976280160:AAHAIfa0lmFcTj7HJW_da__S7BzHrwmneEE"
default_chat_id = "2080681940"
default_image_path = "test_image.png"  # Place a test image in your project directory

async def send_basic_telegram_image(bot_token, chat_id, image_path, caption="Test image from script"):
    bot = Bot(token=bot_token)
    with open(image_path, "rb") as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption)

if __name__ == "__main__":
    asyncio.run(send_basic_telegram_image(default_bot_token, default_chat_id, default_image_path))
    print("Image sent!") 