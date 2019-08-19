from BeautifulSoup import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
states = ["nsw","vic","wa","qld","wa","sa","tas","act","nt"]
ids = dict()
for i in states:
    ids[i] = {}
    if i == "act":
        url = "http://www.bom.gov.au/"+i+"/observations/canberra.shtml"
    else:
        url = "http://www.bom.gov.au/"+i+"/observations/"+i+"all.shtml"
    soup = BeautifulSoup(urllib.request.urlopen(url))
    for j in soup.findAll("tr", {"class":"rowleftcolumn"}):
        tag = j.find("th")
        ids[i][tag.text.lower()] = tag.a["href"].split("/")[-1][:-6]
with open("bom.dat","w") as f:
  for i in iter(sorted(ids.items())):
    for j in iter(sorted(i[1].items())):
      f.write(' '.join([i[0],j[1],j[0]]))
      f.write('\n')
