import click
import re
import json
import copy
from datetime import datetime
from os import makedirs, remove
from os.path import isdir
from pathlib import Path
from typing import Any

APP_NAME = "infoeduka-cli"
FILE_CREDENTIALS = "credentials.json"
FILE_MATERIALS = "materials.json"
DIRECTORY_MATERIALS = "materials"

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
    if not isdir(app_dir):
        makedirs(app_dir)
    config_path: Path = Path(app_dir) / filename
    return config_path


def read_file(path: Path):
    with path.open("r") as credential_file:
        return json.load(credential_file)


def try_read_file(path: Path):
    try:
        return read_file(path)
    except:
        return None


def write_file(path: Path, object: Any):
    with path.open('w') as file:
        json.dump(object, file, indent=4)


def get_blank_credentials():
    return copy.deepcopy(EMPTY_CREDENTIALS)


def get_credentials():
    config_path: Path = get_filename(FILE_CREDENTIALS)
    try:
        return read_file(config_path)
    except:
        return get_blank_credentials()


def set_credentials(username: str = None, password: str = None, token: str = None):
    save_credentials = get_credentials()
    config_path: Path = get_filename(FILE_CREDENTIALS)

    if username: save_credentials["username"] = username
    if password: save_credentials["password"] = password
    if token: save_credentials["token"] = {"phpsessid": token, "loggedin": datetime.now().isoformat()}

    write_file(config_path, save_credentials)


def reset_credentials(username: str = False, password: str = False, token: str = False):
    save_credentials = get_credentials()
    config_path: Path = get_filename(FILE_CREDENTIALS)

    if username and password and token: return delete_credentials()
    if username: save_credentials["username"] = None
    if password: save_credentials["password"] = None
    if token: save_credentials["token"] = None

    write_file(config_path, save_credentials)


def delete_credentials():
    config_path = get_filename(FILE_CREDENTIALS)
    remove(config_path)


def get_username():
    save_credentials = get_credentials()
    return False if not save_credentials else save_credentials["username"]


def validate_string(string: str):
    return True if string and len(string) > 0 else False


def validate_token_format(token: str):
    try:
        return re.search("(phpsessid=|PHPSESSID=)?([\d\w]{26})", token)[2]
    except:
        return False


def did_token_timeout(token):
    loggedin = datetime.fromisoformat(token["loggedin"])
    diff = (datetime.now() - loggedin).total_seconds()
    return False if diff < 1800 else True


def has_credentials():
    credentials = get_credentials()
    if credentials == get_blank_credentials(): return False
    if not did_token_timeout(credentials["token"]): return True
    if credentials["username"] and credentials["password"]: return True
    return False


def get_login_method(token, username, password):
    if validate_token_format(token): return "token", token
    if validate_string(username) and validate_string(password): return "username_password", None
    if has_credentials(): return "stored_credentials", None
    return False, None
