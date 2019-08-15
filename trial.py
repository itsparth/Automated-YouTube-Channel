import os, requests, re, DriveUpload

directory = os.getcwd() + "\\Books\\downloads\\"

folderName = "THERMODYNAMICS"
booksString = '''P.K. NAG- https://drive.google.com/open?id=0B9bpsTYXP4ceaGttcWo1ek04d1E  N.D. HARI DASS- https://drive.google.com/open?id=0B6pGoYzCs7PgQUxRbFR1Y0x0akk  R.K. RAJPUT- https://drive.google.com/open?id=0B6pGoYzCs7PgUUpLSGlFY1JWNzA  CENGEL BOLES- https://drive.google.com/open?id=0B6v8d0nd8ubpMlY0LWJUM09Tc1E  SANFORD KLEIN- https://drive.google.com/open?id=0B9bpsTYXP4ceWTI2QTBwVkttM0U  MARK J. ASSAEL- https://drive.google.com/open?id=0B9bpsTYXP4ceVENpU0p4Mm1yZlE  BORGNAKKE 8e- https://drive.google.com/open?id=0B9bpsTYXP4ceOTJZMlloUU5ZY2M  ROBERT BALMER- https://drive.google.com/open?id=0B7JWdKw_4Q07X2M3TmtsckUxVmc  NO AUTHOR- https://drive.google.com/open?id=0B7JWdKw_4Q07N3M5TlRtV1N6R1k  MORAN, SHAPIRO- https://drive.google.com/open?id=0B7JWdKw_4Q07QjZfbGRYbzVzYzg  EASTOP- https://drive.google.com/open?id=0B4SQTWiEAAQeZFRyRVBkWEU1REU  Y V C RAO- https://drive.google.com/open?id=0B9bpsTYXP4ceRFlKcm5lbER2M3M  SCHAUMS- https://drive.google.com/open?id=0B6pGoYzCs7PgUTRMV1dTc1ZfSUU  CHIH WU- https://drive.google.com/open?id=0B5CXzYw2DbwIUHZlZmFUQ0l6ZDQ  NO AUTHOR- https://drive.google.com/open?id=0B9bpsTYXP4ceZE9FcC13d0NRa28  BILL POIRIER- https://drive.google.com/open?id=0B6pGoYzCs7PgMEtJV2FHd2ZKT1U  ONKAR SINGH- https://drive.google.com/open?id=0B9bpsTYXP4cebmNjUGJJSXdNNXM  MERLE C. POTTER- https://drive.google.com/open?id=0B6pGoYzCs7PgTmMzcUZtbmxfSGc  CENGEL- https://drive.google.com/open?id=0B7JWdKw_4Q07cGFMbXU4WkpiWDA  BORGNAKKE SONNTAG- https://drive.google.com/open?id=0B7JWdKw_4Q07bk9ab1k5VmlrYlE '''

pattern = r"https://drive.google.com/open\?id=(.+?)\s"

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb+") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    ids = re.findall(pattern, booksString)
    for id in ids:
        print("Downloading id %s" %id)
        filename = DriveUpload.get_file_name(id)
        dir = directory+folderName
        if not os.path.exists(dir):
            os.mkdir(dir)
        if not os.path.exists(dir+"/"+filename):
            print("Not Exists %s" %filename)
            try:
                download_file_from_google_drive(id, dir+"/"+filename)
            except:
                pass