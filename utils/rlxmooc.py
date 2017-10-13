
import sys, urllib, re, datetime, ntplib, pytz, tzlocal, traceback, httplib2, gspread
import numpy as np
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials

template_id = "1Dy5ITWjvtvSO4brkINoOlwxPW3rE7UvCz_iwxpbSUec"
course_id   = "2017BG"

def encryptDecrypt(input):
        key = ['A', 'M', 'B', 'N','O','F','E','A','E','E'] #Can be any chars, and any size array
        output = []

        for i in range(len(input)):
                xor_num = ord(input[i]) ^ ord(key[i % len(key)])
                output.append(chr(xor_num))

        return ''.join(output)

def check_user_auth():

   storage = Storage('/tmp/creds')
   credentials = storage.get()
   if credentials is None:
      return False, None
   if credentials.access_token_expired:
       print "session expired, please run the first cell to authenticate with your google account again"
       return False, None
   http_auth = credentials.authorize(httplib2.Http())
   oauth_service = discovery.build(serviceName='oauth2', version='v2', http=http_auth)
   userinfo = oauth_service.userinfo().get().execute()
   return True, userinfo["email"]

def get_RLXMOOC_credentials():
   json_key = {'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/bg2017%40bg-182713.iam.gserviceaccount.com', 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC0OX6GreqdpnWg\nTeOK2DAlFe071qEkFHhyz9DCuL6aNuv6zLbpHZ5+cbGUZayip9jnM87I6wP7ZSPF\n4YpraDaUGtztC9Yl1HNrKk0ClqZJ/vQzPNYLwr5UAGpPcBLfpfYEHMwxbDAytdyo\nuv0wG3mtzQFO1kXdaFuTSAVsFA6HwFzMfnhDLaht+yHZsjP2zzecTsifK7tf9fjr\nqJHnvWrizy2A2PnFJzXAIRjOv60HT6uhwtyMmpfFfYnvPkfHsgj6NKsASY8n9fN8\nE+SN+M83bm1DUKJeZ7gSTPcMZOXwnHSlhpbne9lIum0tjFQBcvn8O3V/tF8qBKf6\nl3tiHTNHAgMBAAECggEAApRYFUFj/EGnqVW0DgauGbnInXSi9cs9Nhd3W3IdeEOU\n+Q/5BjkgTZr++arC38kbN6PsL7/9XJnD+08RFhx1u4Tu6I2k0QHLbRs74u+ZDbIS\neLFENwLgin8/BkgKXR0Y+lIXMhXkUrV7pQaYHRonka8/d4tlkJevx9neCf/3fUXj\naA9rxvNbGQK/Or0bHJIG35vM5Q2p3g4dUF0Rf3sbntas9K7J5J+q/IT/6FYTdiIY\nfp+ARfyKv99yo5hRmEm56Z+9JrD8GYGNELDBwY0kq3e6hzeUl9IVhx9yxSGcqkrh\nl4W/M806ayRo7zh51XLv5aUAKJGMBuOLWl0ePF6KkQKBgQDXzX4qV1WqCWku7M7E\nAeo61Q/w4fRryAY69DsJ2KNpuw88jB2N2PJMdDfyQYNla06Fkxuk8DZ4DX6epEab\nXPyFNb6025poOJzm8jDbkWjsUrHXkBB1W+9dAo5py0S73LP4CfnMhHcOybeDKu8U\nEhP5YZNTM/sz9+7WeGrjGo+NewKBgQDVy3dXpR7wpZFWaLP9awgStiP1hwZ6yrRq\n3jb8LGllmtd39EGKpnVtVtTWfoCQsfWDvvYepFswhtDtvMl/ff+xy6bgMTOTbHDo\n/jMm7Hy4smkScKDXedMksZfTgoW/HmcnWJeCdXW4YdsL9AmVpxwK0P76BWPa1oAx\nDlO7WnIZpQKBgQCfpzqQzp3ktyOnALETl6sXLWumtTPjzU62rNtEtI5o+WgTTkHL\nIFZZs510T32LObEU5zmLc9+IP8uOSFCoPknfr1xQZys7sa56uXDl8BTkyWUi6kUS\n3hofAHYl1KkcJvLKLW8uHE4MlbV7h/bqLVmzpLme05Uj5GhBKUNCkvLjIwKBgQCE\n4DyAQKQGNSErb0/OxWLzHjkjNJSWZL3VXd8WxBONjrs0Vp8VqXd6SWlnFqCZTcGl\n7F3TlZsHggMAf0FM9+affk9tL6c6jT9vz+3C12B8+oXLbCzLP3A3chlG3+x4aFD8\nZ1djQdW0jz0xJK+AT6hiIJsYkZkKPh7WXm00GHap8QKBgAfQ48Lre0t6c/mkgygC\npjfuCDIncVgaYbamC53tzAyYyx4nEuiqycmk6bx6vLcAhQ3bgF5oF6MuO/SDQqkH\nom8NWi58le8zmG09EVDmgw1C6sq7/MTgUkt/kYRER4yqJE2aSLrCgkQfD8WdUxmY\nAV7oOOsGd/AYwv4cqkNGa4HX\n-----END PRIVATE KEY-----\n', 'client_email': 'bg2017@bg-182713.iam.gserviceaccount.com', 'private_key_id': '467b8256caa9a634daaede7c98cf76029b525885', 'client_id': '105854021643136742430', 'token_uri': 'https://accounts.google.com/o/oauth2/token', 'project_id': 'bg-182713', 'type': 'service_account', 'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs'}
   scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
   credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
   gc = gspread.authorize(credentials)
   http = credentials.authorize(httplib2.Http())
   service = discovery.build("drive", "v3", http=http)
   return json_key['client_email'], gc, service

def google_drive_file_exists(service, fname):
    results = service.files().list(q='name="'+fname+'"').execute()
    items = results.get('files',[])
    return len(items)!=0

def google_drive_remove_files(service, fname):
    results = service.files().list(q='name="'+fname+'"').execute()
    items = results.get('files',[])
    for i in items:
        print "removing", i["name"], i["id"] 
        service.files().delete(fileId=i["id"]).execute()
        
def google_drive_create_file_from_template(service, fname, template_id, user_ro_access):
    origin_fileid=template_id
    copied_file = {'title': fname, 'name': fname}

    f = service.files().copy(fileId=origin_fileid, body=copied_file).execute()
    rlxmooc_permision = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': 'pruebadaielchom@gmail.com'
    }

    user_permision = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': user_ro_access
    }

    service.permissions().create(fileId = f["id"], body=rlxmooc_permision, fields="id").execute()
    service.permissions().create(fileId = f["id"], body=user_permision, fields="id").execute()


def check_solution (pid, src):

   # execute submitted code (must be a function)
   exec(src)

   # load grader code
   grader_fname = "utils/grader_"+pid+".epy"
   with open(grader_fname, 'r') as myfile:
        grader_src = encryptDecrypt(myfile.read())

   exec(grader_src)
   globals().update(locals())

   # call grader code
   try:
       r = "CORRECT" if eval("grade()") else "NOT CORRECT"
   except Exception as e:
       traceback.print_exc()
       r = "EXECUTION ERROR"

   return r
   
   
fmt_tz   = "%Y/%m/%d %H:%M:%S [%z]"
fmt_notz = "%Y/%m/%d %H:%M:%S"

def get_localized_inet_time():
    c = ntplib.NTPClient()
    response = c.request('0.europe.pool.ntp.org', version=3)
    nowloc = datetime.datetime.fromtimestamp(response.tx_time)

    lnowloc = tzlocal.get_localzone().localize(nowloc)    
    return lnowloc

def datetime2str(t):
    return t.strftime(fmt_tz)

def str2datetime(s):
    p = re.compile('(.*)\s\[([+|-])(\d\d)(\d\d)\]')
    m = p.match(s)
    mdate, msign, mtzhour, mtzmin = m.groups()
    offset = (-1*(msign=="-")+1*(msign=="+"))*int(mtzhour)*60+int(mtzmin)

    d1 = datetime.datetime.strptime(mdate, fmt_notz)
    d1 = pytz.FixedOffset(offset).localize(d1)
    return d1   


def get_config(gc, course_id, problem_set_id, configvar, debug=False):
    try:
        name = course_id+"::"+problem_set_id+"::"+configvar
        if debug:
            print "looking for", name
        w = gc.open("RLXMOOC CONFIGS").worksheet("config")
        c = w.find(name)
        v = w.cell(c.row, c.col+1).value
        return v

    except gspread.CellNotFound:
        if debug:
            print "not found"
        return None

def check_deadline_expired(gc, course_id, problemset_id, deadline_id="harddeadline"):
    now = get_localized_inet_time()
    deadline_str = get_config(gc, course_id, problemset_id, deadline_id)
    if deadline_str is None:
        return False
    deadline = str2datetime(deadline_str)
    diff = deadline-now
    return diff.total_seconds()<0

if len(sys.argv)<2:
    sys.exit(0)

if sys.argv[1]=="CHECK_SOLUTION":
   pid = sys.argv[2]
   src = urllib.unquote_plus(sys.argv[3])
   result = check_solution(pid, src)
   print "evaluation result", result


if sys.argv[1]=="SUBMIT_SOLUTION":
   pid = sys.argv[2]
   src = urllib.unquote_plus(sys.argv[3])
   problemset_id = pid.split("_")[0]

   print "connecting ...", 
   sys.stdout.flush()
       
   is_authorized, email = check_user_auth()

   if not is_authorized:
      print "user not authenticated, please run the first cell of this notebook to authenticate"
      sys.exit(0)
 
   print "registering submission for", email,"..."
   sys.stdout.flush()

   app_email, gc, service = get_RLXMOOC_credentials()

   fname = course_id+'-'+email

   if not google_drive_file_exists(service, fname):
      google_drive_create_file_from_template(service, fname, template_id, email)
      print "your personal submissions sheet for",course_id,"was created, check your email"
      sys.stdout.flush()
      
   hard_deadline_expired = check_deadline_expired(gc, course_id, problemset_id, "harddeadline")
   soft_deadline_expired = check_deadline_expired(gc, course_id, problemset_id, "softdeadline")

   gf = gc.open(fname)

   wks = gf.worksheet("submissions")
   col1 = wks.col_values(1)
   for i in range(len(col1)):
       if col1[i]=='':
           break

   result = check_solution(pid,src)
   datestr = datetime2str(get_localized_inet_time())
   wks.update_cell(i+1,1,datestr)
   wks.update_cell(i+1,2,pid)
   wks.update_cell(i+1,3,result)
   wks.update_cell(i+1,5,src)
   if hard_deadline_expired:
       wks.update_cell(i+1,4, "HARD DEADLINE EXPIRED")
       print "SUBMITTED AFTER HARD DEADLINE"
   elif soft_deadline_expired:
       wks.update_cell(i+1,4, "DEADLINE EXPIRED")
       print "SUBMITTED AFTER DEADLINE"
   print "your submissions sheet is https://docs.google.com/spreadsheets/d/"+gf.id
   print "----"
   print "evaluation result", result, ", submission registered"