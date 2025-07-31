from tplinkrouterc6udraftsms import (
    TplinkRouterProvider,
    TplinkRouter,
    TplinkC1200Router,
    TplinkC5400XRouter,
    TPLinkMRClient,
    TPLinkVRClient,
    TPLinkEXClient,
    TPLinkXDRClient,
    TPLinkDecoClient,
    TplinkC80Router,
    TplinkWDRRouter,
    Connection,
    SMS
)

from tplinkrouterc6udraftsms.common.exception import *

from ...utils.colors import *

from ...managers import config_manager

router = None

PHONE_NUMBER = "12345678"

def authorize(url : str, password : str) -> bool:
    global router

    print("\nLogging in, please wait...\n")

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

def send_data(data: str) -> None:
    pass

def send_data(messages: list[str]) -> None:
    router.send_sms(phone_number=PHONE_NUMBER, messages=messages, draft=True)

def get_first_page_messages() -> list[str]:
    data = router.get_sms(getFromDraft=True,pageIndex=1)

    messages = []

    for message in data:
        messages.append(message.content)

    return messages

# def get_messages(startIndex: int = 1, numMessages: int = 1) -> list[str]:
#     data = router.get_sms(getFromDraft=True,pageIndex=1)

#     messages = []

#     for message in data:
#         messages.append(message.content)

#     return messages

# def remove_messages(startIndex: int = 1, numMessages: int = 1) -> None:
#     pass