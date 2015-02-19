help = "Admin only, joins or parts the specified channel"
def reloadgreet(conn,data):    
    with open("greets") as f:
        for i in f.readlines():
            j = i.split()
            conn.factory.greets[j[0]] = ' '.join(j[1:])
    conn.msg(data['chan'],"reloaded greets")
def testgreets(conn,data):
    print conn.greets
def join(conn, data):
    try:
        chan = data['words'][1]
        if chan[0] != '#':
            conn.msg(data['chan'],"Channels must start with a #")
        elif chan in conn.chans.keys():
            conn.msg(data['chan'],'Eye\'m already in that channel')
        else:
            conn.join(chan)
    except IndexError:  
        conn.msg(data['chan'],'Please provide a channel to join')

def part(conn, data):
    try:
        chan = data['words'][1]
        if chan not in conn.chans.keys():
            conn.msg(data['chan'],'Eye\'m not in that channel')
        else:
            del conn.chans[chan]
            conn.leave(chan)
    except IndexError:
        conn.msg(data['chan'],"Please specify a joined channel to part from")
        
def msg(conn, data):
    try:
        conn.msg(data['words'][1],' '.join(data['words'][2:]))
    except Exception:
        conn.msg(data['chan'],"Usage is ^msg <serverId> <channel> <message>")
triggers = {'^join':join,'^part':part,'^msg':msg,'^reloadgreet':reloadgreet,'^tg':testgreets}
