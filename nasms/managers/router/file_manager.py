from ...utils.colors import *
from ...utils.proceed_prompt import *
from ...utils.math_utils import *

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

mime = magic.Magic(mime=True)

MAX_FILE_NAME_LENGTH = 4

def file_name_is_valid(name: str) -> bool:
    length = len(name)

    return length >= 1 and length <= file_manager.MAX_FILE_NAME_LENGTH and name.isalnum()

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

    print("\nWiping done! Thank you for your patience.\n")

    config_manager.program_config["is_initial_setup"] = False

    router_manager.send_messages(messages=["list"])

    return True

def get_file_list() -> str:
    return router_manager.get_messages()[0]

def get_file_names(file_list: str) -> list[str]:
    parts = file_list.split(";")

    names = []

    for part in parts:
        names.append(part[:MAX_FILE_NAME_LENGTH])

    return names

def get_next_file_start_index(file_list : str) -> int:
    if(file_list == ";"):
        return 1
    
    parts = file_list.split(";")
    
    return int(parts[-1][MAX_FILE_NAME_LENGTH:])

def update_file_list(old_content: str, name: str, start_index: int) -> None:
    print("\nSending a new file list...")
    router_manager.send_messages(messages=[old_content + name + start_index])

    print("\nRemoving the old file list...")
    router_manager.remove_messages(start_index=1, num_messages=1)

def get_file_bytes(file_path: str) -> bytes:    
    with open(file_path, 'rb') as file:
        return file.read()

def send_file_messages(file_bytes: bytes) -> bool:
    length = len(file_bytes)
    max_bytes_per_message = config_manager.program_config["max_bytes_per_message"]

    num_messages = ceildiv(length, max_bytes_per_message)

    if(not proceed_prompt(f"\n{num_messages} messages will be sent." + RED + " This process can't be suspended until it's finished!" + RESET)):
        return False
    
    messages = []
    
    for byte_index in range(0, length):
        messages.append(file_bytes[byte_index:max_bytes_per_message])

    print(messages)

    router_manager.send_messages(messages)
    
    return True

def store_file(name: str, file_path: str) -> bool:
    file_list = get_file_list()[1:]

    names = get_file_names(file_list)

    if(name in names):
        print("\nName already exists. Please provide a different name. Already used: " + str(names))
        return False

    file_start_index = get_next_file_start_index(file_list)

    file_bytes = get_file_bytes(file_path)

    update_file_list(old_content=file_list, name=name, start_index=file_start_index)

    return send_file_messages(file_bytes=file_bytes)