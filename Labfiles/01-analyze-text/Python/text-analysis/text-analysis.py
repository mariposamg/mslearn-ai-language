from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))

            # Get sentiment
            sentiment = ai_client.analyze_sentiment(documents=[text])[0]
            print('\nSentiment: {}'.format(sentiment.sentiment))

            # Get key phrases
            key_phrases = ai_client.extract_key_phrases(documents=[text])[0]
            print('\nKey phrases:')
            for phrase in key_phrases.key_phrases:
                print(phrase)


            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0]
            print('\nEntities:')
            for entity in entities.entities:
                print('\t{}: {}'.format(entity.category, entity.text))  

            # Get linked entities
            linked_entities = ai_client.recognize_linked_entities(documents=[text])[0]
            print('\nLinked entities:')
            for entity in linked_entities.entities:
                print('\t{}: {}'.format(entity.data_source, entity.name))
                print('\t\t{}'.format(entity.url))
                print('\t\t{}'.format(entity.data_source_entity_id))
                print('\t\t{}'.format(entity.language))
                print('\t\t{}'.format(entity.id))
                print('\t\t{}'.format(entity.bing_id))
                print('\t\t{}'.format(entity.match_score))      


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()