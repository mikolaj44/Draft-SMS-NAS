from ...utils.colors import *
from ...utils.proceed_prompt import *
from ...utils.math_utils import *

from ...actions.list_files import *
from ...actions.load_file import *
from ...actions.log_out import *
from ...actions.remove_file import *
from ...actions.store_file import *

from .. import config_manager
from . import file_manager

from importlib.resources import files

import easygui

def get_file_names(file_list: str, padded: bool = False) -> list[str]:
    parts = file_list.split(";")

    names = []

    for part in parts:
        names.append(part[:file_manager.MAX_FILE_NAME_LENGTH] if padded else part[:file_manager.MAX_FILE_NAME_LENGTH].replace("_", ""))

    return list(filter(("").__ne__, names))[1:]

def get_file_start_indices(file_list: str) -> list[int]:
    parts = file_list.split(";")

    indices = []

    for part in parts:
        indices.append(part[file_manager.MAX_FILE_NAME_LENGTH:])

    return list(filter(("").__ne__, [(int(i) if i != "" else i) for i in indices]))

def get_file_start_index_and_length_from_beginning(file_list: str, file_name: str) -> tuple[int, int]:
    names = get_file_names(file_list)
    total_num_messages = get_num_sent_messages(file_list)
    start_indices = get_file_start_indices(file_list) + [total_num_messages + 1]

    name_index = names.index(file_name)

    length = start_indices[name_index + 1] - start_indices[name_index]

    start_index =  total_num_messages + 3 - start_indices[name_index] - length

    return start_index, length

def get_num_sent_messages(file_list: str) -> int:
    parts = file_list.split(";")

    return int(parts[0])

def get_num_files(file_list: str) -> int:
    return file_list.count(";") - 1

def get_num_messages_for_file(file_bytes: bytes) -> int:
    max_bytes_per_message = config_manager.program_config["max_bytes_per_message"]

    return ceildiv(len(file_bytes), max_bytes_per_message)

def get_next_file_start_index(file_list : str) -> int:    
    return get_num_sent_messages(file_list) + 1

def get_file_bytes(file_path: str) -> bytes:    
    with open(file_path, 'rb') as file:
        return str(file.read())

def get_file_path() -> str:
    return easygui.fileopenbox(msg="Choose your file")

def file_name_is_valid(name: str) -> bool:
    length = len(name)

    return length >= 1 and length <= file_manager.MAX_FILE_NAME_LENGTH and name.isalnum()

def get_file_name(file_list: str, require_new_name: bool) -> str:
    names = get_file_names(file_list)

    while True:
        print("\nPlease enter the file name, max 4 characters and only letters and numbers: ", end="")

        name = input()

        if(not file_name_is_valid(name)):
            print(RED + "\nTry again." + RESET)
        elif(require_new_name and name in names):
            print(RED + "\nName already exists. Already used: " + RESET + str(names))
        elif(not require_new_name and name not in names):
            print(RED + "\nName doesn't exist. Stored file names: " + RESET + str(names))
        else:
            return name + ("_" * (file_manager.MAX_FILE_NAME_LENGTH - len(name)) if require_new_name else "")