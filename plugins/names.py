def setName(conn,data,fool,name,field):   
    try:
        db = conn.getDB()
        id = db.escape_string(name)
        irc_nick = db.escape_string(fool)
        c = db.cursor()
        vals = [irc_nick,field,id]
        vals = str(tuple(vals))
        c.execute("""INSERT INTO `service_nicks` (`irc_nick`,`service`,`service_nick`) VALUES %vals 
                     ON DUPLICATE KEY UPDATE `%s` = '%s';""" % (field,vals,field,id))
        conn.msg(data['chan'],"Set "+field+" for nick "+nick+" to "+id)
    except IndexError:
        conn.msg(data['chan'],"Please supply a %s to associate your nick with" % (field))
def getName(conn,name,field):
    db = conn.getDB()
    id = db.escape_string(name)
    c = db.cursor()
    query = "SELECT `service_nick` FROM service_nicks WHERE `irc_nick` = '%s' AND `service` = '%s'"%(id,field)
    # print field,id, query
    c.execute(query)
    # print c._last_executed
    x = c.fetchone()
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
    q = "SELECT `service`,`service_nick` FROM service_nicks WHERE irc_nick='%s' "%(nick,service)        
    c.execute(q)
    out = ",".join([i[0]+":"+i[1] for i in c.fetchall()])
    
    conn.msg(data['chan'],out)
triggers = {'^get':get}
