def index():
	print("-------6.5-------")
	with open("./templates/index.html", "rb") as f:
		return f.read()

def center():
	with open("./templates/center.html", "rb") as f:
		return f.read()

def application(env, start_response):
	print("-------6.3-----")
	start_response('200 OK', [('Content-Type', 'text/html,charset=utf8')])
	file_name = env['PATH_INFO']

	if file_name == '/index.py':
		return index()
	elif file_name == '/center.py':
		return center()
	else:
		return "hello word!"
