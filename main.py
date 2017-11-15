from flask import Flask, request,render_template, redirect
app = Flask(__name__)
import os

# TODO
# 1: Add admin view template
# 2: Automatic redirect or with a template
# 3: Cookie to remember where the user was sent last time, easy way to avoid repeats from the same user
# 4: Save currentindex in a file as well, just in case
# 5: Logging

loopFile = "workfile"
currentIndexFile = "indexfile"

settingSecret = "secret"

loop = ["URL 1","URL 3","URL 1","URL 2","URL 1"]
currentIdx = 0

try: 
	with open(currentIndexFile, "r") as indexf:
		currentIdx = int(indexf.read())
	indexf.close()
except:
	print("noindexfile")


with open(loopFile, "r") as f:
	content = f.readlines()
	loop = content
f.close()

loop = [item.strip() for item in loop]

# Return current index, update(increment) and save it
def nextIndex():
	global currentIdx

	tempIDX = currentIdx

	currentIdx = currentIdx + 1
	if currentIdx == len(loop):
		currentIdx = 0

	with open(currentIndexFile, "w") as f:
		f.write(str(currentIdx))

	return tempIDX

@app.route('/')
def routing():
	global currentIdx

	nextIdx = nextIndex()

	msg = 'Hello, World!'+str(nextIdx)+ " -- " + str(loop[nextIdx])

	return msg

@app.route('/redirect')
def redir():
	
	nextIdx = nextIndex()
	url = loop[nextIdx] 

	return redirect(url)

@app.route('/settings'+settingSecret, methods=['GET', 'POST'])
def settings():
	global currentIdx
	global loop

	if request.method=="POST":

		urls = request.form.get('urls')
		loop = urls.split("\n")

		with open(loopFile, 'w') as f:
			f.write(''.join(loop))
		f.close()
		
		return render_template('settings.html', loop="\n".join(loop))
	else:
		print(loop)
		return render_template('settings.html', loop="\n".join(loop))
