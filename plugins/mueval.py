import subprocess
help = "Execute a haskell function"

def mueval(conn, data):
    try:
        src = ' '.join(data['words'][1:])
    except:
        conn.msg(data['chan'],"Please specify a valud haskell statement")
        return
    args = ["/home/jonno/.cabal/bin/mueval-core","-E", "-XBangPatterns", "-XNoMonomorphismRestriction", "-XViewPatterns",     "--expression=" + src]
    print "cmd was"+ (' '.join(args))
    try:
        out = subprocess.check_output(args,stderr=subprocess.STDOUT).splitlines()
    except subprocess.CalledProcessError, e:
        out = e.output.splitlines()
    for i in out[:3]:
        conn.msg(data['chan'],i)

triggers = {'^>':mueval,'^c':mueval}
