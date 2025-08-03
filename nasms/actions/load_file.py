from .menu_action import *

from ..managers.router import file_manager
from ..managers.router import router_manager

class LoadFile(MenuAction):
    def select(self):
        file_list = file_manager.get_file_list()

        print(f"\nStored file names: {file_manager.get_file_names(file_list)}")

        name = file_manager.get_file_name(file_list, require_new_name=False)

        start_index, num_messages = file_manager.get_file_start_index_and_length_from_beginning(file_list=file_list, file_name=name)

        print(f"\nGetting the file messages, please wait...")
        
        print(start_index, num_messages)

        messages = router_manager.get_messages(start_index=start_index, num_messages=num_messages)
        
        print(f"\nWriting the file...")

        file_content = ""

        for message in messages[::-1]:
            file_content += message

        print(messages)
        print(len(messages))

        with open("./loaded_file", "w") as file:
            file.write(file_content.encode("utf-8").decode("unicode_escape"))