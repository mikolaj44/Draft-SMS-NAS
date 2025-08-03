from .menu_action import *

from ..managers.router import file_manager

class StoreFile(MenuAction):
    def select(self):
        file_path = file_manager.get_file_path()

        if(file_path == ()):
            print("\nNo file was chosen.\n")
            return
            
        file_list = file_manager.get_file_list()

        name = file_manager.get_file_name(file_list, require_new_name=True)

        file_bytes = file_manager.get_file_bytes(file_path)

        file_start_index = file_manager.get_next_file_start_index(file_list)

        num_messages = file_manager.get_num_messages_for_file(file_bytes)

        new_file_list_content = file_manager.get_new_file_list_content(old_content=file_list, name=name, start_index=file_start_index, num_messages=num_messages)

        if(not file_manager.send_file_messages(file_bytes=file_bytes, num_messages=num_messages, new_file_list_content=new_file_list_content)):
            return
        
        file_manager.move_file_list(new_content=new_file_list_content, start_index=file_start_index, num_messages=num_messages)

        print("\nYour file has been successfully saved!\n")