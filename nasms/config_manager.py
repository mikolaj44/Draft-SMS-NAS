from importlib.resources import files
import json

config = None
file = None

def getConfig() -> None:
    global config, file
    
    file = files("nasms") / "config.json"

    with file.open("r+", encoding="utf-8") as f:
        config = json.load(f)

def updateConfig() -> None:
    global config, file

    with file.open("r+", encoding="utf-8") as f:
        f.truncate(0)
        json.dump(config, f)