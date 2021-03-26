import requests
from bs4 import BeautifulSoup

# requests를 통한 크롤링할 사이트 지정
LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
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


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company.find("a") is not None:
        company = str(company.find("a").string)
    else:
        company = str(company.string)
    company = company.strip()  # To erase blank
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {'title': title, 'company': company, 'location': location, "link": f"https://kr.indeed.com/채용보기?jk={job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"indeed {page}번째 페이지 scrapping 중")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
