import requests, json, os
from dotenv import load_dotenv

##            _               
##           | |              
##   ___  ___| |_ _   _ _ __  
##  / __|/ _ \ __| | | | '_ \ 
##  \__ \  __/ |_| |_| | |_) |
##  |___/\___|\__|\__,_| .__/ 
##                     | |    
##                     |_|    


load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
savefile = os.environ.get("SAVEFILE")
if savefile is None: savefile = ".infoeduka.json"
if not os.path.exists(savefile): 
    open(savefile, 'x').close()
    data = {}
else:
    fp = open(savefile, 'r')
    data_string = "".join(fp.readlines())
    try:
        data = json.loads("data_string")
    except:
        data = {}

base_url="https://student.racunarstvo.hr"

##    __                  _   _                 
##   / _|                | | (_)                
##  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ 
##  |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
##  | | | |_| | | | | (__| |_| | (_) | | | \__ \
##  |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
##  

def login(login_username, login_password):
    url = "https://student.racunarstvo.hr/digitalnareferada/api/login"
    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{login_username}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{login_password}\r\n-----011000010111000001101001--\r\n"
    headers = { "Content-Type": "multipart/form-data; boundary=---011000010111000001101001" }
    response = requests.request("POST", url, data=payload, headers=headers)
    response_data = json.loads(response.text)
    session_token = response.cookies.get("PHPSESSID")
    return response_data, session_token

def materials(session_token):
    url = "https://student.racunarstvo.hr/digitalnareferada/api/student/predmeti"
    querystring = {"dodatno":"materijali"}
    headers = {"Cookie": f"PHPSESSID={session_token}", "Accept": "application/json;charset=utf-8"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.encoding = 'utf-8'
    response_data =  json.loads(response.text)
    return response_data

##                 _       _          _             _   
##                (_)     | |        | |           | |  
##   ___  ___ _ __ _ _ __ | |_    ___| |_ __ _ _ __| |_ 
##  / __|/ __| '__| | '_ \| __|  / __| __/ _` | '__| __|
##  \__ \ (__| |  | | |_) | |_   \__ \ || (_| | |  | |_ 
##  |___/\___|_|  |_| .__/ \__|  |___/\__\__,_|_|   \__|
##                  | |                                 
##                  |_|                                 

login_response_data, session_id = login(username, password)
materials_response_data = materials(session_id)

for semester in materials_response_data["data"]:
    for year in semester["godine"]:
        for subject in year["predmeti"]:
            data[subject["idPredmet"]] = {
                # semester
                "academicYear": semester["akademskaGodina"],
			    "semester": semester["semestar"],

                # year
                "track": year["studij"],
                "subtrack": year["smjer"],
                "year": year["godina"],
                "enrollment": year["nacin"],
                "group": year["grupa"],

                # subject
                "name": subject["predmet"],
                "code": subject["sifra"],
                "ects": subject["ects"],
                "signature": subject["potpis"],
                "signature_date": subject["potpisDatum"],
                "grade": subject["ocjena"],
                "grade_desc": subject["ocjenaOpisno"],
                "grade_date": subject["ocjenaDatum"],
                "passed_nograde": subject["polozenBezOcjene"],
                "passed_nograde_kolok": subject["polozenBezOcjeneKolokviran"],
                "accepted": subject["priznat"],
                "accepted_cert": subject["priznatCertifikat"],

                "materials": {
                    "count": subject["dodatno"]["materijali"]["brojMaterijala"],
                    "last_changed_dotw": subject["dodatno"]["materijali"]["zadnjaIzmjenaDanUTjednu"],
                    "last_changed_date": subject["dodatno"]["materijali"]["zadnjaIzmjenaDatum"],
                    "last_changed_user": subject["dodatno"]["materijali"]["zadnjaIzmjenaKorisnik"],
                    "files": {}
                }
            }

            for category in subject["dodatno"]["materijali"]["kategorije"]:
                for material in category["materijali"]:
                    data[subject["idPredmet"]]["materials"]["files"][category["kategorija"]] = {
                        "id": material["id"],
                        "filename": material["naziv"],
                        "description": material["opis"],
                        "bytes": material["velicina"],
                        "date_uploaded": material["vrijeme"],
                        "user_uploaded": material["korisnika"],
                        "content_type": material["contentType"],
                        "url": material["link"]
                    }

os.system("clear")
print(json.dumps(data, indent=4, ensure_ascii=False))

##        _                              
##       | |                             
##    ___| | ___  __ _ _ __  _   _ _ __  
##   / __| |/ _ \/ _` | '_ \| | | | '_ \ 
##  | (__| |  __/ (_| | | | | |_| | |_) |
##   \___|_|\___|\__,_|_| |_|\__,_| .__/ 
##                                | |    
##                                |_|    

# fp = open(savefile, 'w')
# fp.write(json.dumps(data))