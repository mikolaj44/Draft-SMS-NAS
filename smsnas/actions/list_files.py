from .menu_action import *

from ..managers.router import file_manager
from ..managers.router import file_helpers
from ..managers import config_manager

def get_formatted_list(file_list: str) -> str:
    names = file_helpers.get_file_names(file_list)
    total_num_messages = file_helpers.get_num_sent_messages(file_list)
    start_indices = file_helpers.get_file_start_indices(file_list) + [total_num_messages + 1]
    max_bytes_per_message = config_manager.program_config["max_bytes_per_message"]

    formatted_list = ""

    start_indices_length = len(start_indices)

    for i in range(start_indices_length - 2, -1, -1):
        num_messages = start_indices[i + 1] - start_indices[i]
        formatted_list += f"{str(start_indices_length - i - 1)}: {names[i]} (Number of messages: {num_messages}, max {num_messages * max_bytes_per_message} bytes)\n"

    return formatted_list

class ListFiles(MenuAction):
    def select(self):
        print("\nGetting the file list...")
        file_list = file_manager.get_file_list()

        file_manager.quit_on_incorrect_file_list(file_list)

        print(f"\nNumber of saved files: {file_helpers.get_num_files(file_list)} ({file_helpers.get_num_sent_messages(file_list)} total messages), list: (recently saved on the top)")
        print(f"\n{get_formatted_list(file_list)}")
        print("Raw data list:\n\n" + file_list + "\n")