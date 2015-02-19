#!/usr/bin/python2.7
'''
Created on 10/07/2012

@author: Jonathan Mackenzie

You will need to create a database and specify it in 
the keys file. To create the database use:

create user 'mysql_user'@'localhost' identified by 'some_pw';
create table tell(
  `sender` varchar(32) NOT NULL,
  `to` varchar(32) NOT NULL,
  `message` text not null,
  `time` datetime not null);
alter table service_nicks ADD PRIMARY KEY(irc_nick,service);

create table service_nicks(
  irc_nick varchar(32) not null,
  service varchar(32) not null,
  service_nick varchar(32) not null);

'''

from twisted.internet import reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.words.protocols import irc

from plugins import *
from collections import deque
from datetime import datetime,date

import os,sys
import time
import MySQLdb
import MySQLdb.cursors
import twitter
pluginList = [ web, mueval, amigo, ban,chans,  help, tell, scroll,
    tweet,  lastfm, fullwidth, counterstrike, steam, privilege,names]
adminPlugins = [ joinpart, ban, quit , stat, reddit]

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass
def fileToDict(file):
    out = {} 
    with open(file) as f:
        for i in f.readlines():
            j = i.split()
            out[j[0]] = ' '.join(j[1:])
    return out
keys = fileToDict('keys')
api = twitter.Api(
    keys['consumer_key'],
    keys['consumer_secret'],
    keys['access_token_key'],
    keys['access_token_secret']
    )
def readFile(f):
    lines = []
    with open(f) as f:
        lines = map(lambda x: x.rstrip(),f.readlines())
    return lines

class TwatBot2(irc.IRCClient):
    nickname    = "TwatBot"
    client      = "IRC BOAT"
    realname    = "Segwinton Buttsworth Jr."
    username    = "gar.fucks"
    userinfo    = "Fruity Event Loops"
    versionName = "Twisted and Shit"
    versionName = "0.1"
    versionEnv  = "Help I'm trapped in a sandbox"
    sourceURL   = "http://github.com/JonnoFTW"
    lineRate    = 1
    vhost       = "given.0"
    nazi        = False
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
#        print "Connected to",self.hostname
        self.chans = dict()
        cu = self.getDB().cursor()
        cu.execute("SELECT `to` FROM tell")
        s = cu.fetchall()
        self.tells = set()
        for i in s:
          self.tells.add(i[0])
        self.plugins = pluginList + adminPlugins
        
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
    
    def seen(self, user):
        if user in self.tells:
            self.notice(user,'You have unread messages, type ^read to read them')
            self.tells.remove(user)
        
    
    def joined(self,chan):
        print "Joined: "+chan
        self.chans[chan] = dict()
        self.chans[chan]['users']  = set()
        self.chans[chan]['scroll'] = deque([],10)
        self.chans[chan]['kicks']  = deque([],5)
        self.sendLine("WHO %s" % chan)
    def kickedFrom(self,chan,kicker,message):
        print "Kicked from %s by %s"%(chan,kicker)
        del(self.chans[chan])
    def topicUpdated(self, user, channel, newTopic):
        print "%s: %s changed topic to %s"%(channel,user,newTopic)
    def signedOn(self):
        self.msg("Nickserv", "identify "+self.factory.nickpass)
        for i in self.factory.channels:
            print "Joining "+i
            self.join(i, None)
            
    def noticed(self,user,channel,msg):
        print channel," NOTICE:","<"+user+">",msg
        self.seen(user)

    def msg(self, user, message, length=None):
        print "SENDING: <%s> %s" % (user,message)
        try:
            irc.IRCClient.msg(self,user,message.encode('utf-8'),length)
        except:
            irc.IRCClient.msg(self,user,message,length)
    def notice(self, user, message):
        print "NOTICE: <%s> %s" % (user,message)
        irc.IRCClient.notice(self,user,message.encode('utf-8'))

       
    def privmsg(self,user,channel,msg):
        print channel,time.strftime("%H:%M:%S",time.localtime()),":","<"+user+">",msg
        if len(msg.split()) == 0:
            return
        cmd = msg.split()[0]

        data = {'user':self.getNick(user),'chan':channel,"msg":msg, 'words':msg.split(),'fool':self.getNick(user)}
        if msg.strip()[0] != '^' and channel != self.nickname :
            self.chans[channel]['scroll'].append(data['user']+": "+msg)
        if channel == self.nickname:
            data['chan'] = data['fool']
        self.seen(data['user'])
        if data['user'] in self.factory.admins:
            if data['words'][0] == '^reload':
                try:
                    g = dict(globals())
                    for i in g:
                        if data['words'][1] == i:
                            reload(globals()[data['words'][1]])
                            self.msg(data['chan'],"Module "+i+" reloaded")
                            break
                except Exception, e:
                    self.msg(data['chan'],str(e))
            for i in adminPlugins:
                if cmd in i.triggers:
                    i.triggers[cmd](self,data)
                    return
        if data['fool'] not in self.factory.ignores:
            for i in pluginList:
                if cmd in i.triggers:
                    i.triggers[cmd](self,data)
        default.default(self,data)
        
    
    def alterColliderNick(self,nick):
        return nick + '`'
    
    def getNick(self, user):
        return user.split('!')[0]
    
    def userRenamed(self,old, new):
        print "%s changed nick to %s" % (old,new)
        for i in self.chans:
            try:
                self.chans[i]['users'].remove(old)
                self.chans[i]['users'].add(new)
            except KeyError:
                pass
        
    def userKicked(self,kickee, channel, kicker, message):
        kickee = self.getNick(kickee)
        try:
            self.chans[channel]['users'].remove(kickee)
            print "%s :  %s kicked by %s, %s at %s" % (channel,kickee, kicker, message,time.time()),
            # Only store the most recent kick
            t = []
            for i,j,k in self.chans[channel]['kicks']:
                if k != kickee:
                   t.append((i,j,k))
            self.chans[channel]['kicks'] = t
            self.chans[channel]['kicks'].append((kicker,time.time(),kickee))
            self.detectMassKick(channel)
        except KeyError:
            pass
        
    def detectMassKick(self,channel):
            kickers = {}
            print "Kicks are:", self.chans[channel]['kicks']
            for i,j,k in self.chans[channel]['kicks']:
                try:
                    kickers[i].append(j)
                except:
                    kickers[i] = [j]
            for i,j in kickers.iteritems():
                j.sort()
                t = j[-1] - j[0]
                count = len(j)
                print "%s: %d kicks in %d, %s"%(i,count, t, str(j))
                if j[-1] - j[0] < 10 and count >= 3:
                    self.msg(channel, "Mass kick by "+i+" detected")
                    self.msg('chanserv','akick '+channel+' add '+i+' masskick')
            
    def userLeft(self, user, channel):
        user = self.getNick(user)
        print "%s : %s left" % (channel,user)
        try:
            self.chans[channel]['users'].remove(user)
        except KeyError:
            pass
        
    def userJoined(self,user,channel):
        user = self.getNick(user)
        print "%s : %s joined" % (channel,user)
        self.chans[channel]['users'].add(user)
        if len(user) > 15 and channel == "#perwl":
            pass
            #self.kick(channel,user,"Please use a nick with less than 15 chars")
        if user in self.factory.greets:
            self.msg(channel,user+": "+self.factory.greets[user])
        self.seen(user)
        
    def userQuit(self, user, msg):
        user = self.getNick(user)
        print "%s quit" % user
        for i in self.chans:
            try:
                self.chans[i]['users'].remove(user)
            except KeyError:
                pass 
            
    def irc_RPL_WHOREPLY(self, pref, param):
        self.chans[param[1]]['users'].add(param[5])
    
    def irc_RPL_TOPIC(self,prefix,params):
        self.chans[params[1]]['topic'] = params[2]

    def topicUpdated(self,user,channel,topic):
        print channel,"TOPIC: ",topic
        self.chans[channel]['topic'] = topic
    def getDB(self):
        return MySQLdb.connect (host="localhost",user=keys['mysql_user'],passwd=keys['mysql_pass'],db=keys['mysql_db'])   

    def setName(self,data,fool,name,field):
        return names.setName(self,data,fool,name,field)
    def getName(self,name,field):
        return names.getName(self,name,field)
                                
class BotFactory(ReconnectingClientFactory):
    def __init__(self,chans,nickpass):
        self.uptime  = datetime.now()
        print "Time",time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.channels = chans
        self.admins = readFile('admins')
        print self.admins
        self.keys = keys
        self.greets = fileToDict('greets')
        self.ignores = set(readFile('ignores'))
        self.nickpass  = nickpass
        self.api = twitter.Api(
            keys['consumer_key'],
            keys['consumer_secret'],
            keys['access_token_key'],
            keys['access_token_secret']
            )
    def buildProtocol(self,addr):
        p = TwatBot2()
        p.factory = self
        self.resetDelay()
        self.p = p
        return p
    
    def clientConnectionLost(self,connector,reason):
        print time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()),"Connection lost:",reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
          
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed:",reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
       
class GitListener(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
    def dataReceived(self, data):   
        p = self.transport.getPeer()
        print "connection from",p,data
        if p.host != "127.0.0.1":
            return
        if data.strip()[0] == '.':
            return
        elif data.strip()[0] == '#':
            self.factory.bot.p.msg(data.split()[0],' '.join(data.split()[1:]))
        else:
            for i in self.factory.echoTo:
                self.factory.bot.p.msg(i,data)
    
class GitFactory(protocol.Factory):
    def __init__(self,bot , echoers = [],):
        self.echoTo = echoers
        self.bot = bot
    def buildProtocol(self,addr):
        return GitListener(self)
        
if __name__ == "__main__":
    print sys.argv
    if len(sys.argv) > 2:
        server = sys.argv[1]
        chans = sys.argv[2:]
    else:
        server = "irc.rizon.net"
        chans = ["#perwl","#pharmaceuticals",'#/fit/']
    print "Joining",chans,server
    f = BotFactory(chans,keys['nickpass'])
    reactor.connectTCP(server,6667,f)
    if "#perwl" in chans:
        print "Listening"
        g = GitFactory(f,["#perwl"])
        reactor.listenTCP(6666,g,interface='127.0.0.1')
    reactor.run()


