def setName(conn,data,fool,name,field):
    try:
        db = conn.getDB()
        print(db)
        id = name
        irc_nick = fool
        c = db.cursor()
        vals = [irc_nick,field,id]
        c.execute("DELETE FROM service_nicks WHERE irc_nick = ? and service = ?", (irc_nick, field))
        q = "INSERT INTO `service_nicks` (`irc_nick`,`service`,`service_nick`) VALUES (?,?,?)"
        print(q)
        c.execute(q, vals)
#        print "rows:",c.affected_rows()
        c.close()
        db.commit()
        conn.msg(data['chan'],"Set "+field+" for nick "+irc_nick+" to "+id)
    except IndexError:
        conn.msg(data['chan'],"Please supply a %s username to associate your nick with" % (field))
def getName(conn,name,field):
    db = conn.getDB()
    id = name
    c = db.cursor()
    query = "SELECT `service_nick` FROM `service_nicks` WHERE `irc_nick` = ? AND `service` = ?"
    c.execute(query, (id, field))
    x = c.fetchone()
    c.close()
    if x == None or x[0] == None:
        print("Using name: "+ name)
        return name
    else:
        print("Using name: "+x[0])
        return x[0]
def get(conn,data):
    db = conn.getDB()
    c = db.cursor()
    nick = data['fool']
    q = "SELECT `service`,`service_nick` FROM service_nicks WHERE irc_nick = ? and service= ?;"
    c.execute(q, (nick, data['words'][1]))
    out = ",".join([i[0]+":"+i[1] for i in c.fetchall()])

    conn.msg(data['chan'],out)
def set(conn,data):
    setName(conn,data,data['fool'],data['words'][2],data['words'][1])

def info(conn,data):
    db = conn.getDB()
    c = db.cursor()
    c.execute("SELECT service, service_nick FROM service_nicks WHERE irc_nick = ?", (data['fool'],))
    for row in c.fetchall():
        conn.msg(data['chan'], row[0]+"->"+row[1])
triggers = {'^get':get,'^set':set,'^nameinfo':info}
