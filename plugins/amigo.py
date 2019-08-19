
import pickle
import re
import socket
import uuid
import subprocess
import random
from datetime import datetime
from itertools import cycle
import time
import re
help = "Copies the functionality of amigo"
def badfortune(conn,data):
    with open('/home/jonno/trolldb.txt','rb') as fh:
        msgs = fh.read().decode('cp1252').replace('\r\n','\n').split(r'%')
        conn.msg(data['chan'], re.sub(r'\s+',' ', ' '.join(random.choice(msgs).splitlines())).strip())
def rekt(conn,data):
    conn.msg(data['chan'],random.choice(['rekt','smasht','de_molished','de_stroyed','wrekt','owned']))
def noice(conn,data):
    conn.msg(data['chan'],"noice")
def rip(conn,data):
        conn.msg(data['chan'],"Yeah, RIP")
def welcome(conn, data):
    try:
      user  = data['words'][1]+": " 
    except:
      user = ""
    conn.msg(data['chan'],user+"Welcome. Welcome to "+data['chan']+". You have chosen, or been chosen, to relocate to one of our finest remaining IRC channels. I thought so much of "+data['chan']+" that I elected to establish my Administration here in the Citadel so thoughtfully provided by our SysAdmins. I have been proud to call "+data['chan']+" my home. And so, whether you are here to stay, or passing through on your way to parts unknown, welcome to "+data['chan'])
def suptime(conn, data):
   conn.msg(data['chan'],subprocess.check_output(["uptime"]).decode('utf-8'))
def uid(conn, data):
   conn.msg(data['chan'],str(uuid.uuid1()).upper())
def fortune(conn, data):
    try:
      for i in subprocess.check_output(["fortune", "-s"], shell=True, stderr=subprocess.STDOUT).decode('utf-8').splitlines():
        conn.msg(data['chan'],i.replace("\x03", ""))
    except subprocess.CalledProcessError as e:
        conn.msg(data['chan'], e.output.decode('utf-8'))
def uname(conn, data):
    conn.msg(data['chan'],subprocess.check_output(["uname", "-a"]).decode('utf-8'))

def rconpl(conn,data):
    conn.msg(data['chan'],subprocess.check_output("/usr/bin/rconpl",shell=True))
def w(conn, data):
  if data['fool'] not in conn.factory.admins:
      return
  running = subprocess.check_output(["w", "-hsf"]).decode('utf-8').splitlines()
  users = dict()
  for i in running:
    j = i.split()
    u = j[0]
    proc = (' '.join(j[3:]))
    if u in users:
        users[u] = users[u] + ', ' + proc
    else:
        users[u] = proc
  for i in list(users.items()):
    conn.msg(data['chan'],i[0] + ': ' + i[1])
                                          
def ti(conn, data):
    conn.msg(data['chan'],time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))
    
def sdate(conn, data):
    then = datetime(1993, 8, 31, 0, 0, 0)
    now = datetime.now()
    conn.msg(data['chan'],time.strftime('%a Sep ' + str((now - then).days) + ' %H:%M:%S %Z 1993', time.localtime()))
def roulette(conn, data):
    if len(data['words']) == 3 and data['fool'] in conn.factory.admins:
        #get two users
        ua = data['words'][1]
        ub = data['words'][2]
        if not all(u in conn.chans[data['chan']]['users'] for u in [ua,ub]) or ua.lower() == ub.lower():
            conn.msg(data['chan'], "Both users must be in the channel and not the same")
        conn.msg(data['chan'],'\001ACTION Comrades {} and {} have volunteered to play Russian Roulette. A single round is loaded into the revolver\001'.format(ua,ub))
        chamber = random.randint(1,6)
        print("rolled",chamber)
        pos = 1
        it = cycle([ua,ub])
        while True:
            player = next(it)
            time.sleep(1)

            conn.msg(data['chan'],'\001ACTION places the revolver to {}\'s head and pulls the trigger {}'.format(player, '*BANG*' if pos == chamber else '*click*'))
            if pos == chamber:
                conn.msg(data['chan'], '.k {} you died at sports'.format(player))
                break
            pos +=1
        return
    conn.msg(data['chan'],'\001ACTION Loads a single round into the revolver and places it to ' + data['fool'] + '\'s head\001')
    if random.randint(1, 6) == 6:
      conn.msg(data['chan'],'\001ACTION *BANG*\001')
      conn.msg(data['chan'],'.kb ' + data['fool']+ " BOOM HEADSHOT")
    else:
      conn.msg(data['chan'],'\001ACTION *click*\001')
def dig(conn, data):
   try:
     try:
       inet = socket.AF_INET
       if data['words'][1].find(":") != -1:
          inet = socket.AF_INET6
       socket.inet_pton(inet,data['words'][1])
       ip = "-x"
     except socket.error:
       if not re.match(r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*', data['words'][1]):
           conn.msg(data['chan'],'Please enter a valid domain name')
           return
       ip = " "
     ass = subprocess.check_output(["dig", ip, data['words'][1], "+short"]).decode('ascii').split('\n')
     conn.msg(data['chan'],', '.join(ass)[:-2])
   except IndexError as e :
     conn.msg(data['chan'],"Please provide a domain to search for")
def trendy(conn, data):
    # Be sure to have a trendy file ready
    trends = []
    for line in open('plugins/trendy'):
       trends.append(line[:-1])
    l = len(trends) - 1
    conn.msg(data['chan'],' '.join([trends[random.randint(0, l)], trends[random.randint(0, l)], trends[random.randint(0, l)]]))
def uptime(conn, data):
    conn.msg(data['chan'],str(datetime.now() - conn.factory.uptime))

def hipster(conn, data):
   hip = []
   for line in open('plugins/hipster'):
      hip.append(line[:-1])
   l = len(hip) - 1
   out = []
   while(len((' '.join(out).split())) < 5):
      out.append(hip[random.randint(0, l)])
   conn.msg(data['chan'],' '.join(out))
   
def asl(conn, data):
#   conn.msg(data['chan'],'new behaviour!')
    places = ['sa', 'hawaii', 'israel', 'nigeria', 'aus', 'cali', 'nyc', 'nsw', 'fl', 'uk', 'france', 'russia', 'germany', 'japan', 'china', 'nz']
    conn.msg(data['chan'],'/'.join([str(random.randint(8, 30)), random.choice(['m', 'f']), random.choice(places)]))

def flip(conn, data):
   if random.randint(0, 1): 
      msg = 'Heads'
   else:
      msg = 'Tails'
   conn.msg(data['chan'],'A coin is flipped, ' + msg)
def roll(conn, data):
   num =1
   sides = 6
   try:
       num = int(data['words'][1])
       sides = int(data['words'][2])
   except:
       pass
   if num  < 1 or num > 32:
       num = 1
   if sides < 1:
       sides =6
   sep = 'is'
   if num > 1:
     sep = 'are'
   conn.msg(data['chan'],'%d %d sided dice %s rolled: %s'%(num,sides,sep, ', '.join([str(random.randint(1, sides))  for i in range(0,num)])))

def joke(conn, data):
   jokes = []
   buf = []
   for line in open('plugins/jokes.txt'):
      if line.split() == []:
         if buf != []:
            jokes.append(buf)
            buf = []
      else:
         buf.append(line.strip())
   for i in random.choice(jokes):
      conn.msg(data['chan'],i)

def doubles(conn, data):
   db = conn.getDB()
   cursor = db.cursor()
   try:
     if data['words'][1]:
       if data['words'][1] == "top":
           #print the top 3 users
           cursor.execute("SELECT *  FROM doubles order by quads desc, trips desc, dubs desc, misses desc limit 0,3")
           conn.msg(data['chan'],"Top doubles users are: ")
           for i in cursor.fetchall():
            conn.msg(data['chan'],i[0] + ': Dubs:' + str(i[1]) + ' Trips:' + str(i[2]) + ' Quads:' + str(i[3]) + ' Misses:' + str(i[4]))
       elif data['words'][1] == "losers":
           cursor.execute("SELECT *  FROM doubles order by misses desc limit 0,3")
           conn.msg(data['chan'],"Top losers users are: ")
           for i in cursor.fetchall():
            conn.msg(data['chan'],i[0] + ': Dubs:' + str(i[1]) + ' Trips:' + str(i[2]) + ' Quads:' + str(i[3]) + ' Misses:' + str(i[4]))
       else:
           print("Getting user")
           # Get the user specified
           cursor.execute("SELECT * FROM doubles WHERE `nick` = '%s'" % (db.escape_string(data['words'][1])))
           x = cursor.fetchone()
           if x:
             print(cursor._last_executed)
             print(x)
             conn.msg(data['chan'],data['words'][1] + ': Dubs:' + str(x[1]) + ' Trips:' + str(x[2]) + ' Quads:' + str(x[3]) + ' Misses:' + str(x[4]))
           else:
             conn.msg(data['chan'],'No results for user')
   except IndexError:
    n = str(conn.dubs.count).zfill(4)
    count = 0
    for i in n[::-1]:
       if i == n[-1]:
          count += 1
       else:
          break
    out = {1:" ", 2:", DOUBLES", 3:", TRIPS", 4:", QUADS"}[count]
    c = {1:'misses', 2:'dubs', 3:'trips', 4:'quads'}[count]
    nick = db.escape_string(data['fool'])
    # if "noxialis" in data['fool'].lower():
        # if random.randint(0,2) == 0:
            # conn.msg(data['chan'],"Critical error, scores reset")
            # cursor.execute("DELETE FROM `doubles` WHERE `nick` = '"+nick+"';")
    vals = [nick, 0, 0, 0, 0]
    vals[count] = 1
    vals = str(tuple(vals))
    cursor.execute("""INSERT INTO `doubles` (`nick`,`misses`,`dubs`,`trips`,`quads`) 
                        VALUES %s 
                        ON DUPLICATE KEY UPDATE `%s` = `%s` +1 ;""" % (vals, c, c))
    print(cursor._last_executed)
    print(count)
    if count > 1:
        conn.msg(data['chan'],"You rolled " + n + out)
    else:
        conn.notice("You rolled " + n + out)
        
def lines(conn, data):
    db = conn.getDB()
    cursor = db.cursor()
    try:
        nick = data['words'][1]
    except IndexError:
        nick = data['fool']
    cursor.execute("SELECT COUNT(`nick`) FROM `logs` WHERE `nick` = '%s'" % (db.escape_string(nick)))
    conn.msg(data['chan'],"Lines from " + nick + ": " + str(cursor.fetchone()[0]))
   
def latin(conn, data):
    try:
      if conn.latin:
        #Print a random latin phrase
        key = random.choice(list(conn.latin.keys()))
        print(key)
        conn.msg(data['chan'],key + ' ----> ' + conn.latin[key])
    except AttributeError as e:
      conn.latin = None
      pkl = open('plugins/latin.pkl', 'rb') 
      conn.latin = pickle.load(pkl)
      conn.msg(data['chan'],"Loaded phrases")
      pkl.close()
      latin(conn)
def genre(conn, data):
    prefixes = ['enterprise','', 'post', 'indie', 'avant-garde', 'nautical', 'break', 'wub', 'chip', 'vintage', 'classic', 'virtuosic', 'death', 'instrumental', 'british', 'industrial', 'thrash', 'japanese', 'J', 'K', 'acoustic', 'progressive', 'power', 'glam', 'melodic', 'new wave', 'german', 'gothic', 'symphonic', 'grind', 'synth', 'minimal', 'psychedelic', 'brutal', 'sexy', 'easy listening', 'christian', 'anime', 'stoner', 'comedy', 'sad', 'christmas', 'neo', 'russian', 'finnish', 'summer', 'underground', 'dream', 'pagan', 'minimal', 'ambient', 'nu', 'speed', 'contemporary', 'alt', 'acid', 'english', 'kvlt', 'cult', 'mu', 'raw', 'norwegian', 'viking', 'porn']
    suffixes = ['core', '', 'step', 'groove', 'noise']
    gens = ['folk', 'ambient', 'electronica', 'funk', 'hip-hop', 'dance', 'pop', 'trance', 'indie', 'soul', 'hard', 'lounge', 'blues', 'classical', 'grunge', '/mu/core', 'emo', 'rap', 'rock', 'punk', 'alternative', 'nautical', 'electro', 'swing', 'screamo', 'jazz', 'reggae', 'metal', 'classical', 'math', 'nerd', 'country', 'western', 'dub', "drum 'n' bass", 'celtic', 'shoegaze']
    x = random.choice(prefixes)
    if x:
        x += '-'
        if random.randint(0, 2) == 1:
            x += random.choice(prefixes) + '-'
    x += random.choice(gens)
    if random.randint(0, 3) == 1:
        x += random.choice(suffixes)
    
    conn.msg(data['chan'],x)
def newage(conn,data):
    terms = ['Frequency','Vibration','Moonchild','Flowerchild','Freedom','Energy','Enlightened','Ionization','Heuristics','Galactic','Flower-child','HAARP','DARPA','Dianetics','Nexus','Earth','Gaia','Life','Dream','Message','DNA','Ascension','Fully Fledged','God-inspired','Become','Creating','Soul','Solstice','Soulstice','Aura','Mayan','Planetary','Synergy','Mystical','Spiritual','Evolution','Creation','Attraction','Activation','Light-body','Cosmic','Sequential','Dimension','5th-Dimension','Galactic-federation','Archangelic','Waves','Telepathic','Omen']
    conn.msg(data['chan'], ' '.join([random.choice(terms),random.choice(terms),random.choice(terms)]))
def define(conn,data):
    try:
     #   conn.msg(data['chan'],subprocess.check_output(["dict",data['words'][1]],stderr=subprocess.STDOUT))
        pass
    except IndexError:
        conn.msg(data['chan'],"Usage is ^define word")
def boi(conn, data):
    conn.msg(data['chan'],'🅱️ o'+('i'*data['msg'].count('e')))
def lmao(conn, data):
    conn.msg(data['chan'], 'lmao')
def piss(conn,data):
    to = data['fool']
    if data['fool'] in conn.factory.admins and len(data['words'][1]) and data['words'][1] in conn.chans[data['chan']]['users']:
        to = data['words'][1]
    conn.msg(data['chan'],to+": What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces.")
triggers = { '^fortune':fortune,
             '^uname':uname,
             '^piss':piss,
             '^welcome':welcome,
             '^newage':newage,
 #            '^lines':lines,
             '^time':ti,
             '^w':w,
             '^uuid':uid,
             '^sdate':sdate,
             '^roulette':roulette,
             '^trendy':trendy,
             '^dig':dig,
             '^uptime':uptime,
             '^hipster':hipster,
             'asl':asl,
             '^suptime':suptime,
             '^roll':roll,
             '^joke':joke,
             '^flip':flip,
#             '^doubles':doubles,
             '^latin':latin,
             '^genre':genre,
             'rip':rip,
             'RIP':rip,
             '^players':rconpl,
             '^define': define,
             'noice':noice,
             'rekt':rekt,
             '^rekt':rekt,
            'ye':boi,
            'ayy': lmao,
            '^enlighten': badfortune
}
    
