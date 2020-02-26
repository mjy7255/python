import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
  indeed_result=requests.get(URL)


  indeed_soup = BeautifulSoup(indeed_result.text,"html.parser")

  pagination = indeed_soup.find("div",{"class":"pagination"})



  links=pagination.find_all('a')
  pages =[]

  for link in links[:-1]:
      pages.append(int(link.find("span").string))
  max_page = pages[-1]
  return max_page

def extract_indeed_jobs(last_page):
  jobs=[]
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results:
        title= result.find("div", {"class":"title"}).find("a")["title"]
        print(title)

  return jobs