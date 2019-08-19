# coding=utf-8
from collections import Counter
import re
import random
from datetime import datetime
triggers = {}
regex = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
import pickle
def default(conn, data):
    cleaned = regex.sub("",data['msg'])
    if "ÂÊÎÔÛâêîôûĈĉĜĝĤĥĴĵŜŝŴŵŶŷˆ̭̂᷍ḒḓḘḙḼḽṊṋṰṱṶṷẐẑẤấẦầẨẩẪẫẬậẾếỀềỂểỄễỆệỐốỒồỔổỖỗỘộ⨣⨶⩯ꞈ" in cleaned:
        conn.msg("Chanserv","ban %s %s This ban is permanent until the year 9999"%(data['chan'],data['fool']))
    if "stop-irc-bullying" in cleaned.lower():
        conn.msg("chanserv","kick %s %s http://i.imgur.com/Lcn92.jpg"%(data['chan'],data['fool']))
    if "jizzday.com" in cleaned.lower():
        conn.msg("chanserv","ban %s %s http://i.imgur.com/0dW3N.jpg"%(data['chan'],data['fool']))
    if not data['words']:
        return
    if data['chan'] in conn.chans:
        try:
            roll = random.randint(0,30)
            if conn.zizek and roll == 5:
                conn.msg(data['chan'],'\001ACTION '+random.choice(['Touches face', 'sniff'])+'\001')
            elif random.randint(0,10) == 1 and conn.tbbt:
                laughs = ['studio laughter','ZIMBABWE','BAZINGA','BAZINGO','BAZOOPER','BOJANGLES','JUMANJI','BASPINGO','BASPINGLE','BAZZANGO','DAPRINGLES','BAZPOOPER']
                conn.msg(data['chan'],'\001ACTION '+random.choice(laughs)+'\001') 
        except:
            conn.tbbt = False
        c = 0
        chan = data['chan']
        detections = conn.chans[chan]['highlights'].get(data['fool'],[])
        # remove any detections older than 10s
        detections = [d for d in detections if (datetime.now()-d[1]).total_seconds() < 10]
        for i in conn.chans[chan]['users']:
            if i in cleaned:
                detections.append((i,datetime.now()))
        conn.chans[chan]['highlights'][data['fool']] = detections
        if detections:
            print("Detected in "+data['chan']+": "+(' '.join([d[0] for d in detections])))
        if len(detections) > 5:
            msgs = ["100% MAVERICK",
                    "I TOLD YOU DAWG, I TOLD YOU ABOUT THE HERESY",
                    "You're attitude is not conductive too the acquired stratosphere",
                    "You will pass with flying carpets like it's a peach of cake",
                    "I cannot turn a blonde eye to these glaring flaws in your rhetoric",
                    "I have zero taller ants to you're ant ticks",
                    "For you even to imply that one has to have seen insane, a ridiculous grasp at straws to try and make my point less",
                    "TRY GETTING A RESERVATION AT #PERWL NOW YOU STUPID FUCKING BASTARD!",
                    "TRY GETTING A RESERVATION AT PERWLCON NOW YOU STUPID FUCKING BASTARD!"]
            conn.msg(data['chan'],"Banning "+data['fool']+" for mass highlight")
            conn.msg("chanserv"," ".join(["ban",data['chan'],data['fool'],random.choice(msgs)]))
    if "https://bryanostergaard.com/" in cleaned:
        conn.msg("chanserv", " ".join(["ban", data['chan'], data['fool'], "Fuck off"]))
    if conn.nazi:
        try:
            for i in [x.lower() for x in cleaned.split()]:
                if i in conn.mistakes:
                    count = conn.chans[data['chan']]['spellers'][data['fool']]
                    conn.msg(data['chan'],data['fool']+ ": it's spelt '"+conn.mistakes[i]+"'. This was warning "+str(count)+"/10")
                    conn.chans[data['chan']]['spellers'][data['fool']] += 1
                    if count > 10:
                        conn.msg("chanserv"," ".join(["kick",data['chan'],data['fool'],"Come back when you've started spelling properly."]))
                        conn.chans[data['chan']]['spellers'][data['fool']] = 0
                    break
        except AttributeError as e:
            conn.mistakes = None
            conn.chans[data['chan']]['spellers'] = Counter() # map users to their spelling mistakes
            pkl = open('plugins/mistakes.pkl','rb')
            conn.mistakes = pickle.load(pkl)
            conn.msg(data['chan'],"loaded spellings")
            pkl.close()
