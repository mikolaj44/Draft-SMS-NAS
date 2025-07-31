from ..utils.colors import *

from ..data.actions.list_files import *
from ..data.actions.load_file import *
from ..data.actions.log_out import *
from ..data.actions.remove_file import *
from ..data.actions.store_file import *

from .router import router_manager
from .router import message_manager

from . import config_manager
from . import ip_manager

from importlib.resources import files
import stdiomask
import atexit

menu_actions = [ListFiles("View the list of all saved files"), StoreFile("Store a file"), LoadFile("Load a file"), RemoveFile("Remove a file"), LogOut("Log out and quit")]

def at_exit() -> None:
    try:
        router_manager.logOut()
    except:
        return

atexit.register(at_exit)

def log_in() -> None:
    print("Please enter your router password to authorize: (commonly \"admin\")\n")

    while True:
        if(router_manager.authorize(config_manager.user_config["url"], str(stdiomask.getpass()))):
            break

        print("\nPlease enter the password again or edit your config file to include the correct url.\n")

    print(LIGHT_GREEN + "Logged in successfully!\n" + RESET)
        
def choice_is_valid(choice : str) -> None:
    if(not choice.isdigit()):
        return False
    
    num = int(choice)

    return num >= 1 and num <= len(menu_actions)

def main() -> None:    
    config_manager.get_config()

    print("\n" + LIGHT_GREEN + "Welcome to Draft SMS \"NAS\"!\n" + RESET)
    
    if (config_manager.user_config["show-warnings"] == True):
        print(RED + "WARNING: Remember that this tool requires your router to have SMS support (LTE, SIM card) and will clean your SMS draft inbox in order to prepare the memory.\n")
        print("WARNING: Your router internal memory is VERY small, the draft inbox on the TL-MR150 is probably like 5 MB in size, so don't save \"big\" files.\n")
    
        print(YELLOW + "You can disable the warnings in your config.txt file.\n" + RESET)

    ip_manager.get_ip()
    config_manager.update_config()

    log_in()

    message_manager.get_num_messages_per_page()
    config_manager.update_config()

    if(not message_manager.prepare_memory()):
        return
    config_manager.update_config()

    print(LIGHT_GREEN + "Possible actions:\n" + LIGHT_BLUE)

    for i in range(len(menu_actions)):
        print(f"[{i + 1}] " + menu_actions[i].description)

    print(RESET)

    choice = -1

    while(True):
        print("Enter your choice: ", end="")

        choice = input()

        if(not choice_is_valid(choice)):
            print(RED + "\nPlease provide a number between 1 and 5.\n" + RESET)
        else:
            choice = int(choice)
            break

    menu_actions[choice - 1].select()