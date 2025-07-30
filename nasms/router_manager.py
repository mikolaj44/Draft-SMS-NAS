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
from logging import Logger

from tplinkrouterc6udraftsms.common.exception import *

from .utils.colors import *

router = None

def authorize(url : str, password : str) -> bool:
    global router

    print("\nLogging in, please wait...\n")

    try:
        router = TplinkRouterProvider.get_client(f"http://{url}", password)

        router.authorize()
    except Exception as e:
        print(RED + "\nCould not log in, reason from the tplinkrouterc6u library: " + PURPLE + str(e) + RESET)
        return False
    return True

def logOut() -> None:    
    router.logout()