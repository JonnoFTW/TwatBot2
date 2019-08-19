import praw
def redditvote(conn,data):
	r = praw.Reddit(
        user_agent='perwl irc',
        client_id=conn.factory.keys['reddit_client_id'],
        client_secret=conn.factory.keys['reddit_client_secret'],
        username=conn.factory.keys['reddit_user'],
        password=conn.factory.keys['reddit_pass'])
	usage = 'Usage is: ^reddit thing_id up|down'
#	r.login(conn.factory.keys['reddit_user'],conn.factory.keys['reddit_pass'])
#	r.set_oauth_app_info(client_id=conn.factory.keys['reddit_client_id'],
#	client_secret=conn.factory.keys['reddit_client_secret'],
#	redirect_uri='http://127.0.0.1:65010/authorize_callback')
	if len(data['words'])!=3:
		conn.msg(data['chan'],usage)
		return
	else:
		s = r.submission(id=data['words'][1])
		title =s.shortlink
		if data['words'][2].lower() == 'down':
			s.downvote()
			conn.msg(data['chan'],"Down voted "+title)
		elif data['words'][2].lower() == 'up':
			s.upvote()
			conn.msg(data['chan'],"Upvoted "+title)
		else:
			conn.msg(data['chan'],usage)

triggers = {"^reddit":redditvote}
