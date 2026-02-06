import platform
import os
import urllib.request
import time
import ctypes
import traceback
import sys
import time
import settings
import subprocess
import getpass
import platform
from screeninfo import get_monitors

__title__ = 'Unsplash Wallpaper'
__version__ = "1.3"
__author__ = 'tobimori, maschhoff'
# last edited @ 22.10.2018

def get_screensize():
    size="1920x1080"
    for m in get_monitors():
        size=str(m.width)+"x"+str(m.height)
        print(size)
    return size


def get_image():
    directory = os.path.dirname(__file__)
    USER_NAME = getpass.getuser()
    osvar = platform.system()

    if osvar == "Windows": 
            directory = r'C:\Users\%s\AppData\Local\unsplashipy' % USER_NAME
    else:
            directory=os.path.dirname(__file__)
    
    global filepath
    filepath = directory + "/" + str(time.time()) + ".jpg"
    print(f"\r[+] Status: Starting download...", end="")
    try:
        screensize = get_screensize()
        config=settings.loadConfig()
        urllib.request.urlretrieve("https://source.unsplash.com/random/" + screensize+"/?"+config["collection"], filepath) # TODO choose image type (nature,...)
        print(f"\r[+] Status: Downloaded image from source.unsplash.com/random/{screensize} to {filepath}", end="")
        return filepath
    except:
        print(f"\r[-] Status: Encountered some problems while downloading the image.", end="")
        traceback.print_exc()
        sys.exit(1)
        
def del_image():
        try:
                os.remove(filepath)
                print(f"\r[+] Temp Image removed", end="")
        except:
                print(f"\r[-] Status: Encountered some problems while removing filepath.", end="")
                traceback.print_exc()
        
        
def windows(filepath_absolute):
            print("\r[+] Status: Detected System: Windows", end="")
            print("\033[0m")
            try:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath_absolute, 0)
                print("\n[+] Status: Done!", end="")
            except:
                print(f"\r[-] Status: Error - Couldn't set your wallpaper.", end="")
                traceback.print_exc()
                sys.exit(1)

#only xfce4         
def linux_xfce(filepath_absolute):
        #get backdrop path by "xfconf-query -c xfce4-desktop -m" than change wallpaper
        args0 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitorLVDS-1/workspace0/last-image", "-s", filepath_absolute]
        args1 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitorLVDS-1/workspace0/image-style", "-s", "3"]
        args2 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitorLVDS-1/workspace0/image-show", "-s", "true"]
        subprocess.Popen(args0)
        subprocess.Popen(args1)
        subprocess.Popen(args2)
        args = ["xfdesktop","--reload"]
        subprocess.Popen(args)

def linux_gnome(filepath_absolute):
    subprocess.run([
    "gsettings",
    "set",
    "org.gnome.desktop.background",
    "picture-uri",
    f"file://{filepath_absolute}"
])



def main():
        print(f"{__title__} v{__version__} by {__author__}")
        osvar = platform.system()

       
        if osvar == "Windows":
                windows(get_image())
        elif osvar == "Linux":
                linux(get_image())
        else:
            print("\r[-] Status: Sorry, only supporting Windows right now. Feel free to fork and add support ;)", end="")
            

