from indeed import get_last_page
import requests
from bs4 import BeautifulSoup

# requests를 통한 크롤링할 사이트 지정
URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "fs-body3"}).find("a")["title"]
    company, location = html.find(
        "h3", {"class", "fs-body1"}).find_all("span", recursive=False)  # span 안의 span을 찾지 않도록 설정
    print(company, location)

    return {"title": title}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    # 여기 조절해서 더 찾을 수 있음
    last_page = int(get_last_page() / 10)
    jobs = extract_jobs(last_page)
    return jobs
