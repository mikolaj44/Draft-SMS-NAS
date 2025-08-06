from importlib.resources import files
import json

user_config = None
user_config_file = None

program_config = None
program_config_file = None

def set_config() -> None:
    global user_config, user_config_file, program_config, program_config_file
    
    user_config_file = files("smsnas") / "user_config.json"
    program_config_file = files("smsnas") / "program_config.json"

    with user_config_file.open("r+", encoding="utf-8") as f:
        user_config = json.load(f)

    with program_config_file.open("r+", encoding="utf-8") as f:
        program_config = json.load(f)

def update_config() -> None:
    with user_config_file.open("r+", encoding="utf-8") as f:
        f.truncate(0)
        json.dump(user_config, f, indent=4)

    with program_config_file.open("r+", encoding="utf-8") as f:
        f.truncate(0)
        json.dump(program_config, f, indent=4)