from os import path

from flask import Flask, redirect, url_for, render_template, request, make_response
import os.path
import threading
import atexit
import random
import socket               # Import socket module
import time

import mimetypes
from datetime import datetime
from time import sleep


POOL_TIME = 5 #Seconds
PORT = 81
templateno = 0
myProgress = 0;
calenderBins = [2,7,31,365,999999]
calenderBinCount = [0,0,0,0,0]
filecount = 0

dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()

app = Flask(__name__, static_url_path="/")



def root_dir():  # pragma: no cover
    print("RootDir")
    return ""


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        print("Serve File")
        print(filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
@app.route("/Index.html", methods=["GET", "POST"])
def home():
    print("index")
    #if request.method == "POST":
    cookieKey = request.cookies.get('YourSessionCookie')
    #print("Cookie :"+str(cookieKey))
    response = make_response(
        render_template("index.html", QText='dummy', QSubText='dummy', QImage='', QTimeout=0,
                        QAnswerType='', Question=''))
    if (cookieKey is None):
        cookieKey = str(int(random.random() * 90000000))
        response.set_cookie('YourSessionCookie', cookieKey)
    answer = request.args.get('Online')
    response = make_response(render_template("index.html"))
    response.set_cookie('YourSessionCookie', cookieKey)
    return response


@app.route("/view", methods=["GET", "POST"])
def config():
    global templateno
    global myProgress
    print("view")
    templateno = templateno +1
    myProgress = myProgress +1
    myColor = "#000000"
    if (myProgress > 20):
        myColor = "#0000FF"
    if (myProgress > 40):
        myColor = "#00FFFF"
    if (myProgress > 60):
        myColor = "#00FF00"
    if (myProgress > 80):
        myColor = "#FF0000"
    if (myProgress > 100):
        myProgress = 0

    answer = request.args.get('Mode')
    print("Mode:")
    print(answer)
    if (answer is None or "Text" in answer):
        print("Detected Nothing")
        fullHTML = "\"<label>Copy:</label><label style='color:blue'>"+str(myProgress)+" Files</label>\""
    if ("Progress" in answer):
        print("Detected Progress")
        fullHTML = "\"<label>Progress:<progress id='fortschritt' value='"+str(myProgress)+"' max='50'></progress></label>\""
    if ("Circle" in answer):
        print("Detected Circle")
        fullHTML = "\"<label>Status: </label><label style='color:green'>OK</label><svg style='overflow: visible;'  viewBox='70 -20 80 20' width='80'><circle  cx='10' cy='10' r='5' fill='"+myColor+"'/><circle  cx='25' cy='10' r='5' fill='#00FF00'/><circle  cx='40' cy='10' r='5' fill='#00FF00'/><circle  cx='55' cy='10' r='5' fill='#00FF00'/> </svg>\""
    if ("Bar" in answer):
        print("Detected Bar")
        fullHTML = "\"<label>Status: </label><label style='color:green'>OK</label><li><svg style='overflow: visible;' viewBox='70 -20 80 20' width='80'><rect  x='0' y='0' width='15' height='10' fill='#FF0000'/><rect  x='15' y='0' width='"+str(100-myProgress)+"' height='10' fill='#FFFF00'/><rect  x='30' y='0' width='25' height='10' fill='#00FFFF'/><rect  x='55' y='0' width='"+str(myProgress)+"' height='10' fill='#0000FF'/> </svg></li>\""
    if ("Icon" in answer):
        print("Detected Icon")
        if (myProgress % 3 == 0):
            fullHTML = "\"<label>Data ON</label><img src='http://vision2u.de/img/DataActive.png' width='30' height='30''>\""
        if (myProgress % 3 == 1):
            fullHTML = "\"<label>Data Off</label><img src='http://vision2u.de/img/DataInactive.png' width='30' height='30''>\""
        if (myProgress % 3 == 2):
            fullHTML = "\"<label>Images On</label><img src='http://vision2u.de/img/ImagesActive.png' width='30' height='30''>\""
        if (myProgress % 3 == 3):
            fullHTML = "\"<label>Images Off</label><img src='http://vision2u.de/img/ImagesInActive.png' width='30' height='30''>\""


    response = make_response(render_template("api.php", Timestamp=templateno, data_view = "progress", data_name="DB-Tools", data_status="Online", data_color=myColor, data_text="My Text", data_action="Copy", data_progress = fullHTML, data_statistik1 = 60, data_statistik2= 34, data_statistik3 = 28, data_statistik4 = 10))
    return response

@app.route("/Heimdall", methods=["GET", "POST"])
def test():
    fullHTML = ""
    print("Heimdall")
    answer = request.args.get('TestPort')
    if (answer is not None and ":" in answer):
        print("Port:")
        print(answer)
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        x = answer.split(":")
        targetHost = x[0]
        targetPort = int(x[1])
        a_socket.settimeout(1)
        result_of_check = a_socket.connect_ex((targetHost, targetPort))
        if result_of_check == 0:
            print(targetHost + " Port " + str(targetPort) + " is open")
            fullHTML += "\"<svg style='overflow: visible;'  viewBox='70 -20 80 20' width='80'><circle  cx='10' cy='10' r='5' fill='0x00FF00'/> </svg>\""
        else:
            print(targetHost + " Port " + str(targetPort) + " is NOT open")
            fullHTML += "\"<svg style='overflow: visible;'  viewBox='70 -20 80 20' width='80'><circle  cx='10' cy='10' r='5' fill='0xFF0000'/> </svg>\""
        a_socket.close()
    answer = request.args.get('TestPort2')
    if (answer is not None and ":" in answer):
        print("Port:")
        print(answer)
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        x = answer.split(":")
        targetHost = x[0]
        targetPort = int(x[1])
        a_socket.settimeout(1)
        result_of_check = a_socket.connect_ex((targetHost, targetPort))
        if result_of_check == 0:
            print(targetHost + " Port " + str(targetPort) + " is open")
            fullHTML = fullHTML.replace("</svg>", "<circle  cx='25' cy='10' r='5' fill='#00FF00'/> </svg>\"")
        else:
            print(targetHost + " Port " + str(targetPort) + " is NOT open")
            fullHTML = fullHTML.replace("</svg>", "<circle  cx='25' cy='10' r='5' fill='#FF0000'/> </svg>\"")
        a_socket.close()

    answer = request.args.get('TestFoldersize')
    if (answer is not None ):
        print("TestFoldersize: "+answer)
        fullHTML += "\"<label>Size:</label><label style='color:blue'>" + get_size_format(get_size(answer)) + " </label>\""

    answer = request.args.get('FolderBar')
    if (answer is not None):
        print("FolderBar: " + answer)
        calenderBinCount = [0, 0, 0, 0, 0]
        scanFolder(filePath=answer)
        fullHTML += printScanResults()

    answer = request.args.get('Modified')
    if (answer is not None):
        print("Modified: " + answer)
        fullHTML += "\"<label>Modified:</label><label style='color:blue'>" +str(888) + " </label>\""


    response = make_response(render_template("api.php",  data_progress = fullHTML ))
    return response



def do(msession):
    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global commonDataStruct
        global yourThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
            app.run(host='0.0.0.0', port=PORT);
        # Set the next thread to happen
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    # Initiate
    session = msession
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)

    #app.run();
    return app


import os
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += (os.path.getsize(fp) if os.path.isfile(fp) else 0)
    return total_size

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def printScanResults():
    global calenderBins, calenderBinCount, filecount
    maxWidth = 100;
    for x in range(len(calenderBins)):
        print((calenderBinCount[x]*maxWidth)/filecount)
    print("Files:"+str(filecount))
    fullHTML = "\"<li><svg style='overflow: visible;' viewBox='70 -20 80 20' width='80'>" \
               "<rect  x='0'  y='0' width='"+str(int((calenderBinCount[0]*maxWidth)/filecount))+ "' height='10' fill='#FF0000'/>" \
               "<rect  x='"+str(int((calenderBinCount[0]*maxWidth)/filecount))+ "' y='0' width='"+str(int((calenderBinCount[1]*maxWidth)/filecount))+ "' height='10' fill='#FFFF00'/>" \
               "<rect  x='"+str(int(((calenderBinCount[0]+calenderBinCount[1])*maxWidth)/filecount))+ "' y='0' width='"+str(int((calenderBinCount[2]*maxWidth)/filecount))+"' height='10' fill='#00FFFF'/>" \
               "<rect  x='"+str(int(((calenderBinCount[0]+calenderBinCount[1]+calenderBinCount[2])*maxWidth)/filecount))+ "' y='0' width='"+str(int((calenderBinCount[3]*maxWidth)/filecount))+"' height='10' fill='#0000FF'/> " \
               "<rect  x='"+str(int(((calenderBinCount[0]+calenderBinCount[1]+calenderBinCount[2]+calenderBinCount[3])*maxWidth)/filecount))+ "' y='0' width='"+str(int((calenderBinCount[4]*maxWidth)/filecount))+"' height='10' fill='#00FFFF'/></svg></li>\""
    return fullHTML

def scanFolder(filePath = "."):
    global calenderBins, calenderBinCount, filecount
    dt1 = datetime.fromtimestamp(time.time())
    for root, dirs, files in os.walk(filePath):
        for file in files:
            if (path.exists(filePath+"/"+file)):
                #print(filePath+"/"+file)
                dt2 = datetime.fromtimestamp(os.path.getmtime((filePath+"/"+file)))
                delta = dt1 - dt2
                filecount = filecount+1
                for x in range(len(calenderBins)):
                    if (delta.days <= calenderBins[x]):
                        calenderBinCount[x] = calenderBinCount[x] +1
                        #print(str (delta.days))
                        break
        for dir in dirs:
            #print("Scanfolder:"+dir)
            scanFolder(filePath = filePath+"/"+dir)

if __name__ == "__main__":


    print("DummyMicroservice 2")
    filePath = "C:\Data\Seidenader"
    #scanFolder(filePath=filePath)
    #printScanResults()

    app.run(host='0.0.0.0', port=PORT)