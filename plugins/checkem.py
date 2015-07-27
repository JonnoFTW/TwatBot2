import socket
import re
import sys
sys.setrecursionlimit(1500)
help = "4chan dubs getter AIO. use ^check <board> for current post no. of a board . 9MB Bale pack at http://www.mediafire.com/?j3idvabga74e8sy"

def readWord(f,s = ''):
    p = f.recv(1)
    if p == ' ':
        return s
    else:
        return readWord(f,s+p)
def getNos(f):
    nos = []
    # Read in first 7 post numbers
    count = 0
    while count != 7:
       word = readWord(f)
       if word[:6] == 'id=\"no':
         count+= 1
         nos.append(re.sub("[^0-9]","",word))
    return max(nos)



def getPostCount(board):
   port = 80
   host = 'boards.4chan.org'
   headers = "User-Agent: Mozilla/5.0 (X11; Linux i686; rv:2.0) Gecko/20110321 Firefox/4.0\r\nAccept: text/html\r\nCache-Control: max-age=0\r\n"
   get = "GET /%s/ HTTP/1.1\r\nHost: %s\r\n%s\r\n" % (board, host, headers)  
   f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   f.connect((host, port))
   f.send(get)
   return getNos(f)
   f.close()
#boards = ['a','b','c','d','e','f','g','gif','h','vg','hr','k','m','o','p','r','s','t','u','v','w','wg','i','ic','cm','y','3','adv','an','cgl','ck','co','fa','fit','int','jp','lit','mu','n','po','sci','soc','sp','tg','toy','trv','tv','vp','x']
boards = ['a','mlp','hm', 'b', 'c', 'd', 'e', 'f', 'g', 'gif', 'h', 'hr', 'k', 'm', 'o', 'p', 'r', 's', 't', 'u', 'v', 'vg', 'w', 'wg','i', 'ic','r9k','cm', 'y','3','adv', 'an', 'cgl', 'ck', 'co', 'diy', 'fa', 'fit', 'hc', 'int', 'jp', 'lit', 'mu', 'n', 'po', 'pol', 'sci', 'soc', 'sp', 'tg', 'toy', 'trv', 'tv', 'vp', 'x']
def getNo(conn, data):
    if len(data['words']) > 1:
        chan = data['words'][1].lower()
        if chan not in boards:
            conn.msg(data['chan'],'Please select an actual channel',data['chan'])
        else:
            conn.msg(data['chan'],'Current post for '+chan+' is: '+getPostCount(chan),data['chan'])    
    else:
        conn.msg(data['chan'],'How about you give me a board?',data['chan'])
 

triggers = {'^check':getNo,'^checkem':getNo}
