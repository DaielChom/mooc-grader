
import sys, urllib, re, datetime, ntplib, pytz, tzlocal, traceback, httplib2, gspread
import numpy as np
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials

course_id   = "##COUSERNAME##"

def encryptDecrypt(input):
        key = ##KEYPY## #Can be any chars, and any size array
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
   json_key = ##JSONKEY##
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

def google_drive_create_file(gc, fname, email):

    template = gc.create(fname)
    template.add_worksheet('submissions', 100, 100)
    template.add_worksheet('summary',100,100)
    template.get_worksheet(0).update_acell('A1', "SUBMISSION DATE")
    template.get_worksheet(0).update_acell('B1', "PROBLEM NUMBER")
    template.get_worksheet(0).update_acell('C1', "RESULT")
    template.get_worksheet(0).update_acell('D1', "REMARKS")
    template.get_worksheet(0).update_acell('E1', "CODE")
    template.share('##EMAIL##', perm_type='user', role='writer')
    template.share(email, perm_type='user', role='reader')


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
        w = gc.open("MOOCGRADER CONFIGS").worksheet("config")
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
      google_drive_create_file(gc, fname, email)
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
