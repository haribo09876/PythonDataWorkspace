from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import csv


# Job 데이터
class JobData:
    """
    ### Job 데이터
      - url:     링크 주소
      - title:   제목
      - company: 회사
      - reward:  리워드
    """

    def __init__(self, url: str = '', title: str = '', company: str = '', reward: str = ''):
        self.data = {
            'url': url,
            'title': title,
            'company': company,
            'reward': reward,
        }

    """
    ### CSV에서 필요한 값 가져오기
      - columns: 헤더에 사용되는 컬럼 순서
    """

    def get_csv_row(self, columns: list[str]) -> list:
        result: list[str] = []

        for key in columns:
            if key in self.data:
                result.append(self.data[key])
            else:
                result.append('')

        return result


# Job 스크랩
class JobScrap:
    """
    ### 원티드에서 직업 내역 가져오기
      - keywords: 직업 검색 키워드
    """

    def get_jobList(self, keywords: list[str]) -> dict[str, str]:
        # 브라우저 실행
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)

        # 결과 값
        result: dict[str, str] = {}

        # Wanted 웹페이지 접속
        page = browser.new_page()
        page.goto('https://www.wanted.co.kr/')
        time.sleep(3)

        # 키워드 별 데이터 가져오기
        for key in keywords:
            page.click('button[aria-label="검색"]')
            time.sleep(1)
            page.locator(
                'form[role=presentation] > input[type=search]').fill(key)
            time.sleep(1)
            page.keyboard.down('Enter')
            time.sleep(2)
            page.click('a#search_tab_position')
            time.sleep(3)

            for i in range(3):
                page.keyboard.down('End')
                time.sleep(1)

            result[key] = page.content()
            time.sleep(1)
        p.stop()

        return result

    """
    ### 직업 내역 추출 하기
      - html: get_jobList에서 가져온 html 값
    """

    def jobList_parser(self, html: str) -> list[JobData]:
        result: list[JobData] = []
        soup = BeautifulSoup(html, 'html.parser')

        job_list = soup.select(
            'div[role=list] > div[class^=JobCard_container]')
        for job in job_list:
            result.append(JobData(
                url=f"https://www.wanted.co.kr${job.select_one('a[href]')['href']}",
                title=job.select_one('strong[class^=JobCard_title]').text,
                company=job.select_one(
                    'span[class^=JobCard_companyName]').text,
                reward=job.select_one('span[class^=JobCard_reward]').text,
            ))

        return result

    """
    ### CSV로 저장하기
      - file_name: CSV 파일 명
      - job_list: jobList_parser 에서 가져온 내역
    """

    def save_csv(self, file_name: str, job_list: list[JobData]):

        # 파일 쓰기모드로 열기 (CSV Writer)
        file = open(f"{file_name}.csv", mode='w')
        writer = csv.writer(file)

        # CSV에 기록될 헤더 순서
        header = ['Title', 'Company', 'Reward', 'Url']
        # CSV에 기록될 데이터 순서
        column = ['title', 'company', 'reward', 'url']

        # 헤더 기록
        writer.writerow(header)

        # 데이터 기록
        for job in job_list:
            writer.writerow(job.get_csv_row(column))

        # 파일 닫기
        file.close()

    """
    ### 스크랩 시작
      - keywords: 직업 검색 키워드
      - is_save: 검색 내역 csv로 저장 여부
    """

    def run(self, keywords: list[str] = [], is_save=False):
        # 스크랩 할 키워드가 없을 경우
        if len(keywords) == 0:
            print('Please enter scrap keywords')

        # html 데이터 가져오기
        html_datas = self.get_jobList(keywords)

        # html 데이터 → 필요 데이터로 추출
        for key, html in html_datas.items():
            scrap_data = self.jobList_parser(html)

            if is_save:
                self.save_csv(key, scrap_data)


# 스크랩 클래스 선언
scrap = JobScrap()

# 스크랩 처리
scrap.run(
    keywords=[
        'flutter',
        'next js',
        'kotlin',
    ],
    is_save=True
)
