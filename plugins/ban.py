help = "^ignore shows current ignores. ^ignore <user> ignores user if you're and admin"
def ignore(conn, data):
    if len(data['words']) > 1 and data['fool'] in conn.factory.admins:
        conn.factory.ignores.add(data['words'][1])
        writeIgnore(conn)
        toSend = data['words'][1]+' is now ignored'
        conn.msg(data['chan'],toSend)
    else:
        conn.msg(data['chan'],'Current ignores are: '+(', '.join(conn.factory.ignores)))

def writeIgnore(conn):
    with open('ignores','w') as f:
        for i in conn.factory.ignores:
            f.write(i+'\n')
    
def unignore(conn, data):
    conn.msg(data['chan'],"test")
    try:
        u = data['words'][1]
        conn.msg(data['chan'],"Unignorening "+u)
        conn.factory.ignores.remove(u)
        writeIgnore(conn)
    except (IndexError, KeyError) as e:
        conn.msg(data['chan'],"please specify someone to unignore")
    
def admin(conn,data):
    if data['fool'] in conn.factory.admins:
        if len(data['words'] > 1):
            f = open('admins','a')
            conn.factory.admins.append(data['words'][1])
            f.write(data['words'][1]+'\n')
            f.close()
            conn.msg(data['chan'],"Admin added")
        else:
            conn.msg(data['chan'],"^admin <user> to add an admin")
    else:
        conn.msg(data['chan'],"u wot m8")
    
triggers = {'^ignore':ignore,'^ignores':ignore,"^unignore":unignore,'^admin':admin}
