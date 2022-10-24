import vk_api as vk
import os
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from tg_bot import detect_intent_texts

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
    
    load_dotenv()

    vk_session = vk.VkApi(token=os.getenv('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
