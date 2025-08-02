from tplinkrouterc6udraftsms import (
    TplinkRouterProvider,
    TPLinkMRClient,
)

from tplinkrouterc6udraftsms.common.exception import *

from ...utils.colors import *
from ...utils.math_utils import *

from ...managers import config_manager

router = None

PHONE_NUMBER = "123456789"

def authorize(url : str, password : str) -> bool:
    global router

    print("\nLogging in, please wait...")

    try:
        router = TplinkRouterProvider.get_client(f"http://{url}", password)

        if(not isinstance(router, TPLinkMRClient) and config_manager.user_config["ensure_router_is_MR"] == True):
            raise ValueError("Your router is not an MR model.")

        router.authorize()
    except Exception as e:
        print(RED + "\nCould not log in, reason from the tplinkrouterc6u library: " + PURPLE + str(e) + RESET)
        return False
    return True

def log_out() -> None:    
    router.logout()

def send_messages(messages: list[str]) -> None:
    router.send_sms(phone_number=PHONE_NUMBER, messages=messages, draft=True)

def get_messages(start_index: int = 1, num_messages: int = 1) -> list[str]:
    messages = []
    max_messages_per_page = config_manager.program_config["num_messages_per_page"] 

    for pageIndex in range (ceildiv(start_index, max_messages_per_page), ceildiv(start_index + num_messages, max_messages_per_page) + 1):
        messages += router.get_sms_content(get_from_draft=True, page_index=pageIndex)

    start_cutoff = (start_index % max_messages_per_page) - 1
    end_cutoff = max_messages_per_page - ((start_index + num_messages - 1) % max_messages_per_page)
    length = len(messages)
                                            
    messages = messages[start_cutoff : length if end_cutoff > length else length - end_cutoff]

    return messages

def get_first_page_messages() -> list[str]:
    return router.get_sms_content(get_from_draft=True, page_index=1)

def remove_messages(start_index: int, num_messages: int) -> None:
    max_messages_per_page = config_manager.program_config["num_messages_per_page"]

    router.delete_smses(start_sms_index=start_index, num_smses=max_messages_per_page, delete_from_draft=True)

def remove_all_messages() -> None:
    can_remove = True

    page_index = 1
    max_messages_per_page = config_manager.program_config["num_messages_per_page"] 

    while(can_remove):
        print(f"\nRemoving page {page_index}...")

        can_remove = router.delete_sms_page(page_index=1, max_messages_per_page=max_messages_per_page, delete_from_draft=True)
        
        page_index += 1