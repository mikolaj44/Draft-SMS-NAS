from ..utils.colors import *

from ..actions.list_files import *
from ..actions.load_file import *
from ..actions.log_out import *
from ..actions.remove_file import *
from ..actions.store_file import *

from .router import router_manager
from .router import file_manager

from . import config_manager
from . import ip_manager

from importlib.resources import files
import stdiomask
import atexit
import os

menu_actions = [ListFiles("View the list of all saved files"), LoadFile("Load a file"), StoreFile("Store a file"), RemoveFile("Remove a file"), LogOut("Log out and quit")]
special_quit_password = "quitsmsnas"

def safe_exit() -> None:
    try:
        router_manager.log_out()
    finally:
        os._exit(status=os.EX_OK)

atexit.register(safe_exit)

def log_in() -> bool:
    print("\nPlease enter your router password to authorize: (commonly \"admin\")\n")

    while True:
        password = str(stdiomask.getpass())

        if(password == special_quit_password):
            return False
        elif(router_manager.authorize(config_manager.user_config["url"], password)):
            break

        print(f"\nPlease enter the password again or edit your config file to include the correct url. You can also type {special_quit_password} to quit.\n")

    print(GREEN + "\nLogged in successfully!\n" + RESET)

    return True
        
def choice_is_valid(choice : str) -> None:
    if(not choice.isdigit()):
        return False
    
    num = int(choice)

    return num >= 1 and num <= len(menu_actions)

def menu_loop() -> None:
    longest_description_length = 0

    for action in menu_actions:
        length = len(action.description)
        if(length > longest_description_length):
            longest_description_length = length

    while True:
        print(LIGHT_GREEN + "Possible actions:\n" + LIGHT_WHITE + NEGATIVE)

        for i in range(len(menu_actions)):
            print(f"[{i + 1}] " + menu_actions[i].description + " " * (longest_description_length + 1 - len(menu_actions[i].description)))

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

def display_welcome_message() -> None:
    print("\n" + LIGHT_GREEN + "Welcome to Draft SMS \"NAS\"!" + RESET)

    if (config_manager.user_config["show-warnings"] == True):
        print("\n" + RED + "Keep in mind that you can't manually save messages to the draft inbox if you want this program to work correctly - it will clear all of them\nwhen using it for the first time, but not later, so you will have to manually remove everything before the first (file list) message\n" + RESET)

        print(RED + "Remember that this tool requires your MR series router to have SMS support (LTE, SIM card) and will clean your SMS draft inbox in order to prepare the memory.\n")
        print("Your router internal memory is VERY small, the draft inbox on the TL-MR150 is probably like 5 MB in size, so don't save \"big\" files, maybe up to like 100 kilobytes.\n")
    
        print(YELLOW + "You can disable these warnings in your user_config.json file." + RESET)

def main() -> None:    
    config_manager.set_config()

    display_welcome_message()

    ip_manager.set_ip()
    config_manager.update_config()

    if(not log_in()):
        safe_exit()

    if(not file_manager.set_config_num_messages_per_page()):
        safe_exit()
    config_manager.update_config()

    if(not file_manager.prepare_memory()):
        safe_exit()
    config_manager.update_config()

    menu_loop()

    safe_exit()