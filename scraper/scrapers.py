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

        i = 0
        for job_card in job_cards:
            # title
            title_tag = job_card.find('h2', class_='job-card-content-middle__title') or job_card.select_one(
                '.job-card-wrapper__temp strong')
            job_card_title = title_tag.get_text(strip=True) if title_tag else None
            if not job_card_title:
                continue

            # company
            company_tag = job_card.find('h3', class_='job-card-content-middle__info--darker') or job_card.select_one(
                '.job-card-wrapper__temp strong:nth-of-type(2)')
            job_card_company = company_tag.get_text(strip=True) if company_tag else None

            # city
            city_tag = job_card.find('div', class_='job-card-content-middle__info')
            job_card_city = city_tag.get_text(strip=True) if city_tag else None

            # date
            date_tag = job_card.find('div', class_='job-card-content-top__date')
            job_card_date = date_tag.get_text(strip=True) if date_tag else None

            link_tag = job_card.find('a', href=True)
            job_card_link = link_tag['href'] if link_tag else None

            if Job.objects.filter(source='ejobs', title=job_card_title, company=job_card_company).exists():
                print(f'{job_card_title} existed')
            else:
                Job.objects.create(
                    source='ejobs',
                    title=job_card_title,
                    company=job_card_company,
                    city=job_card_city,
                    date=job_card_date,
                    link=job_card_link,
                )
                print(f'{job_card_title} created')

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