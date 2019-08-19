import random
help = "Check your privilege!"

def privilege(conn, data):
    # Load the privileges from the db
    if random.randint(1,10) == 4:
        conn.msg(data['chan'],data['fool']+": DIE YOU OPRESSIVE CIS SCUM")
        return
    privileges = ['cissexual','heteromantic','cisethnic','white','jew','thin','male','literate','educated','wealth','toilet','able-bodied','middle-class','straight','masculine','sexual','non-intersex','neurotypical','vanilla','english-speaking','adult','christian','natural-born',"violent-film-liking"]
    if len(data['words']) > 1 and data['words'][1] in conn.chans[data['chan']]['users']:
        f = data['words'][1]
    else:
        f = data['fool']
    conn.msg(data['chan'],f+': check your '+(' '.join([random.choice(privileges), random.choice(privileges),random.choice(privileges)])+' privilege'))
def check(conn, data): 
    # Load the users privileges in from db
    conn.msg(data['chan'],"CHECK YOUR PRIVILEGE")
def bcmp(conn, data):
    with open('plugins/bmp.dat') as f:
        conn.msg(data['chan'],random.choice(f.readlines()))
def addpriv(conn,data):
    if data['fool'] not in conn.factory.admins:
        conn.msg(data['chan'],data['fool']+ ": you have too much privilege to be telling others with privilege is")
        return
    
    if len(data['words']) < 2:
        conn.msg("Add a privilege to the list of privileges. These should be written in 3rd person")
        return
    with open('plugins/bmp.dat','a+') as f:
        l = f.readlines()
        c = l[-1].split()[0][:-1]
        print(c)
        priv = ' '.join(data['words'][1:])
        line = str(int(c)+1)+'. '+priv+'\n'
        f.write(line)
        conn.msg(data['chan'],"Added privilege:  "+line)
triggers = {'^check': check, '^privilege':privilege,'^blackcismaleprivilege':bcmp,'^addpriv':addpriv}
