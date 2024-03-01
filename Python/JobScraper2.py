import requests
from bs4 import BeautifulSoup

all_jobs = []

keywords = ["flutter", "python", "golang"]


class Scraper:
    def scrap_jobs(self):
        soup = BeautifulSoup(self.response, "html.parser")
        jobs = soup.find("table", id="jobsboard").find_all("tr", class_="job")
        for job in jobs:
            job_info = job.find("td", class_="company")
            a = job_info.find("a")
            url = a["href"]
            title = a.find("h2", attrs={"itemprop": "title"})
            company = job_info.find("span", class_="companyLink").find(
                "h3", attrs={"itemprop": "name"})
            location = job_info.find(
                "span", class_="companyLink").next_sibling.next_sibling
            job_data = {
                "title": title.text.strip(),
                "company": company.text.strip(),
                "location": location.text.strip(),
                "link": f"https://remoteok.com{url}",
                "keyword": self.keyword
            }
            all_jobs.append(job_data)

    def show_jobs(self):
        filtered_jobs = [
            d for d in all_jobs if self.type in d.get("keyword", "")]
        print(filtered_jobs)

    def __init__(self, keyword):
        self.type = keyword
        response = requests.get(f"https://remoteok.com/remote-{keyword}-jobs", headers={
                                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        self.response = response.content
        self.keyword = keyword


python = Scraper(keywords[1])
python.scrap_jobs()
python.show_jobs()
golang = Scraper(keywords[2])
golang.scrap_jobs()
golang.show_jobs()
print(all_jobs)
