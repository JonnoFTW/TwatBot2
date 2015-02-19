
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import json
import xml.dom.minidom
import re
import time
import random
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
        url = urllib2.urlopen("http://tinyurl.com/api-create.php?url="+w).read()
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
            conn.msg(data['fool'],"Usage is ^bitcoin <code>. Default is mtgoxUSD. Codes are:"+(" ".join(btc.keys())))
        else:   
            if arg in btc:
                m = btc[arg]
                conn.msg(data['chan'],"Bitcoin {} :Avg: {} {}. Volume: {}, High:{}, Low:{}".format(m['symbol'],m['avg'],m['currency'],m['volume'],m['high'],m['low']))
            else:
                conn.msg(data['chan'],"No such code. See ^bitcoin help for details")
    else:
        conn.msg(data['chan'],"Bitcoin: {} {}, {} {}".format(btc['mtgoxUSD']['avg'],btc['mtgoxUSD']['currency'], btc['mtgoxGBP']['avg'], btc['mtgoxGBP']['currency']))
def getBitcoinCharts(conn):
    print "Loading butts"
    btc = json.load(urllib2.urlopen('http://bitcoincharts.com/t/markets.json'))
    markets = {}
    for i in btc:
        markets[i['symbol']] = i
    conn.bitcoin = {'chart':markets,
                    'time':time.time()}
    print "Loaded at",conn.bitcoin['time']
def imdb(conn,data):
    try:
        page = json.load(urllib2.urlopen('http://www.omdbapi.com/?%s'%(urllib.urlencode({'t':'+'.join(data['words'][1:])}))))
        if page["Response"] == "False":
            conn.msg(data['chan'],page["Error"])
        else:
            conn.msg(data['chan'],"Movie: %s, rating: %s, votes: %s, released: %s, director: %s, link: http://imdb.com/title/%s"%(page['Title'],page['imdbRating'],page['imdbVotes'],page['Released'],page['Director'],page['imdbID']))
    except IndexError:
        conn.msg(data['chan'],"Usage is ^imdb <film title>")

def shootout(conn,data):
    if len(data['words']) != 3:
        conn.msg(data['chan'],'Usage is %s <lang1> <lang2>. Scores are how much slower the compiler is than the fastest'%(data['words'][0]))
        return
    page = BeautifulSoup(urllib2.urlopen('http://benchmarksgame.alioth.debian.org/u64q/which-programs-are-fastest.php'))
    # A map of lang->median
    langs = {}
    for i in page.findAll('table')[-1].findAll('tr')[2:-1]:
        cells = i.findAll('td')
        langs[cells[1].text.replace('&nbsp;',' ')] = cells[5].text
    print langs
    s1 = data['words'][1]
    s2 = data['words'][2]
    l1 = ''
    l2 = ''
    base = ''
    for i in langs:
        if s1.lower() == i.split(' ')[0].lower():
            l1 = i
        elif s2.lower() == i.split(' ')[0].lower():
            l2 = i
        if langs[i] == '1.00':
            base = i
    if l2 == '' or l1 == '':
        conn.msg(data['chan'],"No such language found")
    else:
        best  = min([langs[l1],langs[l2]])
        worst = max([langs[l1],langs[l2]])
        if best == langs[l1]:
            best  = l1 +': '+ best
            worst = l2 +': '+ worst
        else:
            best  = l2 +': '+ best
            worst = l1 +': '+ worst
        conn.msg(data['chan'],"Shootout results: %s > %s. Scores show that the languages are x times slower than '%s'"%(best,worst,base))

def ip(conn, data):
    if data['fool'] in conn.factory.admins:
        ip = urllib2.urlopen("http://telize.com/ip").read()
        conn.notice(data['fool'],ip)
 
def convert(s):
    s = s.replace("<b>", '\2')
    s = s.replace("</b>", '\2')
    return s
def search(conn, data):
    try:
        page = json.load(urllib2.urlopen("https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + ('%20'.join(data['words'][1:]))))
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
            conn.msg(data['chan'], data['fool']+": What you are currently trying to achieve you pathetic fucking lowlife")
            return
        try:
            d = json.load(urllib2.urlopen("http://www.urbandictionary.com/iphone/search/define?term=" + ('%20'.join(data['words'][1:]))))
            print json.dumps(d,indent=4)
        except urllib2.HTTPError, e:
            conn.msg(data['chan'],"Error: {}: {}".format(e.code, e.reason))
            return
#        if not d['has_related_words']:
#            conn.msg(data['chan'],"Word not defined. No suggestions.")
        if d['result_type'] == 'no_results':
            conn.msg(data['chan'],"No such word")
#        elif d['result_type'] != 'exact':
#            suggestions = map(lambda x: x['definition'], d['list'])[:4]
#            conn.msg(data['chan'],"Word is not defined. Perhaps you meant: " + (', '.join(suggestions)))  
        else:
            word = d['list'][i]
            conn.msg(data['chan'],
                     '\0030,2UrbanDictionary\003 {} (+{},-{},[{}/{}]): {} --- {}'.format(
                         word['word'],
                         word['thumbs_up'],
                         word['thumbs_down'],
                         i+1,
                         len(d['list']), 
                         word['definition'],
                         word['example'][:756].replace('\n','')
                         )[:300]
                     )
    except IndexError, e:
        print e
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
        q = json.load(urllib2.urlopen(url))    
        out = ""
        for i in ['City', u'Temp(°C)', 'Wind(m/s)', 'Rain(mm)', 'Humidity(%)', 'Wind_Dir', 'Wind_spd(km/h)', 'Visibility(km)', 'Updated']:
            out += '%s ' % (i.rjust(10))
        conn.msg(data['chan'],out)
        out = ""
        for i in ['name', 'air_temp', "wind_spd_kmh", "rain_trace", "rel_hum", "wind_dir", "wind_spd_kmh", "vis_km", "local_date_time"]:
             out += "%s " % (str(q['observations']['data'][0][i]).rjust(10))
        conn.msg(data['chan'],out)
    except IndexError, e:
        conn.msg(data['chan'],"Usage is ^weather <State> <Location>")
    except NameError, e:
        #Use wunderground since google discontinued weather services
        url = "http://autocomplete.wunderground.com/aq?query=" + ('%20'.join(data['words'][1:]))
        p = json.load(urllib2.urlopen(url))
        if len(p['RESULTS']) == 0:
            conn.msg(data['chan'],"No such location")
            return
        code = p['RESULTS'][0]
        w = json.load(urllib2.urlopen("http://api.wunderground.com/api/336ccf40f351429b/conditions/%s.json" %code['l'] ))['current_observation']
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
    conn.page = BeautifulSoup(urllib2.urlopen("http://fmylife.com/random")).findAll('div', {"class":"post article"})
def fml(conn, data):
    try:
        if len(conn.page) == 0:
            refreshFML(conn)
    except AttributeError, e:
        refreshFML(conn,data)
    conn.msg(data['chan'],conn.page.pop().p.text)

def etymology(conn, data):
    try:
        page = BeautifulSoup(urllib2.urlopen("http://www.etymonline.com/index.php?search=" + data['words'][1]))
        conn.msg(data['chan'],page.find('dd').text[:400])
    except IndexError, e :
        conn.msg(data['chan'],'usage is ^etym <word>')
    except AttributeError:
        conn.msg(data['chan'],'No word history available')

def openBook(conn, data):
    try:
        j = json.load(urllib2.urlopen("http://graph.facebook.com/search?q=" + urllib.quote(' '.join(data['words'][1:])) + "&type=post"))
        print json.dumps(j,indent=2)
        for i in j["data"]: 
            try:
                if 'story' in i:
                    msg = "[link] "+convert(i['name'])+"; "+i['caption']+" --- "+i['link']
                else:
                    msg = i['message']
                if 'likes' in i:
                    likes = "("+i['likes']['count']+" likes) "
                else:
                    likes = ''
                conn.msg(data['chan'],("\x030,2Facebook\x03 {}, {} {}").format(i['from']['name'],likes,msg)[:750].replace('\n',''))
                break
            except:
                print json.dumps(i,indent=3)
                pass
        del j
    except IndexError as e:
        print e
    except urllib2.HTTPError as e:
        print e
        	
        conn.msg(data['chan'],"Usage is ^fb <search string>")
def cj(conn, data):
    random.seed()
    req = urllib2.Request('http://www.reddit.com/r/circlejerk+tumblrcirclejerk/.json')
    req.add_header('User-agent', 'TwatBot')
    page = json.load(urllib2.urlopen(req))
    post = random.choice(page['data']['children'])['data']
    msg = (post['title'] + " (" + post['domain'] + "," + post['subreddit'] + ") ( \x030,4+" + str(post['ups']) + "\x03 | \x030,2-" + str(post['downs']) + "\x03 ) http://redd.it/"+post['id']).encode('utf-8')
    conn.msg(data['chan'],msg)

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
    for page in xrange(0,11):
        print "Loading page: ",page
        j = json.load(urllib2.urlopen("http://api.4chan.org/g/%d.json"%(page)))
        for i in j['threads']:
            keys = ["desktoop thred","desktop thread","desktamp thread","time for love","desktop throd"]
            top = i['posts'][0]
            p = re.compile(r'<.*?>')
            q = re.compile(r'\W+')
            if 'com' in top:
                com = q.sub(' ',p.sub(' ',top['com'].lower()))
            
                if any(map(lambda x: x in com,keys)):
                    conn.msg(data['chan'],"Desktop thread found on page %d at http://boards.4chan.org/g/res/%d"%(page,top['no']))
                    conn.desktopFound = False
                    return
        time.sleep(1)
    conn.msg(data['chan'],"No desktop threads found")
    conn.desktopFound = False

def yt(conn,data):
    try:
        page = json.load(urllib2.urlopen("http://gdata.youtube.com/feeds/api/videos?max-results=3&alt=json&"+urllib.urlencode({"q":' '.join(data['words'][1:])})))
    except:
        conn.msg(data['chan'],"Usage is ^yt <search terms")
        return
    results = []
    for i in page['feed']['entry']:
        min = int(i['media$group']['yt$duration']['seconds'])/60
        sec = int(i['media$group']['yt$duration']['seconds'])%60
        max = i['gd$rating']['max']
        average = i['gd$rating']['average']
        rates = i['gd$rating']['numRaters']
        results.append(u"{} [{}:{}] by {}, views:{:}, {}/{} ({:} ratings) | {} ".format(i['title']['$t'],min,sec,i['author'][0]['name']['$t'],i['yt$statistics']['viewCount'],average,max,rates,i['link'][0]['href']))
    
    conn.msg(data['chan'],'\n'.join(results))
    
def reloadPrices(conn,data):
    conn.msg(data['chan'],"Reloading spreadsheet")
    prices = json.load(urllib2.urlopen("http://backpack.tf/api/IGetPrices/v2/"))['response']['prices']
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
            print i,"not in schema"
            getSchema(conn,data)
            return
    
    
def getSchema(conn,data):
    conn.msg(data['chan'],"Reloading TF2 Schema")
    page = json.load(urllib2.urlopen("http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key="+conn.factory.keys['steam_api_key']))
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
    conn.prices['quality'] = dict(zip(conn.prices['quality'].values(),conn.prices['quality']))
    
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
    for i,j in conn.prices['schema'].iteritems():
        if needle in j.lower():
            #we found the item
            print i,j
            if c > 4:
                break
            try:
                price = conn.prices['prices'][str(i)]
                c+=1
            except KeyError:
                print "no price listed for",i,j
                continue
            print price
            p = '; '.join(["{}: {}".format(conn.prices['quality'][int(x)].title(),price[x]['0']['value']) for x in price if x != "5"])
            conn.msg(data['chan'],"Price for '{}' in ref: {}".format(j,p))
    if c==0:
        conn.msg(data['chan'],"No items found")
            
            
def pcreload(conn,data):
    if data['fool'] in conn.factory.admins:
        reloadPrices(conn,data)            
        
triggers = {'^ud':urban,
            '^g':search,
            '^yt':yt,
            '^priceReload':pcreload,
            '^google':search,
            "^weather":weather,
            '^pc':pricecheck,
            '^fmyl':fml,
            '^fb':openBook,
            '^etym':etymology,
            '^ip':ip,
            '^circlejerk': cj,
            '^desktop':desktop,
            '^shootout':shootout,
            '^benchmark':shootout,
            '^imdb':imdb,
            '^bitcoin':bitcoin,
            '^tiny':tiny
            }

