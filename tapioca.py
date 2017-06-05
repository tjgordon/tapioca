#!/usr/bin/python

import evdev
import subprocess
from decimal import Decimal
import time
import os
import ConfigParser
from collections import OrderedDict
from threading import Timer, Thread
from pymouse import PyMouse
import argparse
import sys

# todo
# long press should not work on two finger long press
# implement three finger tap
# implement swipes

mouse = PyMouse()
app_name = "tapioca"
config_folder = os.path.join(os.path.expanduser("~"), '.config', app_name)
config_file = app_name + ".conf"
full_config_file_path = os.path.join(config_folder, config_file)
Config = ConfigParser.ConfigParser(allow_no_value=True)

parser = argparse.ArgumentParser(
    description=app_name + " enables right click on linux touchscreen devices.")
parser.add_argument(
    "--device", help="Specify name of your touch panel make" \
    " (can be found out by running xinput command).")

args = parser.parse_args()
# print(args.device)

# do not edit these settings, all settings should be changed in .conf file
# in user section

default_section = "Default Settings"
user_section = "User Settings"
default_settings = OrderedDict([
    ('; Touch panel make (run xinput command in terminal)', None),
    ('touch_panel', ""),
    ('; Minimum long press time in seconds, e.g - 0.5, 1.2', None),
    ('minimum_long_press_time', 1.5),
    ('; Right click methods, possible values - xdotool, pymouse', None),
    ('right_click_method', 'xdotool'),
    ('; Long press behavior, possible values - pc (menu appears after finger lift),' \
     ' smartphone (no finger lift required, menu flickers once)', None),
    ('long_press_behavior', 'pc'),
    ('; Long press, possible values - 1 (True), 0 (False)', None),
    ('enable_long_press', 1),
    ('; Two finger tap, possible values - 1 (True), 0 (False)', None),
    ('enable_two_finger_tap', 1)
])

def setconfig():
    try:
        if os.stat(full_config_file_path).st_size > 0:
            file_empty = False
        else:
            file_empty = True
    except OSError:
        pass

    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    if not os.path.exists(full_config_file_path) or file_empty == True:
        with open(full_config_file_path, "w+") as f:
            Config.add_section(default_section)
            Config.set(
                default_section, '; !!!! do not edit, change settings in user section !!!!')
            for k, v in default_settings.items():
                if v == None:
                    Config.set(default_section, k)
                else:
                    Config.set(default_section, k, v)
            Config.add_section(user_section)
            Config.set(user_section, '; change settings below')
            for k, v in default_settings.items():
                if v == None:
                    Config.set(user_section, k)
                else:
                    Config.set(user_section, k, v)
            Config.write(f)

        if args.device != None:
            with open(full_config_file_path, "w") as b:
                Config.set(user_section, "touch_panel", args.device)
                Config.write(b)

try:
    setconfig()
except KeyboardInterrupt:
    sys.exit(1)

Config.read(full_config_file_path)

try:
    touch_panel = Config.get(user_section, "touch_panel")
except:
    try:
        touch_panel = Config.get(default_section, "touch_panel")
    except:
        touch_panel = default_settings['touch_panel']

try:
    minimum_long_press_time = float(Config.get(
        user_section, "minimum_long_press_time"))
except:
    try:
        minimum_long_press_time = float(Config.get(
            default_section, "minimum_long_press_time"))
    except:
        minimum_long_press_time = default_settings['minimum_long_press_time']

try:
    right_click_method = Config.get(user_section, "right_click_method")
except:
    try:
        right_click_method = Config.get(default_section, "right_click_method")
    except:
        right_click_method = default_settings['right_click_method']

try:
    long_press_behavior = Config.get(user_section, "long_press_behavior")
except:
    try:
        long_press_behavior = Config.get(
            default_section, "long_press_behavior")
    except:
        long_press_behavior = default_settings['long_press_behavior']

try:
    enable_long_press = Config.getboolean(user_section, "enable_long_press")
except:
    try:
        enable_long_press = Config.getboolean(
            default_section, "enable_long_press")
    except:
        enable_long_press = default_settings['enable_long_press']

try:
    enable_two_finger_tap = Config.getboolean(
        user_section, "enable_two_finger_tap")
except:
    try:
        enable_two_finger_tap = Config.getboolean(
            default_section, "enable_two_finger_tap")
    except:
        enable_two_finger_tap = default_settings['enable_two_finger_tap']

lift_time = None
touch_time = None
finger0_time = None
finger1_time = None
finger2_time = None
abs_touch_time = None
abs_lift_time = None
no_device_found = True
long_press_done = False

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

for device in devices:
    # print(device.fn, device.name, device.phys)
    # print device.name
    if (device.name == touch_panel):
        input_node = device.fn
        no_device_found = False

if no_device_found == True:
    print "No touch input detected."
    print "Please make sure you have entered correct touch panel name in user settings."
    print "Quitting in 10 seconds."
    time.sleep(10)
    quit()

device = evdev.InputDevice(input_node)
# print device
# print device.capabilities(verbose=True)
# print device.active_keys(verbose=True)

def rclick():
    if right_click_method == "xdotool":
        # proc = subprocess.Popen("eval $(xdotool getmouselocation --shell) && echo $X $Y", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True ).communicate()
        # print proc[0]
        # p = proc[0].strip('\n')
        # xc = int(p.partition(' ')[0])
        # yc = int(p.partition(' ')[2])
        # print xc, yc
        # subprocess.Popen(["xdotool", "mousemove", "--sync", str(xc), str(yc)], shell = False)
        subprocess.Popen(["xdotool", "click", "3"], stdout=subprocess.PIPE)
    elif right_click_method == "pymouse":
        mouse.click(mouse.position()[0], mouse.position()[1], 2)

for event in device.read_loop():
    # print(evdev.util.categorize(event))
    if event.code == 330 and event.value == 1:
        touch_time = Decimal(str(event.sec) + "." + str(event.usec))
        # print touch_time
        t = Timer(minimum_long_press_time, lp, [touch_time])
        t.daemon = True
        t.start()

    if event.code == 330 and event.value == 0:
        lift_time = Decimal(str(event.sec) + "." + str(event.usec))
        # print lift_time
    else:
        lift_time = None

    if event.code == 47 and event.value == 0:
        finger0_time = Decimal(str(event.sec) + "." + str(event.usec))
        # print finger0_time

    if event.code == 47 and event.value == 1:
        finger1_time = Decimal(str(event.sec) + "." + str(event.usec))
        # print finger1_time

    if event.code == 47 and event.value == 2:
        finger2_time = Decimal(str(event.sec) + "." + str(event.usec))
        # print finger2_time

    if event.code == 57 and event.value > -1:
        abs_touch_time = Decimal(str(event.sec) + "." + str(event.usec))
        # print abs_touch_time
        t = Timer(minimum_long_press_time, lp, [abs_touch_time])
        t.daemon = True
        t.start()

    if event.code == 57 and event.value == -1:
        abs_lift_time = Decimal(str(event.sec) + "." + str(event.usec))
        # print abs_lift_time
    else:
        abs_lift_time = None

    if touch_time != None and lift_time == None and long_press_behavior == "smartphone":
        if t.is_alive() == False and long_press_done == False:
            if enable_long_press == True:
                print "smartphone long press"
                rclick()
                long_press_done = True
                t.cancel()
                t.join()

    if touch_time != None and lift_time != None and enable_long_press == True:
        diff = lift_time - touch_time
        # print diff
        if diff >= minimum_long_press_time and long_press_behavior == "pc":
            print "pc long press"
            rclick()

    if event.code == 330 and event.value == 0:
        if long_press_done == True and long_press_behavior == "smartphone":
            rclick()
        long_press_done = False
        touch_time = None

    if finger0_time != None and finger1_time != None and enable_two_finger_tap == True:
        if event.code == 330 and event.value == 0:
            if finger0_time == finger1_time:
                print "Two finger tap"
                u = subprocess.Popen(["xdotool", "click", "3"])