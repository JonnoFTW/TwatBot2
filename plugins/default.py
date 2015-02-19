# coding=utf-8
from collections import Counter
import re
import random
triggers = {}
regex = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
import cPickle
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
            if random.randint(0,10) == 1 and conn.tbbt:
                laughs = ['studio laughter','ZIMBABWE','BAZINGA','BAZINGO','BAZOOPER','BOJANGLES','JUMANJI','BASPINGO','BASPINGLE','BAZZANGO','DAPRINGLES','BAZPOOPER']
                conn.msg(data['chan'],'\001ACTION '+random.choice(laughs)+'\001') 
        except:
            conn.tbbt = False
        c = 0
        detections = []
        for i in conn.chans[data['chan']]['users']:
            if i in cleaned:
                detections.append(i)
                c += 1
        if detections:
            print "Detected in "+data['chan']+": "+(' '.join(detections))
        if c > 5:
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
    if conn.nazi:
        try:
            for i in map(lambda x: x.lower(),cleaned.split()):
                if i in conn.mistakes:
                    count = conn.chans[data['chan']]['spellers'][data['fool']]
                    conn.msg(data['chan'],data['fool']+ ": it's spelt '"+conn.mistakes[i]+"'. This was warning "+str(count)+"/10")
                    conn.chans[data['chan']]['spellers'][data['fool']] += 1
                    if count > 10:
                        conn.msg("chanserv"," ".join(["kick",data['chan'],data['fool'],"Come back when you've started spelling properly."]))
                        conn.chans[data['chan']]['spellers'][data['fool']] = 0
                    break
        except AttributeError, e:
            conn.mistakes = None
            conn.chans[data['chan']]['spellers'] = Counter() # map users to their spelling mistakes
            pkl = open('plugins/mistakes.pkl','rb')
            conn.mistakes = cPickle.load(pkl)
            conn.msg(data['chan'],"loaded spellings")
            pkl.close()
