import asyncio
from telegram import Bot

def send_telegram_image(bot_token: str, chat_id: str, image_path: str, caption: str = ""):
    """
    Send an image to a Telegram chat using a bot.
    Args:
        bot_token (str): Telegram bot token from BotFather.
        chat_id (str): Chat ID to send the image to.
        image_path (str): Path to the image file.
        caption (str): Optional caption for the image.
    """
    async def _send():
        bot = Bot(token=bot_token)
        with open(image_path, "rb") as image_file:
            await bot.send_photo(chat_id=chat_id, photo=image_file, caption=caption)
    asyncio.run(_send()) 