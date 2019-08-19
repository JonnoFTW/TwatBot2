# coding=utf-8
help = "Converts string to glorious Ｆ Ｕ Ｌ Ｌ ＀ Ｗ Ｉ Ｄ Ｔ Ｈ"

def convert(conn, data):
    try:
        fool = ''.join(data['words'][1:])
        out = ''
        for i in fool:
            if i == ' ':
                out += chr(0x3000)
            else:
                out += chr(ord(i)+0xfee0)
        conn.msg(data['chan'],out)
    except IndexError as e:
        conn.msg(data['chan'],'Please provide a string',data['chan'])
        return

triggers = { '^full':convert}
