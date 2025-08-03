from .menu_action import *

from ..managers.router import file_manager
from ..managers.router import file_helpers

def get_formatted_list(file_list: str) -> str:
    names = file_helpers.get_file_names(file_list)
    total_num_messages = file_helpers.get_num_sent_messages(file_list)
    start_indices = file_helpers.get_file_start_indices(file_list) + [total_num_messages + 1]

    formatted_list = ""

    for i in range(len(start_indices) - 1):
        formatted_list += f"{str(i + 1)}: {names[i]} (Number of messages: {start_indices[i + 1] - start_indices[i]})\n"

    return formatted_list

class ListFiles(MenuAction):
    def select(self):
        file_list = file_manager.get_file_list()

        print("\n=================================")
        print(f"Number of saved files: {file_helpers.get_num_files(file_list)} ({file_helpers.get_num_sent_messages(file_list)} total messages), list:")
        print(f"\n{get_formatted_list(file_list)}")
        print("Raw data list:\n\n" + file_list)
        print("=================================\n")