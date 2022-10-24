import vk_api as vk
import os
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

def echo(event, vk_api):
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    session_id = event.user_id
    texts = event.text
    language_code = os.getenv('LANGUAGE_CODE')
    vk_api.messages.send(
        user_id=event.user_id,
        message=detect_intent_texts(project_id, session_id, texts, language_code),
        random_id=random.randint(1,1000)
    )

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))
    
    #for text in texts:
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text

if __name__ == '__main__':
    
    load_dotenv()

    vk_session = vk.VkApi(token=os.getenv('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
