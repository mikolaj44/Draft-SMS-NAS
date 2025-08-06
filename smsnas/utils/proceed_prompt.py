def proceed_prompt(message: str = "", fullPrompt: bool = True) -> bool:
    if(fullPrompt):
        print(f"{message} Do you wish to proceed? [Y/N]: ", end="")
    else:
        print(f"{message} [Y/N]: ", end="")

    while True:
        result = input()

        if(result.lower() == "y"):
            break

        if(result.lower() == "n"):
            return False
        
        print("\nPlease provide a valid choice [Y/N]: ", end="")

    return True