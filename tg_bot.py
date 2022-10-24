import logging
import os

from dotenv import load_dotenv

from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class ErrorLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)



def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    session_id = update.effective_user
    texts = update.message.text
    language_code = os.getenv('LANGUAGE_CODE')
    response = detect_intent_texts(project_id, session_id, texts, language_code)
    update.message.reply_text(response.query_result.fulfillment_text)


def detect_intent_texts(project_id, session_id, texts, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))
    
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response
    

def main() -> None:
    try:
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
        dispatcher.add_handler(CommandHandler("help", help_command))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        updater.start_polling()

        updater.idle()

    except ConnectionError as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        sleep(30)


if __name__ == '__main__':
    main()