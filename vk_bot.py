import logging
import vk_api as vk
import os
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram import Bot
from dotenv import load_dotenv

from tg_bot import detect_intent_texts

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

def echo(event, vk_api):
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    session_id = event.user_id
    texts = event.text
    language_code = os.getenv('LANGUAGE_CODE')
    response = detect_intent_texts(project_id, session_id, texts, language_code)
    if not response.query_result.intent.is_fallback: 
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1,1000)
        )


if __name__ == '__main__':
    try:
        load_dotenv()

        telegram_bot_logger_token = os.getenv('TELEGRAM_BOT_LOGGER_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        bot_logger = Bot(token=telegram_bot_logger_token)
       
        logger.setLevel(logging.WARNING)
        logger.addHandler(ErrorLogsHandler(bot_logger, telegram_chat_id))

        vk_session = vk.VkApi(token=os.getenv('VK_TOKEN'))
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)

    except ZeroDivisionError as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
    except ReadTimeout as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
    except ConnectionError as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        sleep(30)

