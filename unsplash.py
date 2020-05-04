import platform
import os
import urllib.request
import time
import ctypes
import traceback
import sys
import time
import settings

__title__ = 'Unsplash Wallpaper'
__version__ = "1.3"
__author__ = 'tobimori, maschhoff'
# last edited @ 22.10.2018

#TODO update ready
def get_screensize(multiplier):
    try:
        user32 = ctypes.windll.user32
        screensize = f"{user32.GetSystemMetrics(78)*multiplier}x{user32.GetSystemMetrics(79)*multiplier}"
        print(f"\r[+] Status: Detected virtual monitor size {user32.GetSystemMetrics(78)}x{user32.GetSystemMetrics(79)}.", end="")
        if multiplier > 1:
            print(f"\r[+] Status: Multiplying to {screensize} for better quality.", end="")
        return screensize
    except:
        print(f"\r[-] Status: Encountered some problems while detecting your display size.", end="")
        traceback.print_exc()
        sys.exit(1)


def get_image(multiplier):
    directory = os.getcwd() + "/.unsplash"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("\r[+] Status: Create temporary directory", end="")
    global filepath
    filepath = directory + "/" + str(time.time()) + ".jpg"
    print(f"\r[+] Status: Starting download...", end="")
    try:
        screensize = get_screensize(multiplier)
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



def main():
        print(f"{__title__} v{__version__} by {__author__}")
        osvar = platform.system()

        #TODO Linux
        if osvar == "Windows":
                windows(get_image(1))
        else:
            print("\r[-] Status: Sorry, only supporting Windows right now. Feel free to fork and add support ;)", end="")
            
