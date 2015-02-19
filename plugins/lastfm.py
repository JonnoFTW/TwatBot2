# -*- coding: utf-8 -*-

from urllib2 import urlopen
from urllib  import quote, quote_plus, urlencode
import json

help = "Various functions for last.fm. Use ^np <user> to get a users last played track." 

def compare(conn,data):
    n1 = n2 = ""
    l = len(data['words'])
    if l == 1:
        conn.msg(data['chan'],"usage is ^compare <user1> <user2>. If you omit 1 name, it will compare yourself and the other person")
        return
    if l == 2:
        n1 = conn.getName(data['fool'],'lastfm')
        n2 = conn.getName(data['words'][1],'lastfm')
    elif l >= 3:
        print data
        n1 = conn.getName(data['words'][1],'lastfm')
        n2 = conn.getName(data['words'][2],'lastfm')
    url = "http://ws.audioscrobbler.com/2.0/?method=tasteometer.compare&format=json&api_key=%s&type1=user&type2=user&value1=%s&value2=%s"%(conn.factory.keys['lastfm_api_key'],n1,n2)
    print url
    u = json.load(urlopen(url))
    input = u['comparison']['input']['user']
    result = u['comparison']['result']
    artists = ["None"]
    matches = 0
    try:
        matches = result['artists']['@attr']['matches']
        artists = []
        for i in result['artists']['artist']:
            artists.append(i["name"].encode('utf-8'))
    except:
        pass
    conn.msg(data['chan'],u"\0030,4Last.fm\003 Comparison of {} and {}. Score: {:.2%}, matches: {}, common artists: {}".format(input[0]['name'], input[1]['name'],float(result['score']),matches,', '.join(artists)))
                        
        
def np(conn, data):
    #get now playing info for a user
    key = conn.factory.keys['lastfm_api_key']
    try:
        n = data['words'][1]
    except:
        n = data['fool']
    name = conn.getName(n,'lastfm')
#    name = n
    #Get the users now playing shit
    u = json.load(urlopen("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+quote(name.encode("utf-8"))+"&format=json&api_key="+key))
    try:
        if u['recenttracks']['total'] == '0':
            conn.msg(data['chan'],"This user (%s) has nothing played"%(name))
#            print u
            return
    except KeyError: 
        pass
    try:
#        print u
        track = u['recenttracks']['track'][0]
    except KeyError:
        if 'message' in u:
            conn.msg(data['chan'],u['message']+", error:"+u['error']+", user"+name)
        else:
            conn.msg(data['chan'],"No user by that name")
        return
    urls = [{'method':'track.gettoptags',
             'album':track['album']['#text'].encode("utf-8"),
             'track':track['name'].encode("utf-8")
             },
            {'method':'artist.gettoptags'}]
    for i in urls:
        i['format'] = 'json'
        i['autocorrect'] = 1
        i['artist'] =  track['artist']['#text'].encode("utf-8")
        i['api_key'] = key
    tags = []
    for url in urls:
      try:
          t = json.load(urlopen("http://ws.audioscrobbler.com/2.0/?"+urlencode(url)))
          tags = ', '.join(map(lambda x:x['name'],t['toptags']['tag'][:5]))
          break
      except (TypeError, KeyError):
          tags = 'No tags available' 
          continue
    if track['album']['#text']:
        track['album']['#text'] = " from '"+ track['album']['#text']+"'"   
    curr = "is now pegging"
    if '@attr' not in track:
        curr = "last pegged"
#    print json.dumps(track,indent=4)
    conn.msg(data['chan'],"\0030,4Last.fm\003 User '%s' %s to '%s' by '%s'%s, (%s)" % (name,curr,track['name'],track['artist']['#text'],track['album']['#text'],tags)) 

def setlastfm(conn, data):
    #Associate your nick with a username
    try:
        conn.setName(data,data['fool'],data['words'][1],'lastfm')
    except IndexError:
        print e
        conn.msg(data['chan'],"Please provide your lastfm username")
def lastfm(conn, data):
    #Get info about an artists or something
    conn.msg(data['chan'],"Not yet implemented")

def charts(conn, data):
    user = ''
    if len(data['words']) > 1:
        user = conn.getName(data['words'][1],'lastfm')
    args = {'method':'chart.gettopartists','format':'json','limit':10,'api_key':conn.factory.keys['lastfm_api_key']}   
    key = "artists"
    if user:
        args['method'] = "user.getweeklyartistchart"
        args['user']   = user
        key = "weeklyartistchart"
    u = json.load(urlopen("http://ws.audioscrobbler.com/2.0/?%s"%(urlencode(args))))
    artists = []
    for i in u[key]['artist']:
        try:
            artists.append("{}: {:,.0f}".format(i['name'],int(i['playcount'])))
            print artists[-1]
        except Exception, e:
            print i['name'], e
            pass
    pre = ' '
    if user:
        pre = ' this week for'
    conn.msg(data['chan'],'\0030,4Last.fm\003 Top Artists%s %s: '%(pre,user)+(' \002|\002 '.join(artists)))

triggers = {'^np':np,'^setlastfm':setlastfm, '^lastfm':lastfm,"^compare":compare,'^charts':charts}
