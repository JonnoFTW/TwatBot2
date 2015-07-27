def setName(conn,data,fool,name,field):   
    try:
        db = conn.getDB()
        print db
        id = db.escape_string(name)
        irc_nick = db.escape_string(fool)
        c = db.cursor()
        vals = [irc_nick,field,id]
        print vals
        vals = str(tuple(vals))
        q = """INSERT INTO `service_nicks` (`irc_nick`,`service`,`service_nick`) VALUES %s 
                     ON DUPLICATE KEY UPDATE 
                            `service_nick` = values(service_nick),
                            `irc_nick` = values(irc_nick),
                            `service` = values(service);""" % (vals)
        print q
        c.execute(q)
#        print "rows:",c.affected_rows()
        c.close()
        db.commit()
        conn.msg(data['chan'],"Set "+field+" for nick "+irc_nick+" to "+id)
    except IndexError:
        conn.msg(data['chan'],"Please supply a %s username to associate your nick with" % (field))
def getName(conn,name,field):
    db = conn.getDB()
    id = db.escape_string(name)
    c = db.cursor()
    query = "SELECT `service_nick` FROM service_nicks WHERE `irc_nick` = '%s' AND `service` = '%s'"%(id,field)
    # print field,id, query
    c.execute(query)
    # print c._last_executed
    x = c.fetchone()
    c.close()
    if x == None or x[0] == None:
        print "Using name: "+ name
        return name
    else:
        print "Using name: "+x[0]
        return x[0]
def get(conn,data):
    db = conn.getDB()
    c = db.cursor()
    nick = db.escape_string(data['fool'])
    try:
        service =" AND `service`='%s'"%( db.escape_string(data['words'][1]))
     
    except IndexError:
        service = ''
    q = "SELECT `service`,`service_nick` FROM service_nicks WHERE irc_nick='%s' %s;"%(nick,service)        
    c.execute(q)
    out = ",".join([i[0]+":"+i[1] for i in c.fetchall()])
    
    conn.msg(data['chan'],out)
def set(conn,data):
    setName(conn,data,data['fool'],data['words'][2],data['words'][1])

def info(conn,data):
    db = conn.getDB()
    c = db.cursor()
    c.execute("SELECT USER()")
    conn.msg(data['chan'],c.fetchone()[0])
triggers = {'^get':get,'^set':set,'^nameinfo':info}
