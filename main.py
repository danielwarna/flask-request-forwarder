import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request, render_template, redirect

# TODO
# 1: DONE Add admin view template
# 2: DONE Automatic redirect or with a template
# 3: Cookie to remember where the user was sent last time, easy way to avoid repeats from the same user
# 4: DONE Save currentindex in a file as well, just in case
# 5: Logging

app = Flask(__name__)

logFilename = "forwarder.log"
logFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = RotatingFileHandler(logFilename, maxBytes=1024 * 1024 * 100, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logFormatter)
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

    with open(currentIndexFile, "w") as workfile:
        workfile.write(str(currentIdx))

    return tempIDX

@app.route('/')
def routing():
    global currentIdx

    nextIdx = nextIndex()

    app.logger.info("Showing index " + str(nextIdx) + " - " + loop[nextIdx])
    print("Showing index " + str(nextIdx) + " - " + loop[nextIdx])

    params = request.query_string
    params = params.decode('utf8')

    # msg = 'Hello, World!'+str(nextIdx)+ " -- " + str(loop[nextIdx])
    url = str(loop[nextIdx])

    if len(params) > 0:
        app.logger.info("Found params+ " + params)
        url = url + "?" + params

    return render_template("forward.html", content=url)
    # return msg


@app.route('/redirect')
def redir():

    nextIdx = nextIndex()

    app.logger.info("Forwarding index " + str(nextIdx) + " - " + loop[nextIdx])

    params = request.query_string
    params = params.decode('utf8')

    url = loop[nextIdx]

    if len(params) > 0:
        app.logger.info("Found params+ " + params)
        url = url + "?" + params

    url = url.strip('\n')
    url = url.strip('\t')
    return redirect(url)

@app.route('/settings'+settingSecret, methods=['GET', 'POST'])
def settings():
    global currentIdx
    global loop

    if request.method == "POST":

        urls = request.form.get('urls')
        loop = urls.split("\n")

        with open(loopFile, 'w') as workfile:
            workfile.write(''.join(loop))
        workfile.close()

        app.logger.info("Update urllist to: " + str(loop))

        return render_template('settings.html', loop="\n".join(loop))
    else:
        print(loop)
        return render_template('settings.html', loop="\n".join(loop))


@app.route('/settings' + settingSecret + '/log', methods=['GET'])
def showlog():
    with open(logFilename, "r") as logfile:
        loglines = logfile.readlines()

    return render_template("logs.html", logs=loglines)


if __name__ == "__main__":
    app.run()