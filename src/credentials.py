from textwrap import indent
from wsgiref import validate
import click
import re, json, copy
from pathlib import Path
from os import makedirs
from os.path import isdir
from datetime import datetime

APP_NAME = "infoeduka-cli"
FILE_CREDENTIALS = "credentials.json"
FILE_MATERIALS = "materials.json" 

EMPTY_CREDENTIALS = {
    "username": None,
    "password": None,
    "token": {
        "phpsessid": None,
        "loggedin": None
    }
}

def get_filename(filename: str):
    app_dir = click.get_app_dir(APP_NAME)
    if not isdir(app_dir): makedirs(app_dir)
    config_path: Path = Path(app_dir) / filename
    return config_path

def get_credentials():
    config_path: Path = get_filename(FILE_CREDENTIALS)
    if not config_path.is_file():
        return False
    try:
        with config_path.open("r") as credential_file:
            return json.load(credential_file)
    except:
        return None

def set_credentials(username: str = None, password: str = None, token: str = None):
    save_credentials = get_credentials()
    config_path: Path = get_filename(FILE_CREDENTIALS)
    if not save_credentials:
        save_credentials = copy.deepcopy(EMPTY_CREDENTIALS)

    if username: save_credentials["username"] = username
    if password: save_credentials["password"] = password
    if token: save_credentials["token"] = token

    with config_path.open('w') as credential_file:
        json.dump(save_credentials, credential_file, indent=4)


def validate_string(string: str):
    return True if string and len(string) > 0 else False

def validate_token(token: str):
    # if not validate_string(token): return False
    try:
        return re.search("(phpsessid=|PHPSESSID=)?([\d\w]{26})", token)[2]
    except:
        return False
    # return found_token if len(found_token) == 26 else False


def can_continue(token, username, password):
    if validate_token(token): return "token"
    if validate_string(username) and validate_string(password): return "username+password"
    if get_credentials(): return "stored_credentials"
    return False