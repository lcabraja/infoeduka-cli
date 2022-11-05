from datetime import datetime
import requests, json
from credentials import did_token_timeout, get_credentials, has_credentials, set_credentials

def verify_credentials(username, password):
    try: 
        _, session_token = post_login(username, password)
        return session_token
    except:
        return False

def reauthenticate(credentials = get_credentials()):
    if not did_token_timeout(credentials["token"]): return credentials["token"]["phpsessid"]
    return authenticate(credentials["username"], credentials["password"], True)


def authenticate(username, password, storeToken = False):
    _, session_token = post_login(username, password)
    if storeToken: set_credentials(token=session_token)
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

def get_materials(session_token):
    url = "https://student.racunarstvo.hr/digitalnareferada/api/student/predmeti"
    querystring = {"dodatno":"materijali"}
    headers = {"Cookie": f"PHPSESSID={session_token}", "Accept": "application/json;charset=utf-8"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.encoding = 'utf-8'
    response_data =  json.loads(response.text)
    return response_data