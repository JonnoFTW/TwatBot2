# coding=utf-8
help = "^tell will private message the given person whenever and whereever it sees them again. use ^read to read any message you may have"

def setGreet(conn,data):
    if len(data['words']) == 1:
        conn.msg(data['chan'],"Usage is ^setgreet <your greet message>")
    else:
        conn.factory.greets[data['fool']] = ' '.join(data['words'][1:][:128])
        conn.msg(data['chan'],"Greet set for "+data['fool'])
        with open('greets','w') as f:
            for i in conn.factory.greets.items():
                f.write("%s %s\n"%i)


def addTell(conn, data):
    """
    Usage: ^tell <to> <msg>
    Add a tell to the database for a specific username.
    Database has:
        - Table tell- (PK)msgId,to(nick),message,time,sender(nick)
    """
    try:
      db = conn.getDB()
      cursor = db.cursor()
      cursor.execute("""INSERT INTO tell (`to`,message,time,sender)
                     VALUES (%s,%s,NOW(),%s)""",
                     (data['words'][1],
                      ' '.join(data['words'][2:]),
                      data['fool']))
      conn.msg(data['chan'],"Consider it noted")
      conn.tells.add(data['words'][1])
      print conn.tells
    except IndexError, e:
      print e
      conn.msg(data['chan'],"Usage: ^tell <to> <message>")
    except Exception, e:
        conn.msg(data['chan'],"Something went wrong telling the message! %s" % (str(e)))

def getTell(conn, data):
    try:
      db = conn.getDB()
      cursor = db.cursor()
      cursor.execute("""SELECT tell.sender, tell.message, tell.time
                        FROM tell WHERE `to` = %s
                     """, (data['fool']))
      msgs = cursor.fetchall()
      if len(msgs) == 0:
          conn.notice(data['user'],"You have no messages")
      else:
          conn.notice(data['user'],"You have the following messages: ")
          for i in msgs:
              try:
                  conn.notice(data['user'],u"From: {0} on {1} -----> {2}".format(i[0], i[2], i[1]).decode('utf-8'))
              except:
                  pass
          cursor.execute("DELETE FROM tell WHERE `to` = %s", (data['fool']))
          cursor.close()
    except Exception, e:
        print e
        conn.notice(data['fool'],"Something went wrong telling the message! %s" % (str(e)))

triggers = {'^tell':addTell, '^read':getTell,'^setgreet':setGreet}
