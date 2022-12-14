import logging
import os

from dotenv import load_dotenv

from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from detect_intent import detect_intent_texts
from tg_error_logs_handler import ErrorLogsHandler


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def get_dialogflow_response(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    session_id = update.effective_user
    texts = update.message.text
    language_code = os.getenv('LANGUAGE_CODE')
    response = detect_intent_texts(project_id, session_id, texts, language_code)
    update.message.reply_text(response.query_result.fulfillment_text)


def main() -> None:
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()
    tg_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_bot_logger_token = os.getenv('TELEGRAM_BOT_LOGGER_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot_logger = Bot(token=telegram_bot_logger_token)
    
    logger.setLevel(logging.WARNING)
    logger.addHandler(ErrorLogsHandler(bot_logger, telegram_chat_id))

    updater = Updater(tg_bot_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_dialogflow_response))
    updater.start_polling()

    updater.idle()
    

if __name__ == '__main__':
    main()