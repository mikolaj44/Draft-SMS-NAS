from ...utils.colors import *

from ...data.actions.list_files import *
from ...data.actions.load_file import *
from ...data.actions.log_out import *
from ...data.actions.remove_file import *
from ...data.actions.store_file import *

from ..router import router_manager
from .. import config_manager
from .. import ip_manager

from importlib.resources import files
import stdiomask
import atexit

def get_num_messages_per_page() -> None:
    number = config_manager.program_config["num_messages_per_page"]
                        
    if(isinstance(number, int) and number > 0):
        return
    
    test_number = config_manager.program_config["num_messages_to_send_to_find_num_per_page"]
        
    print(f"Sending {test_number} messages to get the number of messages per page...")
    
    router_manager.send_data(messages=["a" * test_number])

    num_messages_per_page = len(router_manager.get_first_page_messages())

    print(f"\nThere are {num_messages_per_page} messages per page.\n")

    config_manager.program_config["num_messages_per_page"] = num_messages_per_page

def prepare_memory() -> bool:
    if(config_manager.program_config["is_initial_setup"] == False):
        return
    
    print("The draft inbox needs to be wiped. Do you wish to proceed? [Y/N]: ", end="")

    while True:
        result = input()

        if(result.lower() == "y"):
            break

        if(result.lower() == "n"):
            return False
        
        print("\nPlease provide a valid choice [Y/N]: ", end="")
    
    # TODO: remove all messages from the draft

    print("wiping...")

    config_manager.program_config["is_initial_setup"] = False

    return True