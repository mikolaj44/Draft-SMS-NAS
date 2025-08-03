from ...utils.colors import *
from ...utils.proceed_prompt import *
from ...utils.math_utils import *

from .file_helpers import *

from ...actions.list_files import *
from ...actions.load_file import *
from ...actions.log_out import *
from ...actions.remove_file import *
from ...actions.store_file import *

from ..router import router_manager
from .. import config_manager

from importlib.resources import files

MAX_FILE_NAME_LENGTH = 4

def set_config_num_messages_per_page() -> bool:
    num_messages_per_page = config_manager.program_config["num_messages_per_page"]
                        
    if(isinstance(num_messages_per_page, int) and num_messages_per_page > 0):
        return True
    
    num_messages_to_send = config_manager.program_config["num_messages_to_send_to_find_num_per_page"]

    if(not proceed_prompt(f"We need to save and then remove {num_messages_to_send} messages to find out how many per page there are.")):
        return False
        
    print(f"Sending {num_messages_to_send} messages to get the number of messages per page..." + RED + " Dont't quit!" + RESET)
    
    router_manager.send_messages(messages=["a"] * num_messages_to_send)

    num_messages_per_page = len(router_manager.get_first_page_messages())

    print(f"Removing {num_messages_to_send} messages..." + RED + " Dont't quit!" + RESET)

    router_manager.remove_messages(start_index=1, num_messages=num_messages_to_send)

    print(f"\nDone removing. There are {num_messages_per_page} messages per page.\n")

    config_manager.program_config["num_messages_per_page"] = num_messages_per_page

    return True

def prepare_memory() -> bool:
    if(config_manager.program_config["is_initial_setup"] == False):
        return True
    
    if(not proceed_prompt("The draft inbox needs to be wiped.")):
        return False

    print("\nRemoving in progress. This will take a while if you have multiple pages - deleting messages is the slowest part of this 'system'. It's also probably the single action in this program that you can stop and come back to it later as it just clears the inbox.")
    
    router_manager.remove_all_messages()

    router_manager.send_messages(messages=["0;"])

    print("\nWiping done! Thank you for your patience.\n")

    config_manager.program_config["is_initial_setup"] = False

    return True

def get_file_list() -> str:
    return router_manager.get_messages()[0]

def update_file_list(new_content: str) -> None:
    print("\nSending a new file list...")
    router_manager.send_messages(messages=[new_content])

    print("\nRemoving the old file list...")
    router_manager.remove_messages(start_index=2, num_messages=1)

def move_file_list(new_content: str, start_index: int, num_messages: int) -> None:
    print("\nMoving the updated file list to the front...")
    router_manager.send_messages(messages=[new_content])

    print("\nRemoving the old file list...")
    router_manager.remove_messages(start_index=num_messages + 2, num_messages=1)
    
def send_file_messages(file_bytes: bytes, num_messages: int, new_file_list_content: str) -> bool:
    update_file_list(new_file_list_content)

    length = len(file_bytes)

    file_bytes = file_bytes[2:length - 1]

    length -= 3

    max_bytes_per_message = config_manager.program_config["max_bytes_per_message"]

    if(not proceed_prompt(f"\n{num_messages} messages will be sent." + RED + " This process can't be suspended until it's finished!" + RESET)):
        return False
    
    messages = [file_bytes[i:i + max_bytes_per_message] for i in range(0, length, max_bytes_per_message)]

    # print(messages)

    print(f"\nSending {num_messages} messages. " + RED + "Don't quit." + RESET)

    router_manager.send_messages(messages)

    return True