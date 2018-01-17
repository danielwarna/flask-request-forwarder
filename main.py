from flask import Flask, request,render_template, redirect
app = Flask(__name__)
import os
import logging
from logging.handlers import RotatingFileHandler

# TODO
# 1: DONE Add admin view template
# 2: DONE Automatic redirect or with a template 
# 3: Cookie to remember where the user was sent last time, easy way to avoid repeats from the same user
# 4: DONE Save currentindex in a file as well, just in case
# 5: Logging


file_handler = RotatingFileHandler('forwarder.log', maxBytes=1024 * 1024 * 100, backupCount=10)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

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

app.logger.info("Starting up with index: " + str(currentIdx))
app.logger.info("Starting up with loop: " + str(loop))

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

    app.logger.info("Showing index " + str(nextIdx) + " - " + loop[nextIdx])

    msg = 'Hello, World!'+str(nextIdx)+ " -- " + str(loop[nextIdx])
    url = str(loop[nextIdx])
    return render_template("forward.html", content=url)
    return msg

@app.route('/redirect')
def redir():
    
    nextIdx = nextIndex()

    app.logger.info("Forwarding index " + str(nextIdx) + " - " + loop[nextIdx])

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

        app.logger.info("Update urllist to: " + str(loop))
        
        return render_template('settings.html', loop="\n".join(loop))
    else:
        print(loop)
        return render_template('settings.html', loop="\n".join(loop))
