import json
from requests import request

def get_schedule(session_token):
    url = "https://student.racunarstvo.hr/digitalnareferada/api/student/raspored/tjedni"
    headers = {"Cookie": f"PHPSESSID={session_token}", "Accept": "application/json;charset=utf-8"}
    response = request("GET", url, headers=headers)
    response.encoding = 'utf-8'
    response_data =  json.loads(response.text)
    return response_data

def parse_schedule(schedule_response_data):
    pass

def get_todays_schedule(schedule_data):
    pass

def schedule_main(session_token):
    schedule_respnose_data = parse_schedule(get_schedule(session_token))
    today = get_todays_schedule(schedule_respnose_data)
    return today
