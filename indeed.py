import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    indeed_result = requests.get(URL)

    indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

    pagination = indeed_soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.find("span").string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find('div', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    if company:
        company_anchor = company.find('a')
        if company_anchor is not None:
            company = str(company.find('a').string)
        else:
            company = str(company.string)
        company = company.strip()

    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']#[] 안에 있는건 attributes 적근시 사용 

    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f'https://www.indeed.com/jobs?q=python&limit=50&vjk={job_id}'
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page{page}:")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(2)
  return jobs