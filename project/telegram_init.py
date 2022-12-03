from telegram.ext import Updater, CallbackContext, CommandHandler, Dispatcher
from telegram import Update
from project.utils import read_from_json, save_to_json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)
logging.info("Running the telegram initializer...")
creds = read_from_json()
updater: Updater = Updater(creds.get("telegram_token", None), use_context=True)
dp: Dispatcher = updater.dispatcher


def tgc_start(update: Update, context: CallbackContext):
    creds["telegram_id"] = str(update.message.chat_id)
    logging.info(f"Received start command from '{creds['telegram_id']}'")
    save_to_json(creds)
    update.message.reply_text("Your chat ID has been successfully recorded!")


if __name__ == "__main__":
    dp.add_handler(CommandHandler("start", tgc_start))
    updater.start_polling()
    logging.info("Telegram bot has started")
    