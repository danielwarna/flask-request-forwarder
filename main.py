from flask import Flask, request,render_template
app = Flask(__name__)
import os

# TODO
# 1: Add admin view template
# 2: Automatic redirect or with a template
# 3: Cookie to remember where the user was sent last time, easy way to avoid repeats from the same user
# 4: Save currentindex in a file as well, just in case
# 5: Logging

settingSecret = "secret"

loop = ["URL 1","URL 3","URL 1","URL 2","URL 1"]
currentIdx = 0

with open("workfile", "r") as f:
	content = f.readlines()
	loop = content
f.close()

loop = [item.strip() for item in loop]

@app.route('/')
def routing():
	global currentIdx

	tempIDX = currentIdx

	currentIdx = currentIdx + 1
	if currentIdx == len(loop):
		currentIdx = 0

	msg = 'Hello, World!'+str(tempIDX)+ " -- " + str(loop[tempIDX])

	return msg

@app.route('/settings'+settingSecret, methods=['GET', 'POST'])
def settings():
	global currentIdx
	global loop

	if request.method=="POST":

		urls = request.form.get('urls')
		loop = urls.split("\n")

		with open('workfile', 'w') as f:
			f.write(''.join(loop))
		f.close()
		
		return render_template('settings.html', loop="\n".join(loop))
	else:
		print(loop)
		return render_template('settings.html', loop="\n".join(loop))
