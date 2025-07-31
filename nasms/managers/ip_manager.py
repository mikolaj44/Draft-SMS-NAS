from importlib.resources import files
import ipaddress

from ..utils.colors import *

from . import config_manager

def ip_is_valid(ip : str) -> bool:
    try:
        ipaddress.ip_interface(ip)
        return True
    except ValueError:
        return False

def get_ip() -> None:
    ip = config_manager.user_config["url"]

    if(ip_is_valid(ip)):
        return

    print(LIGHT_GREEN + "Please enter your router private ip:\n" + RESET)

    while (True):
        ip = input()

        if(ip_is_valid(ip)):
            break
        else:
            print(RED + "Please enter a valid IPv4 address.\n" + RESET)

    config_manager.user_config["url"] = ip