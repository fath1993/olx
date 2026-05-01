import json

import requests
import time
from apps.custom_logs.models import custom_log
from erp.settings import BOT_TOKEN

def telegram_http_send_message_via_get_method(chat_id, text):
    telegram_bot_config = '1234'
    if not telegram_bot_config:
        return custom_log('telegram bot config not set')

    try:
        req = requests.get(
            url='https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + str(
                chat_id) + '&text=' + str(text))
        custom_log('telegram_http_send_message_via_get_method-> message: ' + str(json.loads(req.content)))
    except Exception as e:
        custom_log('telegram_http_send_message_via_get_method->try/except. err: ' + str(e))


def telegram_http_send_message_via_post_method(chat_id, text, parse_mode, reply_to_message_id=None, reply_markup=None):
    telegram_bot_config = '1234'
    if not telegram_bot_config:
        return custom_log('telegram bot config not set')

    telegram_api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    try:
        response = requests.post(telegram_api_url, data=data)
        custom_log('telegram_http_send_message_via_post_method-> message: ' + str(json.loads(response.content)))
        response_message = {
            'result': 'success',
            'message': response.text,
        }
    except Exception as e:
        custom_log('telegram_http_send_message_via_post_method->try/except. err: ' + str(e))
        response_message = {
            'result': 'failed',
            'message': str(e),
        }
    return response_message


def telegram_http_update_message_via_post_method(chat_id, message_id, text, parse_mode, reply_markup=None):
    telegram_bot_config = '1234'
    if not telegram_bot_config:
        return custom_log('telegram bot config not set')

    time.sleep(3)
    telegram_api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText'
    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,

    }
    try:
        response = requests.post(telegram_api_url, data=data)
        response_json = json.loads(response.content)
        response_message = {
            'result': 'success',
            'message': response.text,
        }

        if 'error_code' in response_json and response_json['error_code'] == 429:
            retry_after = response_json['parameters']['retry_after']
            custom_log(f"telegram_http_update_message_via_post_method-> Rate limited. Waiting for {retry_after} seconds before retry.")
            response_message = {
            'result': 'failed',
            'message': 'no message',
        }
            time.sleep(retry_after)

    except Exception as e:
        custom_log('telegram_http_update_message_via_post_method->try/except. err: ' + str(e))
        response_message = {
            'result': 'failed',
            'message': str(e),
        }
    return response_message


def telegram_http_send_photo_via_post_method(chat_id, photo, caption, parse_mode, message_thread_id=None,
                                             caption_entities=None,
                                             has_spoiler=None, disable_notification=None, protect_content=None,
                                             reply_to_message_id=None, allow_sending_without_reply=None,
                                             reply_markup=None, ):
    telegram_bot_config = '1234'
    if not telegram_bot_config:
        return custom_log('telegram bot config not set')

    telegram_api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    data = {
        'chat_id': chat_id,
        'message_thread_id': message_thread_id,
        'photo': photo,
        'caption': caption,
        # 'parse_mode': parse_mode,
        # 'caption_entities': caption_entities,
        # 'has_spoiler': has_spoiler,
        # 'disable_notification': disable_notification,
        # 'protect_content': protect_content,
        # 'reply_to_message_id': reply_to_message_id,
        # 'allow_sending_without_reply': allow_sending_without_reply,
        # 'reply_markup': reply_markup,
    }
    try:
        response = requests.post(telegram_api_url, data=data)
        custom_log('telegram_http_send_photo_via_post_method-> message: ' + str(json.loads(response.content)))
        response_message = {
            'result': 'success',
            'message': response.text,
        }
    except Exception as e:
        custom_log('telegram_http_send_photo_via_post_method->try/except. err: ' + str(e))
        response_message = {
            'result': 'failed',
            'message': str(e),
        }
    return response_message
