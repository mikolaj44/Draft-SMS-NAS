from ...utils.colors import *
from ...utils.proceed_prompt import *
from ...utils.math_utils import *

from ...actions import list_files

from .. import config_manager
from .. import console_handler
from . import file_manager

from importlib.resources import files

from tkinter import Tk
from tkinter.filedialog import askopenfilename

def get_file_names(file_list: str, padded: bool = False) -> list[str]:
    parts = file_list.split(";")

    names = []

    for part in parts:
        names.append(part[:file_manager.MAX_FILE_NAME_LENGTH] if padded else part[:file_manager.MAX_FILE_NAME_LENGTH].replace("_", ""))

    return list(filter(("").__ne__, names))[1:]

def quit_on_incorrect_file_list(file_list: str):
    try:
        list_files.get_formatted_list(file_list)
    except Exception as e:
        print(RED + f"\nYour memory is not set up correctly. Please fix it manually, there may be some leading messages before the file list. Got exception: " + LIGHT_PURPLE + str(e) + RESET)
        console_handler.safe_exit()

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
    Tk().withdraw()
    return askopenfilename()

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