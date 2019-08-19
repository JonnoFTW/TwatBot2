import time
import datetime
import random
from valve import rcon
import re
help = "Command line Counter Strike: Source"

def cod(conn, data):
    ends =  ['','','xXx','XXX','X','x','XxX','.:.',':.','-=','-=-','=-=']
    ends2 = ['','','xXx','XXX','X','x','XxX','.:.','.:','=-','-=-','=-=']
    year = datetime.datetime.today().year
    suff  = ['MASTER','','','','M4STER','MA$T3R',random.randint(10,13),random.randint(year-14,year-9),str(random.randint(year-14,year-9)%100).zfill(2)]
    seps = [' ','x','-','_',' \'n\' ']
    f = random.randint(0,len(ends)-1)
    parts = ['b1g','clutch','smoke','yolo','#YOLO','sn1per','RAMBO','IND','death','d34th','DEATH','mlg','MLG','n0sc0pes','qu1k-sc0pe','pr0','hArD-Sc0pe','dope','scope','sc0pes','s1lent','aSsaSs1n','bong','b0ng','bonG','BonG','ripper','r!pper','r1pp3r','sw4g','b0nG','420','42O','w33d','t0kes','tokes','tokez'];
    s = random.choice(suff)
    t = ''
    if s:
        t = random.choice(seps)
    conn.msg(data['chan'],ends[f]+ random.choice(parts) + random.choice(parts) +t+ends2[f])

  #  conn.msg(data['chan'],random.choice(ends)+(random.choice(seps).join([random.choice(parts),random.choice(parts)]))+random.choice(ends))
def ff(conn, data):
    conn.msg(data['chan'],"\002[SM] Friendly fire is disabled.\002")
   
def thetime(conn, data):
    conn.msg(data['chan'],time.strftime("%H:%M:%S (%s)",time.localtime()))

def timeleft(conn, data):
    conn.msg(data['chan'], do_rcon(conn, 'timeleft').strip())
#    conn.msg(data['chan'],time.strftime("[SM] Time remaining for map: %M:%S",(time.gmtime((20*60)-(time.time() % (20*60))))))

def rank(conn, data):
    u = len(conn.chans[data['chan']]['users'])
    conn.msg(data['chan'],"Your rank is: "+str(random.randint(1,u))+"/"+str(u))

def statsme(conn, data):
    stats = ["p90 pub hero","deagle hero","awp whore","team flasher",
           "meat shield","gary","knif crab","DUAL AKIMBO","\002100% MAVERICK\002",
            "cv-47 clutch champion","GLOCKenspiel","happy camper",
            "grrgrgrgrgrgrgr","(gary)","long A rusher","afk","naked",
            "clarion burst fire headshot","bhopping scout master race","MP5 navy SEAL",
            "l33t kr3w","pot plant"]
    conn.msg(data['chan'],data['fool']+ " status: "+random.choice(stats))
   
def nextmap(conn, data):
#    updateMap(conn)
#    if len(conn.maps) == 1:
#        conn.msg(data['chan'],"This is the last round")
#        return
#    if len(conn.maps) == 0:
#        resetmaps(conn)
    nm  = do_rcon(conn, 'nextmap')
    conn.msg(data['chan'],nm)
def players(conn, data):
    players = re.findall(r'^players\s+:\s(.*)$', do_rcon(conn, 'status'), re.M)[0]
    conn.msg(data['chan'],"[SM] Players: "+players)
def bhop(conn, data):
    players = re.findall(r'^hostname:\s(.*)$', do_rcon(conn, 'status'), re.M)[0]
    conn.msg(data['chan'],"[SM] "+players)
def do_rcon(conn, cmd):
    addr = ('bhop.rip', 27015)
    pw = conn.factory.keys['rcon_pw']
    rcon.RCONMessage.ENCODING = 'utf-8'
    return rcon.execute(addr,pw,cmd)

def currentmap(conn, data):
#    updateMap(conn)

    map = re.findall(r'^map\s+:\s(\w+) ',do_rcon(conn,'status'), re.M)[0]
    conn.msg(data['chan'],"[SM] Current map is: "+map)

def updateMap(conn):
    try:
        print("Rounds since last checked: " + str( int( (time.time() - conn.nextMap) / (20*60))-1))
        print("Map list is: "+ (', '.join(conn.maps)))
        for i in range(int((time.time() - conn.nextMap)/(20*60))-1):
            if len(conn.maps) == 0:
                resetmaps(conn)
            conn.maps.pop(0)
    except AttributeError:
        resetmaps(conn)
        
def resetmaps(conn):
    try:
        if time.time() > conn.nextMap:
            conn.nextMap = time.time() + (time.time() % (20*60))
    except AttributeError:
        conn.nextMap = time.time() + (time.time() % (20*60))
    conn.lastChecked = time.time()
    maps = ["cs_office","cs_assault","de_dust2","de_aztec","de_inferno","cs_italy","de_train","de_nuke","fy_iceworld","de_dust"]
    random.shuffle(maps)
    conn.maps = maps

def gg(conn, data):
    conn.msg(data['chan'],"gg")
def dank(conn, data):
    conn.msg(data['chan'],"memes")
triggers ={  'ff':ff,
             '^cod':cod,
             'dank':dank,
             'gg':gg,
             'thetime':thetime,
             'rank':rank,
             'statsme':statsme,
             'timeleft':timeleft,
             'nextmap':nextmap,
             'players': players,
             'bhop': bhop,
             'currentmap':currentmap}
