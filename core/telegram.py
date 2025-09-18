import asyncio
from telegram import Bot
from django.conf import settings


def send_telegram_message(message: str):
    """
    Send a message to Telegram chat using the bot.

    Args:
        message (str): The message text to send.
    """
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    asyncio.run(bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID,
        text=message,
        parse_mode='Markdown'
    ))
