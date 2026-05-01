import time
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from olx.settings import AI_SETTING_MAX_RETRIES, AI_SETTING_RETRY_DELAY, OPENAI_TOKEN
from scraper.models import Job


def ejobs():
    url = 'https://www.ejobs.ro/locuri-de-munca/timisoara/part-time/sort-publish'

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        job_cards_list = soup.find_all('ul', class_='job-cards-list')

        try:
            job_card_list = job_cards_list[0]
        except:
            return "job_card_list not found"

        job_cards = job_card_list.find_all('li', class_='job-card-wrapper')

        for job_card in job_cards:
            # title
            title_tag = job_card.find('h2', class_='job-card-content-middle__title')
            job_card_title = title_tag.get_text(strip=True) if title_tag else None
            job_card_title_translation =

            # company
            company_tag = job_card.find('h3', class_='job-card-content-middle__info--darker')
            job_card_company = company_tag.get_text(strip=True) if company_tag else None

            # city
            city_tag = job_card.find('div', class_='job-card-content-middle__info')
            job_card_city = city_tag.get_text(strip=True) if city_tag else None

            # date
            date_tag = job_card.find('div', class_='job-card-content-top__date')
            job_card_date = date_tag.get_text(strip=True) if date_tag else None

            link_tag = job_card.find('a', href=True)
            job_card_link = link_tag['href'] if link_tag else None

            try:
                Job.objects.get(
                    source='ejobs',
                    title=job_card_title,
                    date=job_card_date,
                )
            except:
                Job.objects.create(
                    source='ejobs',
                    title=job_card_title,
                    title_translation=job_card_title_translation,
                    company=job_card_company,
                    city=job_card_city,
                    date=job_card_date,
                    link=job_card_link,
                )

        return response_text

    except requests.RequestException as e:
        print("Request error:", e)


def olx():
    url = 'https://www.olx.ro/locuri-de-munca/timisoara/?currency=RON&search%5Bfilter_enum_type%5D%5B0%5D=part-time'

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        element = soup.select_one("#mainContent > div > div.css-5b6gg2")

        if element:
            response_text = f''''''
            response_text += 'OLX\n'
            response_text += 'https://www.olx.ro/locuri-de-munca/timisoara/?currency=RON&search%5Bfilter_enum_type%5D%5B0%5D=part-time\n'
            response_text += get_jobs_list(element.get_text(strip=True))
            return response_text
        else:
            return "Element not found"

    except requests.RequestException as e:
        print("Request error:", e)


def get_openai_response(model, temperature, system_prompt, prompt):
    attempt = 0
    while True:
        try:
            client = OpenAI(api_key=OPENAI_TOKEN)
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            attempt += 1
            if attempt == AI_SETTING_MAX_RETRIES:
                print(
                    f"get_openai_response: Failed after 3 retries' → {str(e)}")
                return False, e
            time.sleep(AI_SETTING_RETRY_DELAY)


def get_jobs_list(text):
    system_prompt = """
    You are a data analyst. You receive raw text (including HTML or webpage content) and analyze it to extract structured and complete information.

    - Extract all relevant items from the text
    - Do not skip any section
    - Do not invent missing values
    - If something is missing, return null
    - Keep the output clear, structured, and accurate
    """

    prompt = f'''
        از متن زیر، تمام آگهی‌های شغلی را بدون هیچ‌گونه فیلتر یا حذف استخراج کن.

        قوانین:

        1. تمام آگهی‌ها را استخراج کن، بدون توجه به اینکه در کدام بخش هستند، از جمله:
        - نتایج اصلی
        - نتایج پیشنهادی (arie mai mare de cautare)
        - هر سکشن دیگر

        2. هیچ آگهی‌ای را حذف نکن (حتی اگر خارج از شهر یا پیشنهادی باشد)،
        اما فقط مواردی را به عنوان آگهی در نظر بگیر که واقعاً نشان‌دهنده یک موقعیت شغلی مشخص باشند.
        متن‌های عمومی، تبلیغاتی، دکمه‌ها، لینک‌ها و call-to-action ها (مانند "مشاهده فرصت‌های شغلی"، "تماس بگیرید"، "بدون نیاز به رزومه") را آگهی محسوب نکن.

        3. برای هر آگهی این فیلدها را استخراج کن:
        - ترجمه فارسی عنوان شغل

        4. ترجمه عنوان شغل باید:
        - دقیق و طبیعی باشد
        - تحت‌اللفظی خشک نباشد (مناسب استفاده واقعی)
        - معنی شغل را درست منتقل کند

        5. اگر فیلدی وجود نداشت، مقدار آن را "نامشخص" قرار بده.

        6. خروجی را به صورت لیست شماره‌گذاری‌شده بده.

        7. در انتها:
        - تعداد کل آگهی‌ها را اعلام کن
        - مشخص کن آیا نشانه‌ای از صفحه‌بندی (pagination / صفحه دوم یا بیشتر) در متن وجود دارد یا نه
        - اگر وجود ندارد، دقیقاً بنویس: "no pagination found in provided text"

        8. قبل از پاسخ، کل متن را دوباره بررسی کن تا مطمئن شوی:
        - هیچ آگهی واقعی جا نیفتاده است
        - هیچ متن غیرمرتبط به اشتباه به عنوان آگهی استخراج نشده است

        9. ترجمه فارسی باید مطابق اصطلاحات رایج بازار کار باشد، نه ترجمه لغت‌به‌لغت.

        متن:
        <<<
        {text}
        >>>
    '''

    return get_openai_response('gpt-5.4', 0.5, system_prompt, prompt)
