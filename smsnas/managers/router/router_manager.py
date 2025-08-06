from tplinkrouterc6udraftsms import (
    TplinkRouterProvider,
    TPLinkMRClient
)

from tplinkrouterc6udraftsms.common.exception import *

from ...utils.colors import *
from ...utils.math_utils import *

from ...managers import config_manager

import tqdm

router = None

PHONE_NUMBER = "123456789"

def authorize(url : str, password : str) -> bool:
    global router

    print("\nLogging in, please wait...")

    try:
        router = TplinkRouterProvider.get_client(f"http://{url}", password)

        if(not isinstance(router, TPLinkMRClient)):
            raise ValueError("Your router is not an MR model.")

        router.authorize()
    except Exception as e:
        print(RED + "\nCould not log in, reason from the tplinkrouterc6u library: " + LIGHT_PURPLE + str(e) + RESET)
        return False
    return True

def log_out() -> None:    
    router.logout()

def send_messages(messages: list[str]) -> None:
    router.send_sms(phone_number=PHONE_NUMBER, messages=messages, draft=True, enable_tqdm=True)

def get_messages(start_index: int = 1, num_messages: int = 1) -> list[str]:
    max_messages_per_page = config_manager.program_config["num_messages_per_page"]

    start_page_index = ceildiv(start_index, max_messages_per_page)
    end_page_index = ceildiv(start_index + num_messages, max_messages_per_page)

    messages = []

    for page_index in tqdm.tqdm(range(start_page_index, end_page_index + 1)):
        messages += router.get_sms_content(get_from_draft=True, page_index=page_index)

    start_cutoff = (start_index % max_messages_per_page) - 1

    num_redundant_messages = max(0, len(messages) - start_cutoff - num_messages)

    return messages[start_cutoff : len(messages) - num_redundant_messages]

def get_first_page_messages() -> list[str]:
    return router.get_sms_content(get_from_draft=True, page_index=1)

def remove_messages(start_index: int, num_messages: int) -> bool:
    max_messages_per_page = config_manager.program_config["num_messages_per_page"]

    return router.delete_smses(start_sms_index=start_index, num_smses=num_messages, max_messages_per_page=max_messages_per_page, delete_from_draft=True, enable_tqdm=True)

def remove_all_messages() -> None:
    can_remove = True

    page_index = 1
    max_messages_per_page = config_manager.program_config["num_messages_per_page"] 

    while(can_remove):
        print(f"\nTrying to remove page {page_index}...")

        can_remove = router.delete_sms_page(page_index=1, max_messages_per_page=max_messages_per_page, delete_from_draft=True)
        
        print(f"Removed page {page_index}.")

        page_index += 1