from flask import Flask, request
app = Flask(__name__)

# TODO
# 1: Add admin view template
# 2: Automatic redirect or with a template
# 3: Cookie to remember where the user was sent last time, easy way to avoid repeats from the same user
# 4: Save currentindex in a file as well, just in case
# 5: Logging

settingSecret = "secret"

loop = ["URL 1","URL 3","URL 1","URL 2","URL 1"]
currentIdx = 0

@app.route('/')
def routing():
	global currentIdx

	tempIDX = currentIdx

	currentIdx = currentIdx + 1
	if currentIdx == len(loop):
		currentIdx = 0

	msg = 'Hello, World!'+str(tempIDX)

	return msg

@app.route('/settings'+settingSecret, methods=['GET', 'POST'])
def settings():
	global currentIdx

	if request.method=="POST":
		with open('workfile', 'w') as f:
			f.write("NewFile"+ str(currentIdx))
		f.close()
		return "Updating settings"
	else:
		with open('workfile', 'w') as f:
			f.write("NewFile"+ str(currentIdx))

		return ' Settings'
