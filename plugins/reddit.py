import praw
def redditvote(conn,data):
	r = praw.Reddit(user_agent='perwl irc')
	usage = 'Usage is: ^reddit thing_id up|down'
	r.login(conn.factory.keys['reddit_user'],conn.factory.keys['reddit_pass'])
	if len(data['words'])!=3:
		conn.msg(data['chan'],usage)
		return
	else:
		s = r.get_submission(submission_id=data['words'][1])
		title =s.short_link
		if data['words'][2].lower() == 'down':
			s.downvote()
			conn.msg(data['chan'],"Down voted "+title)
		elif data['words'][2].lower() == 'up':
			s.upvote()
			conn.msg(data['chan'],"Upvoted "+title)
		else:
			conn.msg(data['chan'],usage)

triggers = {"^reddit":redditvote}
