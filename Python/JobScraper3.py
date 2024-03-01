from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

# page.click("button.Aside_searchButton__Xhqq3")
# page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
# page.keyboard.down("Enter")
# page.click("a#search_tab_position")

jobs_db = []

for x in range(2):
    time.sleep(1)
    page.keyboard.down("End")

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all(
    "div", class_="JobCard_container__FqChn JobCard_container--variant-card__znjV9")

for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title__ddkwM").text
    company_name = job.find("span", class_="JobCard_companyName__vZMqJ").text

    job = {
        "title": title,
        "company_name": company_name,
        "link": link
    }
    jobs_db.append(job)

file = open("jobs.csv", mode="w", encoding="utf-8-sig")
writer = csv.writer(file)
writer.writerow(["title", "company_name", "link"])

for job in jobs_db:
    writer.writerow(job.values())
file.close()
