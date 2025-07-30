from importlib.resources import files
import ipaddress

from ..utils.colors import *

from . import config_manager

def ipIsValid(ip : str) -> bool:
    try:
        ipaddress.ip_interface(ip)
        return True
    except ValueError:
        return False

def getIP() -> None:
    ip = config_manager.config["url"]

    if(ipIsValid(ip)):
        return

    print(LIGHT_GREEN + "Please enter your router private ip:\n" + RESET)

    while (True):
        ip = input()

        if(ipIsValid(ip)):
            break
        else:
            print(RED + "Please enter a valid IPv4 address.\n" + RESET)

    config_manager.config["url"] = ip