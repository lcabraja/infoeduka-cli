from datetime import datetime
import requests, json, typer
from credentials import get_credentials, has_credentials

def verify_credentials(username, password):
    try: 
        _, session_token = post_login(username, password)
        return session_token
    except:
        return False

def reauthenticate():
    credentials = get_credentials()
    has_cred = has_credentials()
    return
    datetime.fromtimestamp()
    if credentials["token"]["loggedin"]:
        return token

def authenticate(username, password):
    _, session_token = post_login(username, password)
    # TODO: Parse and handle login reponse data
    return session_token

def post_login(username, password):
    url = "https://student.racunarstvo.hr/digitalnareferada/api/login"
    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{username}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{password}\r\n-----011000010111000001101001--\r\n"
    headers = { "Content-Type": "multipart/form-data; boundary=---011000010111000001101001" }
    response = requests.request("POST", url, data=payload, headers=headers)
    response_data = json.loads(response.text)
    session_token = response.cookies.get("PHPSESSID")
    return response_data, session_token
