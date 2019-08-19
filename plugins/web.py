# -*- coding: utf-8 -*-
import cairosvg
import tabulate

from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import io
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import json
import xml.dom.minidom
import re
from lxml import etree
import time
import random
from PIL import Image
import requests
help = "^google <string> does a google search, ^urban <word> gets first urbandictionary def, ^weather <State> <Location> gets the weather from the BOM. Australia only!"
def tiny(conn,data):
    if data['words'][0] == "^tiny" and len(data['words']) > 1:
        w = data['words'][1]
    else:
        for i in conn.chans[data['chan']]['scroll']:
            matches = re.findall(r'(https?://\S+)',i)
            if matches != []:
                w = matches[0]
                break
    try:
        url = urllib.request.urlopen("http://tinyurl.com/api-create.php?url="+w).read()
        conn.msg(data['chan'],data['fool']+": your tiny url from "+w+" is "+url)
    except:
        conn.msg(data['chan'],"Usage is ^tiny url, or ^tiny, the latter will scan the previous messages for a url")
def bitcoin(conn,data):
        
    try:
        if time.time() - conn.bitcoin['time']  > 60*15:
            getBitcoinCharts(conn)

    except AttributeError:
        getBitcoinCharts(conn)
    finally:
        btc = conn.bitcoin['chart']
    
    if len(data['words']) > 1:
        arg = data['words'][1]
        if arg == 'help':
            conn.msg(data['chan'],"Usage is ^bitcoin code>. Details sent to user")
            conn.msg(data['fool'],"Usage is ^bitcoin <code>. Default is mtgoxUSD. Codes are:"+(" ".join(list(btc.keys()))))
        else:   
            if arg in btc:
                m = btc[arg]
                conn.msg(data['chan'],"Bitcoin {} :Avg: {} {}. Volume: {}, High:{}, Low:{}".format(m['symbol'],m['avg'],m['currency'],m['volume'],m['high'],m['low']))
            else:
                conn.msg(data['chan'],"No such code. See ^bitcoin help for details")
    else:
        conn.msg(data['chan'],"Bitcoin: {} {}, {} {}".format(btc['mtgoxUSD']['avg'],btc['mtgoxUSD']['currency'], btc['mtgoxGBP']['avg'], btc['mtgoxGBP']['currency']))
def getBitcoinCharts(conn):
    print("Loading butts")
    btc = json.load(urllib.request.urlopen('http://bitcoincharts.com/t/markets.json'))
    markets = {}
    for i in btc:
        markets[i['symbol']] = i
    conn.bitcoin = {'chart':markets,
                    'time':time.time()}
    print(("Loaded at",conn.bitcoin['time']))
def imdb(conn,data):
    try:
        page = requests.get('http://www.omdbapi.com/', params={'apikey':'ea7415dd','t':'+'.join(data['words'][1:])}).json()
        if page["Response"] == "False":
            conn.msg(data['chan'],page["Error"])
        else:
            conn.msg(data['chan'],"Movie: %s, rating: %s, votes: %s, released: %s, director: %s, link: http://imdb.com/title/%s"%(page['Title'],page['imdbRating'],page['imdbVotes'],page['Released'],page['Director'],page['imdbID']))
    except IndexError:
        conn.msg(data['chan'],"Usage is ^imdb <film title>")

def shootout(conn,data):
    if len(data['words']) != 3 and not data['words'][1] == 'langs':
        conn.msg(data['chan'],'Usage is %s <lang1> <lang2>. Scores are how much slower the compiler is than the fastest. Use "^shootout langs" to show all languages'%(data['words'][0]))
        return
    page = BeautifulSoup(urllib.request.urlopen('http://benchmarksgame.alioth.debian.org/u64q/summarydata.php'),'html.parser')
    
    lines = str(page.find(id='summarydata').p).split('<br/>')
    lines[0] = lines[0][3:60]
    lines.pop()
    reader = csv.DictReader(lines)

    f = lambda: defaultdict(list)
    langs = defaultdict(f)

    for row in reader:
        lang = row['lang'].lower().replace(' ','-')
        langs[lang][row['name']].append({'mem(KB)':row['mem(KB)'],'elapsed':row['elapsed']})
        
    if data['words'][1].lower() =='langs':
        conn.msg(data['chan'], ', '.join(sorted(langs.keys())))

    l1 = data['words'][1].lower()
    l2 = data['words'][2].lower()

    if any([x not in langs for x in [l1,l2]]):
        conn.msg(data['chan'],"No such language found")
    else:
        c1,c2,m1,m2 = 0,0,0,0
        t1 = langs[l1]
        t2 = langs[l2]
        tests = set(t1.keys()).intersection(set(t2.keys()))
        print(("Comparing",l1,"to",l2,"with tests",tests))
        for test in tests:
            idx = len(t1[test])/2
            r1 = t1[test][idx]
            r2 = t2[test][idx]
            if r1['elapsed'] < r2['elapsed']:
                c1 += 1
            else:
                c2 += 1
            if r1['mem(KB)'] < r2['mem(KB)']:
                m1 +=1
            else:
                m2 +=1
        if c1 > c2:
            msg= l1,"wins!",c1,"-",c2
        elif c2 == c1:
            msg= l2,"and",l1,"are equal!"
        else:
            msg = l2,"wins!",c2,"-",c1
        conn.msg(data['chan'],"In speed "+(' '.join([str(x) for x in msg]))+", in memory use: "+l1+": "+str(m1)+", "+l2+": "+str(m2))


def ip(conn, data):
    if data['fool'] in conn.factory.admins:
        req = urllib.request.Request("http://ifconfig.co/ip", headers={'User-Agent':'twatbot'})
        ip = urllib.request.urlopen(req).read().decode('ascii')
        conn.notice(data['fool'],ip)
 
def convert(s):
    s = s.replace("<b>", '\2')
    s = s.replace("</b>", '\2')
    return s
def search(conn, data):
    conn.msg(data['chan'], 'plugin disabled because google removed the good api')
    try:
        page = json.load(urllib.request.urlopen("https://www.googleapis.com/customsearch/v1?key={}&q=".format(conn.factory.keys['google_search']) + ('%20'.join(data['words'][1:]))))
        for i in page["responseData"]["results"]:
            conn.msg(data['chan'],convert(i["title"]) + ": " + i["url"])
    except IndexError:
        conn.msg(data['chan'],"Usage is: ^google <search string>")

def urban(conn, data):
    try:
        if data['words'][-1].isdigit():
            i = int(data['words'].pop()) -1
            if i <0:
                i=0
        else:
            i = 0
        if data['words'][1].lower() == 'spam':
            conn.msg(data['chan'], data['fool']+": What are you currently trying to achieve you pathetic fucking lowlife")
            return
        try:
            d = requests.get("http://www.urbandictionary.com/iphone/search/define", params=[('term',' '.join(data['words'][1:]))]).json()
#            d = json.load(urllib.request.urlopen("http://www.urbandictionary.com/iphone/search/define?term=" + ('%20'.join(data['words'][1:]))))
            #print json.dumps(d,indent=4)
        except urllib.error.HTTPError as e:
            conn.msg(data['chan'],"Error: {}: {}".format(e.code, e.reason))
            return
#        if not d['has_related_words']:
#            conn.msg(data['chan'],"Word not defined. No suggestions.")
        if d['list'] == []:
            conn.msg(data['chan'],"No such word")
#        elif d['result_type'] != 'exact':
#            suggestions = map(lambda x: x['definition'], d['list'])[:4]
#            conn.msg(data['chan'],"Word is not defined. Perhaps you meant: " + (', '.join(suggestions)))  
        else:
            word = sorted(d['list'], key=lambda x:x['thumbs_up'],reverse=True)[i]
            conn.msg(data['chan'],
                     '\0030,2UrbanDictionary\003 {} (+{},-{},[{}/{}]): {} --- {}'.format(
                         word['word'],
                         word['thumbs_up'],
                         word['thumbs_down'],
                         i+1,
                         len(d['list']), 
                         str(word['definition']),
                         str(word['example'][:756].replace('\n',''))
                         )[:300]
                     )
    except IndexError as e:
        print (e)
        if i >= len(d['list']):
            conn.msg(data['chan'], 'There are {} definitions for {}'.format(len(d['list']), d['list'][0]['word']))
        else:
            conn.msg(data['chan'],"Usage is: ^ud <word>")

def weather(conn, data):
    chan = str(data['chan'])
    try:
        state = data['words'][1].lower()
        loc = ' '.join(data['words'][2:]).lower()
        with open("plugins/bom.dat") as f:
          for i in f:
            j = i.split()
            if j[0] == state:
              if ' '.join(j[2:]) == loc:
                s = j[1]
                break
            elif j[0] > state:
                break
        url = "http://www.bom.gov.au/fwo/" + (s.split(".")[0]) + "/" + s + ".json"
        print(url)
        req = urllib.request.build_opener()
        req.addheaders = [('User-Agent', 'Python Scraper')]
        q = json.load(req.open(url))
        o = q['observations']['data'][0]
        out = [{
            'City': o['name'],
            'Temp(°C)': o['air_temp'],
            'Wind(km/h)': o['wind_spd_kmh'], 
            'Rain(mm)':o['rain_trace'], 
            'Humidity(%)': o['rel_hum'], 
            'Wind_Dir': o['wind_dir'], 
            'Visibility(km)': o['vis_km'],
            'Updated':o['local_date_time']
        }]

        conn.msg(data['chan'], tabulate.tabulate(out, headers='keys', tablefmt='plain'))

    except IndexError as e:
        conn.msg(data['chan'],"Usage is ^weather <State> <Location>")
    except NameError as e:
        #Use wunderground since google discontinued weather services
        url = "http://autocomplete.wunderground.com/aq?query=" + ('%20'.join(data['words'][1:]))
        p = json.load(urllib.request.urlopen(url))
        if len(p['RESULTS']) == 0:
            conn.msg(data['chan'],"No such location")
            return
        code = p['RESULTS'][0]
        w = json.load(urllib.request.urlopen("http://api.wunderground.com/api/336ccf40f351429b/conditions/%s.json" %code['l'] ))['current_observation']
        conn.msg(data['chan'],"City: %s; %s: Temp: %s; Precip: %s; Wind: %s" % (w['display_location']['full'],w['weather'],w['temperature_string'],w['precip_today_string'],w['wind_string']))
        
        # Using google weather now
        
        
        #p = urllib2.urlopen("http://www.google.com/ig/api?weather=" + ('+'.join(data['words'][1:]))).read()
        #dom = xml.dom.minidom.parseString(p)
        #info = dict()
        #info["city"] = dom.getElementsByTagName("city")[0].getAttribute("data")
        #for i in dom.getElementsByTagName("current_conditions")[0].childNodes:
        #    info[i.tagName] = i.getAttribute("data")
        #conn.msg(data['chan'],' '.join(["City:", info["city"],
        #                        u"Temp (°C):", info["temp_c"],
        #                        info["humidity"],
        #                        info["wind_condition"],
        #                        "Condition:", info["condition"]
        #                        ])
        #            )
        #conn.msg(data['chan'],"No information for this location",chan)
        
def refreshFML(conn, data):
    conn.msg(data['chan'],"Refreshing page")
    req = urllib.request.Request("http://fmylife.com/random")
    req.add_header('User-agent', 'TwatBot')
    conn.page = BeautifulSoup(urllib.request.urlopen(req)).findAll('p', {"class":"block hidden-xs"})
def fml(conn, data):
    try:
        if len(conn.page) == 0:
            refreshFML(conn)
    except AttributeError as e:
        refreshFML(conn,data)
    conn.msg(data['chan'],conn.page.pop().text.strip())

def etymology(conn, data):
    try:
        page = BeautifulSoup(urllib.request.urlopen("http://www.etymonline.com/index.php?search=" + data['words'][1]))
        conn.msg(data['chan'],page.find('dd').text[:400])
    except IndexError as e :
        conn.msg(data['chan'],'usage is ^etym <word>')
    except AttributeError:
        conn.msg(data['chan'],'No word history available')
def emoji(conn, data):
    req = urllib.request.Request('http://www.reddit.com/r/emojipasta/.json')
    req.add_header('User-agent', 'TwatBot')
    page = json.load(urllib.request.urlopen(req))
    post = random.choice([x for x in page['data']['children'] if x['data']['is_self']])['data']
    msg = post['selftext']
    conn.msg(data['chan'],msg)
def reddit(sub):
    req = urllib.request.Request('http://www.reddit.com/r/{}/.json'.format(sub))
    req.add_header('User-agent', 'TwatBot')
    page = json.load(urllib.request.urlopen(req))
    post = random.choice(page['data']['children'])['data']
    msg = (post['title'] + " (" + post['domain'] + "," + post['subreddit'] + ") ( \x030,4+" + str(post['ups']) + "\x03 | \x030,2-" + str(post['downs']) + "\x03 ) http://redd.it/"+post['id'])
    return msg
def garfield(conn,data):
    conn.msg(data['chan'], reddit('garfield'))
def cj(conn, data):
    conn.msg(data['chan'],reddit('circlejerk+vegancirclejerk+programmingcirclejerk+androidcirclejerk'))
def make_req(url):
    req = urllib.request.Request(url)
    req.add_header('User-agent', 'Twatbot')
    return req
def desktop(conn,data):
    do = True
    try:
        do = conn.desktopFound
    except AttributeError:
        conn.desktopFound = True
    if not do:
        return
    else:
        conn.desktopFound = True
    for page in range(0,11):
        print(("Loading page: ",page))
        
        j = json.load(urllib.request.urlopen(make_req("http://api.4chan.org/g/%d.json"%(page))))
        for i in j['threads']:
            keys = ["desktoop thred","desktop thread","desktamp thread","time for love","desktop throd"]
            top = i['posts'][0]
            p = re.compile(r'<.*?>')
            q = re.compile(r'\W+')
            if 'com' in top:
                com = q.sub(' ',p.sub(' ',top['com'].lower()))
            
                if any([x in com for x in keys]):
                    conn.msg(data['chan'],"Desktop thread found on page %d at http://boards.4chan.org/g/res/%d"%(page,top['no']))
                    conn.desktopFound = False
                    return
        time.sleep(1)
    conn.msg(data['chan'],"No desktop threads found")
    conn.desktopFound = False

def yt(conn,data):
    try:
        page = json.load(urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?max-results=3&"+urllib.parse.urlencode({"q":' '.join(data['words'][1:])})))
    except:
        conn.msg(data['chan'],"Usage is ^yt <search terms>")
        return
    results = []
    for i in page['feed']['entry']:
        min = int(i['media$group']['yt$duration']['seconds'])/60
        sec = int(i['media$group']['yt$duration']['seconds'])%60
        max = i['gd$rating']['max']
        average = i['gd$rating']['average']
        rates = i['gd$rating']['numRaters']
        results.append("{} [{}:{}] by {}, views:{:}, {}/{} ({:} ratings) | {} ".format(i['title']['$t'],min,sec,i['author'][0]['name']['$t'],i['yt$statistics']['viewCount'],average,max,rates,i['link'][0]['href']))
    
    conn.msg(data['chan'],'\n'.join(results))
    
def reloadPrices(conn,data):
    conn.msg(data['chan'],"Reloading spreadsheet")
    prices = json.load(urllib.request.urlopen("http://backpack.tf/api/IGetPrices/v2/"))['response']['prices']
    try:
        conn.prices = {"fetched":time.time(),"prices":prices,"schema":conn.prices['schema']}
    except AttributeError:
        #load in the schema
        conn.prices =  {"fetched":time.time(),"prices":prices}
        getSchema(conn,data)
        return
    # If a price is lsited, but not in schema, it's time to reload the schema
    for i in conn.prices['prices']:
        if i not in conn.prices['schema']:
            print((i,"not in schema"))
            getSchema(conn,data)
            return
    
    
def getSchema(conn,data):
    conn.msg(data['chan'],"Reloading TF2 Schema")
    page = json.load(urllib.request.urlopen("http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key="+conn.factory.keys['steam_api_key']))
    conn.prices['quality'] =  {
                "selfmade": 9, 
                "Normal": 0, 
                "Unusual": 5, 
                "vintage": 3, 
                "completed": 12, 
                "customized": 10, 
                "Genuine": 1, 
                "unused": 2, 
                "unused": 4, 
                "strange": 11, 
                "haunted": 13, 
                "community": 7, 
                "Unique": 6, 
                "tobor_a": 14,
                "developer": 8,
                "Uncraftable":600
                 }
    conn.prices['quality'] = dict(list(zip(list(conn.prices['quality'].values()),conn.prices['quality'])))
    
    conn.prices['schema'] = {}
    for i in page["result"]['items']:
       conn.prices['schema'][i['defindex']] = i['name']

def pricecheck(conn,data):
    try:
        if time.time() - conn.prices['fetched'] >= 3600*12:
            reloadPrices(conn,data)
    except AttributeError:
        reloadPrices(conn,data)
    #Use the weapon name from the schema to get the itemid and look it up in the pricelist and send that info
    # Otherwise send an error msg
    itemId = -1
    if len(data['words']) <= 1:
        conn.msg(data['chan'],"Usage is ^pc <item name>")
        return
    needle = ' '.join(data['words'][1:]).lower()
    c = 0
    for i,j in conn.prices['schema'].items():
        if needle in j.lower():
            #we found the item
            print((i,j))
            if c > 4:
                break
            try:
                price = conn.prices['prices'][str(i)]
                c+=1
            except KeyError:
                print("no price listed for",i,j)
                continue
            print(price)
            p = '; '.join(["{}: {}".format(conn.prices['quality'][int(x)].title(),price[x]['0']['value']) for x in price if x != "5"])
            conn.msg(data['chan'],"Price for '{}' in ref: {}".format(j,p))
    if c==0:
        conn.msg(data['chan'],"No items found")
def closest_col(pxl):
   # cols = [(255,255,255),(0,0,0),(0,0,127), (0,147,0),(255,0,0), (127,0,0), (156,0,156), (252,127,0), (255,255,0), (0,252,0), 
   #         (0,147,147), (0,255,255), (0,0,252), (255,0,255), (127,127,127), (210,210,210)]
   cols =  {0: [255,255,255],     1   : [0,0,0],       2   : [0,0,205],     3   : [0,205,0],     4   : [255,0,0],     5   : [205,0,0],     6   : [205,0,205],   7   : [205,205,0],
            8   : [255,255,0],     9  : [0,255,0],     10  : [0,205,205],   11  : [0,255,255],   12  : [92,92,255],   13  : [255,0,255],   14  : [127,127,127], 15  : [229,229,229],
            16  : [95,0,0],       17  : [135,95,0],    18  : [135,135,0],   19  : [95,95,0],     20  : [0,95,0],      21  : [0,135,95],    22  : [0,95,95],     23  : [0,95,135],
            24  : [0,0,95],       25  : [95,0,135],    26  : [95,0,95],     27  : [135,0,95],    28  : [135,0,0],     29  : [175,95,0],    30  : [175,175,0],   31  : [95,135,0],
            32  : [0,135,0],      33  : [0,175,95],    34  : [0,135,135],   35  : [0,95,175],    36  : [0,0,135],     37  : [135,0,175],   38  : [135,0,135],   39  : [175,0,95],
            40  : [175,0,0],      41  : [215,95,0],    42  : [215,215,0],   43  : [135,175,0],   44  : [0,175,0],     45  : [0,255,175],   46  : [0,175,175],   47  : [0,135,255],
            48  : [0,0,175],      49  : [175,0,255],   50  : [175,0,175],   51  : [215,0,95],    52  : [255,0,0],     53  : [255,135,0],   54  : [255,255,0],   55  : [175,255,0],
            56  : [0,255,0],      57  : [95,255,215],  58  : [0,255,255],   59  : [95,175,255],  60  : [0,0,255],     61  : [215,95,255],  62  : [255,0,255],   63  : [255,0,135],
            64  : [255,95,95],    65  : [255,175,95],  66  : [255,255,95],  67  : [215,255,95],  68  : [95,255,95],   69  : [135,255,215], 70  : [95,255,255],  71  : [135,175,255],
            72  : [95,95,255],    73  : [215,135,255], 74  : [255,95,255],  75  : [255,95,175],  76  : [255,175,175], 77  : [255,215,175], 78  : [255,255,175], 79  : [215,255,175],
            80  : [175,255,175],  81  : [175,255,215], 82  : [175,255,255], 83  : [175,215,255], 84  : [175,175,255], 85  : [215,175,255], 86  : [255,175,255], 87  : [255,135,215],
            88  : [0,0,0],        89  : [18,18,18],    90  : [38,38,38],    91  : [58,58,58],    92  : [78,78,78],    93  : [98,98,98],    94  : [128,128,128], 95  : [158,158,158],
            96  : [188,188,188],  97  : [228,228,228], 98  : [255,255,255], 99  : [0,0,0]}
   return min(list(cols.items()), key=lambda x: (2*(x[1][0]-pxl[0])**2 + 4*(x[1][1]-pxl[1])**2 + 3*(x[1][2]-pxl[2])**2)**0.5)[0]
import binascii
def col_dist(a,b):
    r = (a[0] + b[0]) /2
    dr = (a[0] - b[0])**2
    dg = (a[1] - b[1])**2
    db = (a[2] - b[2])**2
    return (2*dr + 4*dg + 3* db + ((r*(dr-db))/256))**0.5
def closest_col_j(pxl):
    cols = {0: [255,255,255],     1   : [0,0,0],       2   : [0,0,205],     3   : [0,205,0],     4   : [255,0,0],     5   : [205,0,0],     6   : [205,0,205],   7   : [205,205,0],
            8   : [255,255,0],     9  : [0,255,0],     10  : [0,205,205],   11  : [0,255,255],   12  : [92,92,255],   13  : [255,0,255],   14  : [127,127,127], 15  : [229,229,229],16:(71, 0, 0),17:(71, 33, 0),18:(71, 71, 0),19:(50, 71, 0),20:(0, 71, 0),21:(0, 71, 44),22:(0, 71, 71),23:(0, 39, 71),24:(0, 0, 71),25:(46, 0, 71),26:(71, 0, 71),27:(71, 0, 42),28:(116, 0, 0),29:(116, 58, 0),30:(116, 116, 0),31:(81, 116, 0),32:(0, 116, 0),33:(0, 116, 73),34:(0, 116, 116),35:(0, 64, 116),36:(0, 0, 116),37:(75, 0, 116),38:(116, 0, 116),39:(116, 0, 69),40:(181, 0, 0),41:(181, 99, 0),42:(181, 181, 0),43:(125, 181, 0),44:(0, 181, 0),45:(0, 181, 113),46:(0, 181, 181),47:(0, 99, 181),48:(0, 0, 181),49:(117, 0, 181),50:(181, 0, 181),51:(181, 0, 107),52:(255, 0, 0),53:(255, 140, 0),54:(255, 255, 0),55:(178, 255, 0),56:(0, 255, 0),57:(0, 255, 160),58:(0, 255, 255),59:(0, 140, 255),60:(0, 0, 255),61:(165, 0, 255),62:(255, 0, 255),63:(255, 0, 152),64:(255, 89, 89),65:(255, 180, 89),66:(255, 255, 113),67:(207, 255, 96),68:(111, 255, 111),69:(101, 255, 201),70:(109, 255, 255),71:(89, 180, 255),72:(89, 89, 255),73:(196, 89, 255),74:(255, 102, 255),75:(255, 89, 188),76:(255, 156, 156),77:(255, 211, 156),78:(255, 255, 156),79:(226, 255, 156),80:(156, 255, 156),81:(156, 255, 219),82:(156, 255, 255),83:(156, 211, 255),84:(156, 156, 255),85:(220, 156, 255),86:(255, 156, 255),87:(255, 148, 211),88:(0, 0, 0),89:(19, 19, 19),90:(40, 40, 40),91:(54, 54, 54),92:(77, 77, 77),93:(101, 101, 101),94:(129, 129, 129),95:(159, 159, 159),96:(188, 188, 188),97:(226, 226, 226),98:(255, 255, 255), 99:(0,0,0)}
    return min(list(cols.items()), key=lambda x:col_dist(x[1], pxl))[0]
#    return min(cols.items(), key=lambda x: (2*(x[1][0]-pxl[0])**2 + 4*(x[1][1]-pxl[1])**2 + 3*(x[1][2]-pxl[2])**2)**0.5)[0]
def img(conn, data):
    if len(data['words']) != 2:
        conn.msg(data['chan'], "Usage is ^img https://url.to/img.png")
    else:
        try:
            url = data['words'][1]
            res = requests.get(url)
            if url.endswith('.svg'):
                
                imgsio = io.BytesIO()
                cairosvg.svg2png(url=url, write_to=imgsio)     
            else:
                imgsio = io.BytesIO(res.content)
            input_img = Image.open(imgsio).convert("RGB")
        except Exception as e:
            conn.msg(data['chan'], "Error: "+str(e))
            return
        finally:
            del res
            del imgsio
        width, height = input_img.size
        x_acc = 40
        max_x = int(conn._safeMaximumLineLength("PRIVMSG {} :".format(data['chan'])))/9 -1
        x_axx = max_x
        r = x_acc / float(width)
        dim = (int(x_acc), int(height*r))
#        hsize = int(input_img.size[0]
        input_img = input_img.resize(dim, Image.LANCZOS)
        for y in range(dim[1]//2):
            old_char = None
            old_top = None
            old_bot = None
            y2 = 2*y
            line = ''
            for x in range(dim[0]):
                top_pxl = input_img.getpixel((x,y2))
                bot_pxl = input_img.getpixel((x,y2+1))
                # get the closest ansi colour to this pixel
                top_col = closest_col_j(top_pxl)
                bot_col = closest_col_j(bot_pxl)
                if old_bot == bot_pxl:
                    new_char = '\x03{:02d}▀'.format(top_col)
                else:
                    new_char = "\x03{},{}▀".format(top_col, bot_col)
                if new_char == old_char:
                    line += "▀"
                else:
                    line += new_char
                old_char = new_char
                old_bot = bot_pxl
            
            conn.msg(data['chan'], line)
        del input_img
def ll(conn, data):
    max_x = int(conn._safeMaximumLineLength("PRIVMSG {} :".format(data['chan'])))/9 -1
    conn.msg(data['chan'], "Max msg length: {}, img width: {}".format(conn._safeMaximumLineLength("PRIVMSG {} :".format(data['chan'])),max_x))
def pcreload(conn,data):
    if data['fool'] in conn.factory.admins:
        reloadPrices(conn,data)            
def currency(conn,data):
    xml = requests.get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    if len(data['words']) != 4:
        conn.msg(data['chan'], "^conv amnt currency_a currency_b")
        return
    parsed = etree.parse(io.BytesIO(xml.text.encode('utf-8')))
    cmd, amnt,curn_a,curn_b = data['words']
    try:
        amnt = float(amnt)
    except:
        conn.msg(data['chan'],"amnt must be a number")
        return
    try:
        cur_a = float(parsed.xpath(f"//*[@currency='{curn_a.upper()}']/@rate")[0])
        cur_b = float(parsed.xpath(f"//*[@currency='{curn_b.upper()}']/@rate")[0])
    except Exception as e:
        conn.msg(data['chan'], "currencies must a valid currency "+str(e))
        return
    euros = amnt / cur_a
    out = round(euros * cur_b,2)
    conn.msg(data['chan'], f"{amnt} {curn_a.upper()} = {out} {curn_b.upper()}")
triggers = {'^ud':urban,
            '^ll':ll,
            '^g':search,
            '^yt':yt,
            '^priceReload':pcreload,
            '^google':search,
            "^weather":weather,
            '^pc':pricecheck,
            '^fmyl':fml,
#            '^fb':openBook,
            '^etym':etymology,
            '^ip':ip,
            '^circlejerk': cj,
            '^desktop':desktop,
            '^shootout':shootout,
            '^benchmark':shootout,
            '^imdb':imdb,
            '^bitcoin':bitcoin,
            '^tiny':tiny,
            '^imgt': img,
            '^emoji': emoji,
            '^garfield': garfield,
            'lasagna': garfield,
            '^conv':currency
            }

