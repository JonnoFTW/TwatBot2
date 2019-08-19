import random
#encoding=utf-8
help = "Displays the scrollback for use with ^^. Starts at index 0 on the left. Stores 10 last quotes per channel"
def scroll(conn, data):
    if len(data['words']) > 1:
        try:
            conn.notice(data['user'],"Scroll at "+ data['words'][1] + ": " + conn.chans[data['chan']]['scroll'][int(data['words'][1])])
        except Exception as err:
            conn.notice(data['user'],"Perhaps if you used a number < 10, "+str(err)+ (' '*(random.randint(1,5))))
    else:
        conn.notice(data['fool'],' '.join(["%d: %s;"%x for x in enumerate(conn.chans[data['chan']]['scroll'])]))
triggers = {'^scroll':scroll}



