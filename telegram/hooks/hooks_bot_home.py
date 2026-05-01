import json
import threading
from apps.utilities.telegram_message_handler import telegram_http_send_message_via_post_method
from apps.webhooks.hooks.olx import ejobs, olx
from apps.webhooks.hooks.hooks_menu import bot_core_main_menu_buttons


def bot_core_hooks(user_unique_id, text_message):
    if text_message == '/start':
        telegram_message_home(user_unique_id)
        return True
    
    if text_message == "📋 Latest Job List":
        telegram_message_get_latest_job_list(user_unique_id)
        return True
    
    return False


def telegram_message_home(user_unique_id):
    keyboard_markup = {
        "keyboard": bot_core_main_menu_buttons,
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    reply_markup = json.dumps(keyboard_markup)

    message_text = ''' 
    🏡 <b>شما در صفحه اصلی هستید.</b>\n\n
    🔹 با کلیک بر روی دکمه لیست بروز شده اخرین مشاغل را دریافت کنید.\n
    '''

    telegram_http_send_message_via_post_method(
        chat_id=user_unique_id,
        text=message_text,
        reply_markup=reply_markup,
        parse_mode='HTML'  # برای پشتیبانی از <b> و <br>
    )


def telegram_message_get_latest_job_list(user_unique_id):
    keyboard_markup = {
        "keyboard": bot_core_main_menu_buttons,
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    reply_markup = json.dumps(keyboard_markup)

    OlxThread(user_unique_id, reply_markup).start()
    EjobsThread(user_unique_id, reply_markup).start()

    message_text = ''' 
    🏡 نتایج در حال بروز رسانی است. لطفا منتظر بمانید ...\n
    '''

    telegram_http_send_message_via_post_method(
        chat_id=user_unique_id,
        text=message_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


class OlxThread(threading.Thread):
    def __init__(self, user_unique_id, reply_markup):
        super().__init__()
        self.user_unique_id = user_unique_id
        self.reply_markup = reply_markup
        
    def run(self):
        olx_text = str(olx()).replace('*', '')
        olx_chunks = split_text(olx_text)

        for olx_chunk in olx_chunks:
            telegram_http_send_message_via_post_method(
                chat_id=self.user_unique_id,
                text=olx_chunk,
                reply_markup=self.reply_markup,
                parse_mode=None
            )

class EjobsThread(threading.Thread):
    def __init__(self, user_unique_id, reply_markup):
        super().__init__()
        self.user_unique_id = user_unique_id
        self.reply_markup = reply_markup
        
    def run(self):
        ejobs_text = str(ejobs()).replace('*', '')
        ejobs_chunks = split_text(ejobs_text)

        for ejobs_chunk in ejobs_chunks:
            telegram_http_send_message_via_post_method(
                chat_id=self.user_unique_id,
                text=ejobs_chunk,
                reply_markup=self.reply_markup,
                parse_mode=None
            )    
    

def split_text(text, max_length=4000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]
