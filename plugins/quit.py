help = "Rehab is for quitters"
def exit(conn, data):
    conn.quitting = True
    conn.close()
    
triggers = {'^quit':exit,'^exit':exit}
