import humanize
from datetime import datetime
import html
import re
import random
import praw
help = """^^ sends the previous line to twitter. Can't quote yourself either. ^^ n sends the nth line from the scrollback twitter. View with ^scroll. n is n places from the start of the scroll starting at 0. ^last gets the last tweet from Buttsworth. '^last user' gets the last tweet from user."""
badwords = ["bomb","jihad", "anal", "nigger", "loli", "global-jihad", "beatdownbrigade", "404chan", "genericus", "hussyvid", "pthc", "kdv", "r@ygold", "kiddy", "#ff","isis"]
tags = ["perwlcon", "perwl", "perl", "python"]

def getTwit(conn, user,idx):
        try:
            print("user=",user)
            result = conn.factory.api.GetUserTimeline(screen_name=user)[idx]
            print(result)
        except Exception as e:
            result = 'Could not get twitter ' + str(e)
        return result
def setTwitter(conn,data):
    try:
         conn.setName(data,data['fool'],data['words'][1],'twitter')
    except IndexError:
        conn.msg(data['chan'],'Usage is ^^settwitter twitterhandle')
def setTwit(conn, msg,data):
        try:
            result = conn.factory.api.PostUpdate(msg+" "+data['chan']).AsDict()
            link = "https://twitter.com/%s/status/%s"%(result['user']['screen_name'],result['id_str'])
            result['link_'] = link
            return result
            r = praw.Reddit(user_agent="perwl irc", client_id=conn.factory.keys['reddit_client_id'], client_secret=conn.factory.keys['reddit_client_id'], username=conn.factory.keys['reddit_user'], password=conn.factory.keys['reddit_pass'])
            r.subreddit('perwl').submit('%s: %s'%(data['chan'],msg),url=link)

            return result
        except Exception as e:
            conn.msg(data['chan'],'\0030,2Twitter\003 Could not update twitter: ' + str(e))
            return False

def removeTweet(conn, data):
    if data['fool'] in conn.factory.admins:
        try:
            pos = int(data['words'][2])
        except:
            pos =0
        t = getTwit(conn, "Buttsworth_",pos)
        conn.factory.api.DestroyStatus(t.id)
        conn.msg(data['chan'],"\0030,2Twitter\003 removed tweet: " + t.text)

def tweet(conn, data):
        if data['chan']  in conn.factory.ignores:
            return
#    if data['fool'] not in conn.banned and data['chan'] not in conn.ignores:
        if ("".join(conn.chans[data['chan']]['scroll'][len(conn.chans[data['chan']]) - 1].split())) != "":
            try:
                index = int(data['words'][1])
            except:
                index = -1
            if data['fool'] == conn.chans[data['chan']]['scroll'][index].split(':')[0]:
                conn.msg(data['chan'],"Can't quote yourself" + ('!' * (random.randint(0, 2))))
                return
            else:
                if len(data['words']) > 1:
                    toSend = conn.chans[data['chan']]['scroll'][int(data['words'][1])]
                else:
                    toSend = (conn.chans[data['chan']]['scroll'].pop())[:140]
                print(toSend)
                for i in tags:
                    toSend = toSend.replace(i, "#" + i)
                #toSend = ' '.join(map(lambda x: tag(x),toSend.split()))
                if any([x.lower() in toSend.lower() for x in badwords]) and data['fool'] not in data.factory.admins:
                    conn.msg(data['chan'],'Naughty words not allowed')
                    return
                if toSend.find("\001ACTION") != -1:
                    toSend = '*** ' + (toSend.replace(': \001ACTION', '', 1)[:-1])
                print(conn.chans[data['chan']]['users'])
                #for user in conn.chans[data['chan']]['users']:
                #    toSend = re.sub("(?i)"+user,'@'+user,toSend)
                r = setTwit(conn, toSend,data)
                if r:
                    conn.msg(data['chan'],'Sent to twitter '+r['link_'])
                else:
                    conn.msg(data['chan'],'Failed to send')

def last(conn, data):
    try:
        user = data['words'][1]
    except Exception as e:
        print(e)
        user = "Buttsworth_"
    idx = 0
    if len(data['words']) > 2 and data['words'][2].isdigit():
        idx = int(data['words'][2])

    t = getTwit(conn, user,idx)
    print(type(t))
    try:
        print(t.AsDict())
        #Wed May 22 01:56:44 +0000 2019
        conn.msg(data['chan'],"\0030,2Twitter\003 %s %s: %s %s" % (t.user.screen_name, humanize.naturaltime(datetime.utcnow() - datetime.strptime(t.created_at,'%a %b %d %H:%M:%S +0000 %Y')), html.unescape(t.text), "https://twitter.com/{}/status/{}".format(t.user.screen_name,t.id_str)))
    except Exception as e:
        conn.msg(data['chan'],str(e))

def twatter(conn, data):
    try:
       user = data['words'][1]
    except:
       user = "Buttsworth_"
    u = conn.factory.api.GetUser(user)
    conn.msg(data['chan'],"\0030,2Twitter\003 Info for user '%s' (@%s): Loc: %s; Url: %s; Statuses: %s; Followers: %s;" % (u.name, u.screen_name, u.location, u.url, u.statuses_count, u.followers_count))
    
triggers = {'^twat':tweet, '^^':tweet, '^last':last, '^untweet':removeTweet, '^twatter':twatter,'^settwitter':setTwitter}
