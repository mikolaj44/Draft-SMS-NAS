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
import datetime
import os

menu_actions = [ListFiles("View the list of all saved files"), StoreFile("Store a file"), LoadFile("Load a file"), RemoveFile("Remove a file"), LogOut("Log out and quit")]

def safe_exit() -> None:
    try:
        router_manager.log_out()
        os._exit(status=os.EX_OK)
    except Exception as e:
        print(RED + "Could not exit. Reason: " + PURPLE + e + RESET)
        return

atexit.register(safe_exit)

def log_in() -> None:
    print("Please enter your router password to authorize: (commonly \"admin\")\n")

    while True:
        if(router_manager.authorize(config_manager.user_config["url"], str(stdiomask.getpass()))):
            break

        print("\nPlease enter the password again or edit your config file to include the correct url.\n")

    print(LIGHT_GREEN + "\nLogged in successfully!\n" + RESET)
        
def choice_is_valid(choice : str) -> None:
    if(not choice.isdigit()):
        return False
    
    num = int(choice)

    return num >= 1 and num <= len(menu_actions)

def menu_loop() -> None:
    while True:
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

def display_welcome_message() -> None:
    print("\n" + LIGHT_GREEN + "Welcome to Draft SMS \"NAS\"!" + RESET)

    print("\n" + RED + "Keep in mind that you can't manually save messages to the draft inbox if you want this program to work correctly - it will clear all of them when using it for the first time, but not later, so you will have to manually remove everything before the first (file list) message\n" + RESET)

    if (config_manager.user_config["show-warnings"] == True):
        print(RED + "WARNING: Remember that this tool requires your router to have SMS support (LTE, SIM card) and will clean your SMS draft inbox in order to prepare the memory.\n")
        print("WARNING: Your router internal memory is VERY small, the draft inbox on the TL-MR150 is probably like 5 MB in size, so don't save \"big\" files.\n")
    
        print(YELLOW + "You can disable the warnings in your config.txt file.\n" + RESET)

def main() -> None:    
    config_manager.set_config()

    display_welcome_message()

    ip_manager.set_ip()
    config_manager.update_config()

    log_in()

    if(not file_manager.set_config_num_messages_per_page()):
        safe_exit()
    config_manager.update_config()

    if(not file_manager.prepare_memory()):
        safe_exit()
    config_manager.update_config()

    menu_loop()

    safe_exit()

    # list_ = router_manager.get_messages(startIndex=1, numMessages=6)
    # print("===")

    # for item in list_:
    #     print(item + "\n")

    # start = datetime.datetime.now()

    # #router_manager.router.delete_sms_page(pageIndex=1, maxMessagesPerPage=8, deleteFromDraft=True)

    # #for i in range(1, 9):
    # #    router_manager.router.delete_sms(pageIndex=1, smsIndex=i, deleteFromDraft=True)

    # # router_manager.send_messages(["a" * 1430] * 50)
    
    # router_manager.router.delete_smses(start_sms_index=1, num_smses=8, max_messages_per_page=8, delete_from_draft=True)

    # end = datetime.datetime.now()

    # print(end - start)

    # quit()