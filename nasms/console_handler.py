from .utils.colors import *
from .router_manager import *

from importlib.resources import files
import json
import ipaddress
import stdiomask

config = ""
file = None

def getConfig() -> None:
    global config, file
    
    file = files("nasms") / "config.json"

    with file.open("r+", encoding="utf-8") as f:
        config = json.load(f)

def getIP() -> None:
    print(LIGHT_GREEN + "Please enter your router private ip:\n" + RESET)

    ip = ""

    while (True):
        ip = input()

        try:
            result = ipaddress.ip_interface(ip)
            break
        except ValueError as ve:
            print(RED + "Please enter a valid IPv4 address.\n" + RESET)

    config["url"] = ip

def logIn() -> None:
    print("Please enter your router password to authorize: (commonly \"admin\")\n")

    loggedIn = False

    while True:
        password = str(stdiomask.getpass())

        loggedIn = authorize(config["url"], password)

        if(loggedIn):
            break

        print("\nPlease enter the password again or edit your config file to include the correct url.\n")

    print(LIGHT_GREEN + "Logged in successfully!\n" + RESET)

def main() -> None:
    getConfig()

    print("\n" + LIGHT_GREEN + "Welcome to Draft SMS \"NAS\"!\n" + RESET)
    
    if (config["show-warnings"] == "True"):
        print(RED + "WARNING: Remember that this tool requires your router to have SMS support (LTE, SIM card) and will clean your SMS draft inbox in order to prepare the memory.\n")
        print("WARNING: Your router internal memory is VERY small, the draft inbox on the TL-MR150 is probably like 5 MB in size, so don't save \"big\" files.\n")
    
        print(YELLOW + "You can disable the warnings in your config.txt file.\n" + RESET)

    if (config["url"] == ""):
        getIP()

    logIn()

    print("[1] ")

    with file.open("r+", encoding="utf-8") as f:
        json.dump(config, f)