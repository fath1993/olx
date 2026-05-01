import threading

import requests

from olx.settings import GOOGLE_TRANSLATE_TOKEN
from scraper.models import get_settings


def translate_text(text, target_language):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_TRANSLATE_TOKEN}"

    payload = {
        "q": text,
        "target": target_language
    }

    try:
        response = requests.post(url, data=payload)

        if response.status_code == 403:
            print("limit has been reached")
            return text

        if response.status_code == 200:
            result = response.json()
            return result['data']['translations'][0]['translatedText']
        else:
            print(f"unknown error: {response.status_code}")
            return text

    except Exception as e:
        print("server error: ", e)
        return text


class TranslationThread(threading.Thread):
    def __init__(self, instance):
        super().__init__()
        self.instance = instance

    def run(self):
        translated = translate_text(self.instance.title, get_settings().translated_language)
        self.instance.title_translation = translated
        self.instance.save()

