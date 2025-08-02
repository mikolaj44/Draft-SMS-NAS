def proceed_prompt(message: str = "") -> bool:
    print(f"{message} Do you wish to proceed? [Y/N]: ", end="")

    while True:
        result = input()

        if(result.lower() == "y"):
            break

        if(result.lower() == "n"):
            return False
        
        print("\nPlease provide a valid choice [Y/N]: ", end="")

    return True