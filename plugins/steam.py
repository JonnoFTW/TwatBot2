import json
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse  import quote


help = "^steam <steamid> will get userinfo for the user" 
help2 = "Use ^setsteam <steamId> to associate your nick with a given steamId64. It will look like 76561XXXXXXXXXXXX"
def steam(conn, data):
    key = conn.factory.keys['steam_api_key']
    db = conn.getDB() 
    c = db.cursor()
    try:
        #An id or nick was provided
        id = data['words'][1]
        #Check if the is in the db
        if id.isdigit():
            pass
        else:
         try:
            n = data['words'][1]
         except:
            n = data['fool'] 
         x = conn.getName(n,'steamId')
         if x:
            id = x
         else:
            #Perhaps they are providing a user name?
            s = re.compile('var\sajaxFriendUrl\s\=\s\"http\:\/\/steamcommunity\.com\/actions\/AddFriendAjax\/(\d+)\"\;')
            try:
                f = urlopen("http://steamcommunity.com/id/" + quote(id)).read()
                id = s.findall(f)[0]
            except HTTPError:
                conn.msg(data['chan'],"No such user by that name")
                return
                
    except IndexError:
        #No id, perhaps they are stored
        id = conn.getName(data['fool'],'steam')
        if not id:
            conn.msg(data['chan'],"No steamId associated with this nick. "+help2)
            return
    except:
        conn.msg(data['chan'],"Please provide a steamId, or "+help2)
        return
    k = json.load(urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + key + "&steamids=" + id))
    if len(k['response']['players']) == 0:
        conn.msg(data['chan'],"No such user exists! Please specify a valid steamId64 ")
        print(k)
        return
    p = k["response"]["players"][0]
    if "primaryclanid" in p:
        #Get their clan name
        clan = "http://steamcommunity.com/gid/" + p["primaryclanid"]
        clanPage = urlopen(clan).read()
        s = re.compile(r'<title>\W+Steam Community :: Group :: (.*?)\W+<\/title>')
        try:
          clan = s.findall(clanPage)[0]
        except:
          clan = "Group Error"
    else: 
        clan = "None"
    if "gameextrainfo" in p:
        game = p["gameextrainfo"]
    else:
        game = "None"
    if "realname" in p:
        name = p["realname"]
    else:
        name = "None"
    if not "loccountrycode" in p:
        p["loccountrycode"] = "None"
    friends = []
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + key + "&steamid=" + p["steamid"] + "&relationship=friend"
    for i in json.load(urlopen(url))["friendslist"]["friends"]:
        friends.append(i['steamid'])
    f = json.load(urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + key + "&steamids=" + (','.join(friends))))
    friends = []
    for i in f["response"]["players"]:
        friends.append(i["personaname"])
    conn.msg(data['chan'],"User: %s, Realname: %s, Country: %s, Playing: %s, Clan: %s, Friends: [%s]" % 
                 (p["personaname"], name, p["loccountrycode"], game, clan, '; '.join(friends[:10])))

def setsteam(conn, data):
    #Associate a nick with a steam id for later use
    try:
        conn.setName(data,data['fool'],data['words'][1],'steam')
    except IndexError:
        conn.msg(data['chan'],'Please provide a steamId64 to associate your nick with. http://steamidfinder.com')
        
triggers = {"^steam":steam, '^setsteam':setsteam}
