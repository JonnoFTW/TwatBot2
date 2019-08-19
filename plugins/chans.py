help = "List channels currently in"
def chans(conn, data):
    conn.msg(data['chan'],'Currently in: '+(', '.join(list(conn.chans.keys()))))
    
triggers = {'^chans':chans}
