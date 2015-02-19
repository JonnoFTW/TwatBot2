import resource
import psutil
help = "^stat shows memory/cpu usage"
import threading

def getTopic(conn,data):
    conn.msg(data['chan'],conn.chans[data['chan']]['topic'])
def popTopic(conn,data):
    conn.topic(data['chan'],' | '.join(map(lambda x: x.strip(),conn.chans[data['chan']]['topic'].split('|')[:-1])))
def appendTopic(conn,data):
    conn.topic(data['chan'],conn.chans[data['chan']]['topic']+'\003 | '+(' '.join(data['words'][1:])))
def setnick(conn,data):
    if data['fool'] not in conn.factory.admins:
        return
    try:
        conn.setNick(data['words'][1])
        conn.msg("Nickserv","identify "+conn.factory.nickpass)
    except:
        conn.sendMsg(data['chan'],"Usage is: ^setnick <nick>")
def t(conn,data):
    conn.msg(data['chan'],"\001ACTION tests\001")

def threads(conn, data):
    conn.msg(data['chan'],", ".join(map(lambda x: x.getName(), threading.enumerate())))
  
def stat(conn, data):
  r = resource.getrusage(resource.RUSAGE_SELF)
  out = ''
  if r.ru_maxrss < 1024:
    out = str(r.ru_maxrss / 8) + " kB"
  else:
    out = str(r.ru_maxrss / 1024) + " MB"
  conn.msg(data['chan'],"Bot mem usage:" + str(out) + "; System CPU:" + str(psutil.cpu_percent(interval=1)) + "% ;System mem usage: " + str(psutil.phymem_usage()[3]) + "%")
def cmds(conn, data):  
    s = ''
    for i in conn.plugins:
        s += str(i.triggers.keys())
    conn.msg(data['fool'],s)
  
def ddos(conn, data):
    try:
        conn.msg(data['chan'],"Now DDoSing " + data['words'][1])
    except:
        conn.msg(data['chan'],"Now DDoSing " + data['fool'])
def tbbt(conn, data):
    if data['fool'] not in conn.factory.admins:
        return;
    try:
        if data['words'][1] == "on":
            conn.tbbt = True
            conn.msg(data['chan'],"Big Bang Theory mode engaged")
        elif data['words'][1] == "off":
            conn.tbbt = False
            conn.msg(data['chan'],"Big Bang Theory mode disengaged")
        else:
            conn.msg(data['chan'],"^tbbt on|off")
    except AttributeError:
        conn.tbbt = False
        conn.msg(data['chan'],"TBBT mode is "+str(conn.tbbt))
    except IndexError, e:
        try:
            conn.msg(data['chan'],"TBBT mode is "+str(conn.tbbt))
        except AttributeError:
            conn.tbbt = False
            conn.msg(data['chan'],"TBBT mode is "+str(conn.tbbt))
def nazi(conn, data):
    if data['fool'] not in conn.factory.admins:
        return;
    try:
        if data['words'][1] == "on":
            conn.nazi = True
            conn.msg(data['chan'],"Spelling nazi mode engaged")
        elif data['words'][1] == "off":
            conn.nazi = False
            conn.msg(data['chan'],"Spelling nazi mode disengaged")
        else:
            conn.msg(data['chan'],"^nazi on|off")
    except IndexError, e:
        conn.msg(data['chan'],"nazi mode is "+str(conn.nazi))
    except AttributeError:
        conn.nazi = False
        conn.msg(data['chan'],"nazi mode is "+str(conn.nazi))

def ignore(conn, data):
    try:
        user = data['words'][1]
        if user in conn.factory.ignores:
            conn.msg(data['chan'], "I'm already ignoring that nick")
            return
        with open('ignores','a') as f:
            f.write(user+"\n")
            conn.factory.ignores.append(user)
            conn.msg(data['chan'], "Ignoring "+user)
    except IndexError, e:
        conn.msg(data['chan'], "^ignore user")
def debug(conn, data):
    try:
        if data['fool'] in conn.admins:
            if data['words'][1] == "on":
                conn.printAll = True
                conn.msg(data['chan'],"PrintAll is on")
            elif data['words'][1] == "off":
                conn.printAll = False
                conn.msg(data['chan'],"PrintAll off")
            else:
                conn.msg(data['chan'],"Usage is ^debug on|off")
    except IndexError:
        conn.msg(data['chan'],"prinatAll is %s" % (str(conn.printAll)))

def kick(conn,data):
    #add the kicker to list of kickers
    conn.chans[data['channel']]['kicks'].append((data['fool'],time.time()))
    conn.detectMassKick(data['chan'])
triggers = {'^setnick':setnick,'^tbbt':tbbt,'^t':t,'^stat':stat, '^printAll':debug, '^ddos':ddos, '^threads':threads, '^nazi':nazi, '^cmds':cmds, '^ignore':ignore,".k":kick,".kick":kick,".kb":kick,".kickban":kick,
            '^poptopic':popTopic,'^appendtopic':appendTopic,'^gettopic':getTopic}
