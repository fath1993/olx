## 📌 Project Overview
This project is a **Telegram bot** designed to automatically collect and deliver the latest job listings from platforms like OLX and eJobs. It is built using **Python** and **Django**, and includes a **web-based admin panel** for full system management.

---

## ⚙️ Core Components

### 🤖 Telegram Bot
- Sends job listings directly to users
- Supports keyword-based subscriptions
- Provides simple interaction for receiving updates

### 🕷 Scraper Engine
- Extracts job data from OLX and eJobs
- Runs periodically to fetch new listings
- Avoids duplicate entries and processes only new data

### 🧑‍💼 Admin Panel (Django)
- Manage users and subscriptions
- Configure scraping parameters (keywords, categories, intervals)
- Monitor system activity and logs
- Control bot behavior

---

## 🛠 Tech Stack
- **Backend:** Python, Django, Django REST Framework  
- **Bot Integration:** Telegram Bot API  
- **Scraping:** Selenium / Requests / BeautifulSoup  
- **Database:** PostgreSQL  
- **Task Management:** Celery + Redis (optional)  

---

## 🚀 Functionality Flow
1. Admin defines keywords and scraping rules  
2. Scraper collects latest job postings  
3. Data is stored and filtered  
4. Telegram bot sends relevant jobs to users  

---

## 📦 Purpose
Automate job searching and deliver real-time job opportunities to users without manual browsing.
