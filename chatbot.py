from threading import Thread
from Queue import Queue
import win32gui
import win32con
import time
import re
from services.urban_dictionary import UrbanDictionary
from services.dictionary import Dictionary
from services.urls import Urls
from services.auth import Authenticator
from services.core import Translate
from services.oxford_dictionary import Definitions
from services.sexy import Sexy
from services.color_output import ColorOutput
from services.randomplayer import RandomPlayer
from services.balance_teams import BalanceTeams
#VARIABLES--------------------------
 
mainloop_speed = 0.5
queue_worker_idle_time = .1
console_line_count = 6
command_idle_time = 1
    
#INIT ET WINDOW

ch = win32gui.FindWindow("ET WinConsole", 'ET Console')
cs = win32gui.FindWindowEx(ch, None, 'Edit', None)
cg = win32gui.FindWindowEx(ch, cs, 'Edit', None)

q = Queue()
 
#METHODS----------------------------
def send_to_et(text):
    win32gui.SendMessage(cs, win32con.WM_SETTEXT, None, text)
    win32gui.SendMessage(cs, win32con.WM_CHAR, win32con.VK_RETURN, None)

 
def get_console_lines():
    buffer_size = win32gui.SendMessage(cg, win32con.WM_GETTEXTLENGTH, None, None) + 1
    buffer = win32gui.PyMakeBuffer(buffer_size)
    win32gui.SendMessage(cg, win32con.WM_GETTEXT, buffer_size, buffer) 
    split = str(buffer).split('\n')
    return split[len(split)-console_line_count:]
 
def queue_worker():
    while True:
        if q.qsize() > 0:           
            parse_command(q.get())
        time.sleep(queue_worker_idle_time)

def parse_command(lines):
    urban = UrbanDictionary()
    define = Dictionary()   
    urls = Urls()
    auth = Authenticator()
    translate = Translate() 
    oxford = Definitions()  
    sexy = Sexy()
    color_output = ColorOutput()
    randomplayer = RandomPlayer()
    balanceteams = BalanceTeams()

    for line in lines:
        isCmd = False
        if ": !" in line:
            try:
                auth = auth.authenticate(line)
            except:
                print "Authentication error!"
                break
                parse_command(lines)

            newline = line.replace(str(auth) + ": ", "").rstrip()
            if newline[0] == "!":
                #It's a command
                isCmd = True
                try:
                    Command = re.search(r"\!(\w*)(\s.*)?", newline).group(1)
                    try:
                        Argument = re.search(r"\!\w*\s(.*)", newline).group(1)
                    except:                 
                        Argument = ''
                    callFunction = eval(Command).call(Argument)
                    send_to_et("say {}".format(callFunction))
                except:
                    print "Command module error!"
                    break
                    parse_command(lines)
            
        elif "https://" in line or "http://" in line: 
            time.sleep(command_idle_time)
            try:
                urls = urls.call(line)
                for url in urls:
                    send_to_et("say ^1URL: ^7{}".format(url))
                    time.sleep(command_idle_time)
            except: 
                break
                parse_command(lines)

        elif "/color" in line:
            time.sleep(1)
            try:
                text = re.search(r'\/color\s(.*)?', line).group(1)
                send_to_et("say {}".format(color_output.call(text)))
            except:
                break
                parse_command(lines)
            

        elif "/translate" in line:
            time.sleep(1)
            try:
                translate_text = re.search(r'\/translate\s(.*)?', line).group(1)
                send_to_et("echo {}".format(translate.call(translate_text)))
            except:
                break
                parse_command(lines)

        #Print out all lines, color commands green. :)
        if isCmd:
            print '\033[40m' + line + '\033[41m'
        else:
            print line
#MAIN-------------------------------
 
#Start queue consumer in new thread.
t = Thread(target=queue_worker)
t.daemon = True
t.start()
#Start main loop. (queue producer)
tmp = list()
while True:
    console_list = get_console_lines()  #6 last lines
    if set(console_list) != set(tmp): #If theres defference between last 6 lines
        q.put([x for x in console_list if x not in tmp]) # difference between console_list and tmp
        tmp = console_list
    time.sleep(mainloop_speed)
