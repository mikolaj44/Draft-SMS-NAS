from .menu_action import *

from ..utils.colors import *

from ..managers.router import file_manager
from ..managers.router import router_manager

import magic
import mimetypes
import codecs
import os

class LoadFile(MenuAction):
    def select(self):
        print("\nGetting the file list...")
        file_list = file_manager.get_file_list()

        file_manager.quit_on_incorrect_file_list(file_list)

        print(f"\nStored file names: {file_manager.get_file_names(file_list)}")

        name = file_manager.get_file_name(file_list, require_new_name=False)

        start_index, num_messages = file_manager.get_file_start_index_and_length_from_beginning(file_list=file_list, file_name=name)

        print(f"\nGetting the file messages ({num_messages}), please wait...")
        
        messages = router_manager.get_messages(start_index=start_index, num_messages=num_messages)
        
        print(f"\nWriting the file...")

        file_content = ""

        for message in messages[::-1]:
            file_content += message

        mime = magic.Magic(mime=True)

        file_bytes = codecs.decode(file_content, "unicode_escape").encode("latin1")

        extension = mimetypes.guess_extension(mime.from_buffer(file_bytes))

        if(extension == None):
            extension = ""

        file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "loaded_files", f"{name}{extension}"))

        with open(file_path, "wb") as file:
            file.write(file_bytes)

        print(GREEN + f"\nFile sucessfully saved at {file_path}" + RESET + "\n")