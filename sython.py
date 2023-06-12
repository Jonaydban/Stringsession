import os
import logging
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token and developer ID
TOKEN = "6023715909:AAGQQyESjPK3f6NyrwTxoGllGqyldbsdEi4"
DEVELOPER_ID = 1631148798

# Your API ID and API hash
api_id = '23910531'
api_hash = '8c2802db0b56c6bd29282bd8fff933ef'

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id == DEVELOPER_ID:
        update.message.reply_text(
            f"Hello {user.first_name}, please send me your phone number."
        )

def extract_info(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id == DEVELOPER_ID:
        phone_number = update.message.text
        client = TelegramClient(StringSession(), api_id, api_hash)
        client.connect()

        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            update.message.reply_text("I've sent a code to your phone number. Please send me the code.")

            def handle_code(update: Update, context: CallbackContext) -> None:
                code = update.message.text
                client.sign_in(phone_number, code)
                session_str = client.session.save()
                update.message.reply_text(f"Session string: {session_str}")

            context.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_code))
            return

        session_str = client.session.save()
        update.message.reply_text(f"Session string: {session_str}")

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, extract_info))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
