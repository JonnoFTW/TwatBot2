help ="Send the the line preceeding ^^ to @Buttsworth_ on twitter. List all cmds with ^cmds, specific help with ^xyz help . http://twitter.com/#!/Buttsworth_ Source code available at: https://github.com/JonnoFTW/TwatBot2"
def xyz(conn,data):
    conn.notice(data['fool'],"You actually thought this was a function?")
def shelp(conn, data):
    if data['fool'] in conn.factory.admins:
      if len(data['words']) == 1:
          conn.msg(data['chan'],help)
      elif len(data['words']) > 1 and data['words'][1] in conn.chans[data['chan']]['users']:
          conn.notice(data['words'][1],help)
      else:
          conn.notice(data['fool'],"No such user in "+data['chan'])
    else:
      conn.notice(data['fool'],help)

def social(conn,data):
    places = ['http://reddit.com/r/perwl','http://steamcommunity.com/groups/perwl','http://twitter.com/buttsworth_','https://www.facebook.com/groups/PerwlPaintHuffingLogistics/']
    conn.msg(data['chan'],' '.join(places))
triggers = { '^help':shelp,'^about':shelp,"^xyz":xyz,'^social':social}
