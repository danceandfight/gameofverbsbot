import json
import os

from dotenv import load_dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    load_dotenv()
    project_id = os.getenv('GOOGLE_PROJECT_ID')

    with open('questions.json') as file:
        questions_json = file.read()

    questions = json.loads(questions_json)

    for key in questions.keys():
        display_name = key
        training_phrases_parts = questions[key]['questions']
        message_texts = [questions[key]['answer']]

        create_intent(project_id, display_name, training_phrases_parts, message_texts)

if __name__ == '__main__':
    main()