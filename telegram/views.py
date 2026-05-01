import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from apps.webhooks.hooks.hooks_bot_home import bot_core_hooks
from erp.settings import HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN
from apps.custom_logs.models import custom_log


class Webhook(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'webhook request'}

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        if code != 'nfdjbGDhd':
            return JsonResponse({'message': 'not allowed'})
        try:
            user_unique_id = 69254432
            text_message = "📋 Latest Job List"
            
            if bot_core_hooks(user_unique_id, text_message):
                return JsonResponse({'message': 'bot_core_hooks'})
            
            return JsonResponse({'message': 'problem'})
        except Exception as e:
            custom_log(f'{e}')
            return JsonResponse({'message': f'{e}'})


    def post(self, request, *args, **kwargs):
        try:
            telegram_response_check_result = telegram_response_check(request, True)
            if telegram_response_check_result is not None:
                user_unique_id = telegram_response_check_result[0]  # آی‌دی کاربر تلگرام
                user_first_name = telegram_response_check_result[1]  # نام کاربر
                text_message = telegram_response_check_result[2]  # پیام متنی (در صورت وجود)
                user_phone_number = telegram_response_check_result[3]  # شماره تلفن (در صورت ارسال مخاطب)
                document_info = telegram_response_check_result[4]  # اطلاعات فایل (در صورت ارسال فایل)
            else:
                return JsonResponse({'message': 'telegram_response_has_error'})
            
            if bot_core_hooks(user_unique_id, text_message):
                return JsonResponse({'message': 'bot_core_hooks'})
            
            return JsonResponse({'message': 'problem'})
        except Exception as e:
            custom_log(f'{e}')
            return JsonResponse({'message': f'{e}'})



def telegram_response_check(request, custom_log_print: bool):
    try:
        secret_key = request.META.get('HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN')
        if secret_key and str(secret_key) == f'{HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN}':
            if custom_log_print:
                custom_log('secret_key: confirmed')
            response_list = None
            try:
                front_input = json.loads(request.body)

                if custom_log_print:
                    custom_log(str(front_input))

                if 'callback_query' in front_input:
                    user_unique_id = front_input['callback_query']['from']['id']
                    user_first_name = front_input['callback_query']['from']['first_name']
                    message_text = front_input['callback_query']['data']
                    response_list = [user_unique_id,user_first_name, message_text, None, None]

                elif 'message' in front_input:
                    user_unique_id = front_input['message']['from']['id']
                    user_first_name = front_input['message']['from']['first_name']

                    # **بررسی پیام متنی**
                    if 'text' in front_input['message']:
                        message_text = str(front_input['message']['text'])
                        response_list = [user_unique_id, user_first_name, message_text, None, None]

                    # **بررسی تماس دریافتی**
                    elif 'contact' in front_input['message']:
                        user_phone_number = front_input['message']['contact']['phone_number']
                        message_text = front_input['message'].get('reply_to_message', {}).get('text', None)
                        response_list = [user_unique_id, user_first_name, message_text, user_phone_number, None]

                    # **بررسی فایل‌های ارسالی (`document`)**
                    elif 'document' in front_input['message']:
                        document_info = {
                            "file_id": front_input['message']['document']['file_id'],
                            "file_name": front_input['message']['document']['file_name'],
                            "mime_type": front_input['message']['document'].get('mime_type', 'unknown'),
                            "file_size": front_input['message']['document'].get('file_size', 0)
                        }
                        response_list = [user_unique_id, user_first_name, '', None, document_info]

                    # **بررسی عکس‌های ارسالی (`photo`)**
                    elif 'photo' in front_input['message']:
                        photo_info = front_input['message']['photo'][-1]  # آخرین عکس ارسال شده (بیشترین کیفیت)
                        document_info = {
                            "file_id": photo_info["file_id"],
                            "file_size": photo_info.get("file_size", 0)
                        }
                        response_list = [user_unique_id, user_first_name, '', None, document_info]
            except Exception as e:
                if custom_log_print:
                    import traceback
                    custom_log('Webhook->try/except. err: ' + str(traceback.format_exc()))
            return response_list
        else:
            if custom_log_print:
                custom_log('wrong secret_key')
            return None
    except:
        if custom_log_print:
            custom_log('unauthorized access')
        return None

