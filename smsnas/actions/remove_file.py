from .menu_action import *

from ..utils.colors import *
from ..utils.proceed_prompt import *

from ..managers.router import file_manager
from ..managers.router import router_manager
from ..managers import console_handler

def get_new_file_list_content(file_list: str, file_name: str, num_messages: int) -> str:
    file_names = file_manager.get_file_names(file_list, padded=True)
    start_indices = file_manager.get_file_start_indices(file_list)
    total_num_messages = file_manager.get_num_sent_messages(file_list)

    start_indices_length = len(start_indices)

    file_name = file_name + ("_" * (file_manager.MAX_FILE_NAME_LENGTH - len(file_name)))

    file_name_index = file_names.index(file_name)

    for i in range(file_name_index + 1, start_indices_length):
        start_indices[i] -= num_messages

    new_file_list = str(total_num_messages - num_messages) + ";"

    for i in range(start_indices_length):
        if(file_names[i] != file_name):
            new_file_list += file_names[i] + str(start_indices[i]) + ";"

    return new_file_list

class RemoveFile(MenuAction):
    def select(self):
        print("\nGetting the file list...")
        file_list = file_manager.get_file_list()

        file_manager.quit_on_incorrect_file_list(file_list)

        print(f"\nStored file names: {file_manager.get_file_names(file_list)}")

        name = file_manager.get_file_name(file_list, require_new_name=False)

        start_index, num_messages = file_manager.get_file_start_index_and_length_from_beginning(file_list=file_list, file_name=name)

        if(not proceed_prompt(f"\nAre you sure you want to remove '{name}'? ({num_messages} messages)\n" + RED + "This will take a while and this process cannot be suspended." + RESET)):
            return
        
        new_file_list = get_new_file_list_content(file_list=file_list, file_name=name, num_messages=num_messages)

        file_manager.move_file_list(new_content=new_file_list, num_messages=0)

        print("\nRemoving the messages...")

        router_manager.remove_messages(start_index=start_index, num_messages=num_messages)
        
        print(GREEN + f"\nFile '{name}' sucessfully removed.\n")