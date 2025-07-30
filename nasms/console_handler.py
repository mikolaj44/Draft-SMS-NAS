from .utils.colors import *
from . import router_manager
from . import config_manager
from . import ip_manager

from importlib.resources import files
import stdiomask
import atexit

def atExit() -> None:
    try:
        router_manager.logOut()
    except:
        return

atexit.register(atExit)

def logIn() -> None:
    print("Please enter your router password to authorize: (commonly \"admin\")\n")

    while True:
        if(router_manager.authorize(config_manager.config["url"], str(stdiomask.getpass()))):
            break

        print("\nPlease enter the password again or edit your config file to include the correct url.\n")

    print(LIGHT_GREEN + "Logged in successfully!\n" + RESET)

def handle_action(index: int) -> None:
    match index:
        case 1:
            return
        case 2:
            return
        case 3:
            return
        case 4:
            return
        case 5:
            return
        case _:
            return
        
def choice_is_valid(choice : str) -> None:
    if(not choice.isdigit()):
        return False
    
    num = int(choice)

    return num >= 1 and num <= 5

def main() -> None:    
    config_manager.getConfig()

    print("\n" + LIGHT_GREEN + "Welcome to Draft SMS \"NAS\"!\n" + RESET)
    
    if (config_manager.config["show-warnings"] == "True"):
        print(RED + "WARNING: Remember that this tool requires your router to have SMS support (LTE, SIM card) and will clean your SMS draft inbox in order to prepare the memory.\n")
        print("WARNING: Your router internal memory is VERY small, the draft inbox on the TL-MR150 is probably like 5 MB in size, so don't save \"big\" files.\n")
    
        print(YELLOW + "You can disable the warnings in your config.txt file.\n" + RESET)

    ip_manager.getIP()
    config_manager.updateConfig()

    logIn()

    print(LIGHT_GREEN + "Possible actions:\n" + LIGHT_BLUE)
    print("[1] View the list of all saved files")
    print("[2] Store a file")
    print("[3] Load a file")
    print("[4] Remove a file")
    print("[5] Log out and quit\n" + RESET)

    choice = ""

    while(True):
        print("Enter your choice: ", end="")

        choice = input()

        if(not choice_is_valid(choice)):
            print(RED + "\nPlease provide a number between 1 and 5.\n" + RESET)
        else:
            break

    handle_action(choice)