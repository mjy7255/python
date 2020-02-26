import requests
from bs4 import BeautifulSoup

indeed_result=requests.get("https://www.indeed.com/jobs?q=python&limit=50")


indeed_soup = BeautifulSoup(indeed_result.text,"html.parser")

pagination = indeed_soup.find("div",{"class":"pagination"})



links=pagination.find_all('a')
pages =[]

for link in links:
    pages.append(link.find("span").string)
pages=pages[0:-1]

print(pages)