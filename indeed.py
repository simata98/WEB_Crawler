import requests
from bs4 import BeautifulSoup

# requests를 통한 크롤링할 사이트 지정
LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)
    # 어떤 형식으로 출력할 것인가
    soup = BeautifulSoup(result.text, "html.parser")
    # 어떤 구문을 찾을 것인가
    pagination = soup.find("ul", {"class": "pagination-list"})
    # pagination 안에서 어떤 것을 찾을 것인가
    links = pagination.find_all('a')
    # pages라는 배열에 찾고자하는 것을 저장
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        title = result.find("h2", {"class": "title"}).find("a")["title"]
        print(title)
    return jobs
