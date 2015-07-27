# coding=utf-8
help = u"Converts string to glorious Ｆ Ｕ Ｌ Ｌ ＀ Ｗ Ｉ Ｄ Ｔ Ｈ"

def convert(conn, data):
    try:
        fool = ''.join(data['words'][1:])
        out = u''
        for i in fool:
            if i == ' ':
                out += unichr(0x3000)
            else:
                out += unichr(ord(i)+0xfee0)
        conn.msg(data['chan'],out)
    except IndexError, e:
        conn.msg(data['chan'],'Please provide a string',data['chan'])
        return

triggers = { '^full':convert}
