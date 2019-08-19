from urllib.request import urlopen, Request
from BeautifulSoup import BeautifulSoup
import pickle

mistakes = {}
##for i in string.ascii_uppercase:
##  url = "http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/"+i
##  req = Request(url, headers={'User-Agent':"Magic Browser"})
##  print url
##  page = BeautifulSoup(urlopen(req))
##  for j in page.findAll("li"):
##    if "plainlinks" in repr(j):
##      k = j.text.split("(")
##      mistakes[k[0].strip()] = k[1].strip(") ")


url = "http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines"
req = Request(url, headers={'User-Agent':"Magic Browser"})
page = BeautifulSoup(urlopen(req))
for i in page.find("pre").text.splitlines():
  j = i.split("-&gt;")
  mistakes[j[0]] = j[1]

out = open("mistakes.pkl","wb")
pickle.dump(mistakes, out)
out.close()
