import requests
from custom_logs.models import custom_log
from olx.settings import GOOGLE_TRANSLATE_TOKEN

def translate_text(text, target_language):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_TRANSLATE_TOKEN}"

    payload = {
        "q": text,
        "target": target_language
    }

    try:
        response = requests.post(url, data=payload)

        if response.status_code == 403:
            custom_log(f"{response.text}")
            return text

        if response.status_code == 200:
            result = response.json()
            return result['data']['translations'][0]['translatedText']
        else:
            custom_log(f"unknown error: {response.text}")
            return text

    except Exception as e:
        custom_log(f"server error: {e}")
        return text



