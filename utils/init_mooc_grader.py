import sys, urllib, re, datetime, ntplib, pytz, tzlocal, traceback, httplib2, gspread
import numpy as np
import pandas as pd
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials

course = ##COURSE##
course_id   = course['name']

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

def google_drive_create_file_grade_final(gc, sname):
    grade = gc.create(sname)
    grade.add_worksheet('grades', 100, 100)
    grade.share('##EMAIL##', perm_type='user', role='writer')

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
       r = eval("grade()")
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

def retrieve_all_files(service):
    try:
        param = {}
        files = service.files().list(**param).execute()
        return files
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

def clear_worksheet_range(wks, cell_range):
    cell_list = wks.range(cell_range)
    for cell in cell_list:
        cell.value=""
    wks.update_cells(cell_list)

def get_course_sheets(service=None):
    if service is None:
        app_email, gc, service = get_RLXMOOC_credentials()
    files = retrieve_all_files(service)
    sheet_names = [f["name"] for f in files["files"] if f["name"].startswith(course["name"])]
    return sheet_names

def get_coursepart_grades(pdefs, submissions_df):
    r = pd.DataFrame([], columns=submissions_df.columns)


    for pset in pdefs.keys():
        for pid in pdefs[pset]["problems"]:

            dfp = submissions_df[submissions_df.problem_id==pid]

            # Problem Submit
            if len(dfp)>0:
                dfpmax = dfp[dfp['result']==dfp['result'].max()]

                if len(dfpmax)>1:
                    dfpmax = dfpmax.drop(labels=[1], axis=0)

                dfpgrade = dfpmax['result'].copy()

                for strdate in pdefs[pset]["deadlines"]:
                    date = str2datetime(strdate)
                    penalty =  pdefs[pset]["deadlines"][strdate]["penalty"]
                    dname   =  pdefs[pset]["deadlines"][strdate]["name"]

                    if dfpmax['date'][0] > date:
                        grade_penalty = float(dfpgrade.get_value(dfpgrade.index[0]))-float(dfpgrade.get_value(dfpgrade.index[0]))*float(penalty)
                        dfpgrade.set_value(0,grade_penalty,2)
                        dfpmax.set_value(dfpgrade.index[0],'comment',dname)


                dfpmax['grade'] = dfpgrade

            # Problem not submit
            else:
                dfpmax = pd.DataFrame([["NOT SUBMITTED", pid, "NOT SUBMITTED", 0, "NOT SUBMITTED"]], columns=submissions_df.columns)

            if r.empty:
                r = dfpmax
            else:
                r = r.append(dfpmax)


    return r

def get_submissions(sheet_name, gc):
    if gc is None:
        app_email, gc, service = get_RLXMOOC_credentials()

    gf         = gc.open(sheet_name)
    wks        = gf.worksheet("submissions")
    dates      = wks.col_values(1)
    ids        = wks.col_values(2)
    result     = wks.col_values(3)

    dates = [i for i in dates if i!='' and i!="SUBMISSION DATE"]
    ids = [i for i in ids if i!='' and i!="PROBLEM NUMBER"]
    result = [i for i in result if i!='' and i!="RESULT"]

    df = pd.DataFrame([[dates[i], ids[i], result[i]] for i in range(len(dates))], columns=["date", "problem_id", "result"])
    df.date = [str2datetime(i) for i in df.date]
    df = df.dropna()
    df = df[ (df.problem_id!="") & (df.result!="")]
    df["grade"] = np.zeros(len(df))
    df["comment"] = [""] * len(df)
    return df

def get_coursepart_summary(pdefs, grades):
    r = []
    for pset in pdefs.keys():
        pids = pdefs[pset]["problems"]
        psetgrades = []
        for pid in pids:
            pgrade = grades[grades.problem_id==pid].grade
            pgrade = pgrade.iloc[0] if len(pgrade)>0 else 0
            psetgrades.append(pgrade)
        r.append([pset, np.mean(np.array(psetgrades).astype(np.float))])
    r.append(["TOTAL", np.mean([i[1] for i in r])])
    return pd.DataFrame(r, columns=["problemset", "grade"]).sort_values(by=["problemset"])

def find_cell(cell_list, row, col):
    for cell in cell_list:
        if cell.row == row and cell.col==col:
            return cell
    return None

def dataframe_to_gsheet(wks, df, title, start_row, start_col):
    nrows     = len(df)+2
    ncols     = len(df.columns)

    start_col_letter = chr(64+start_col)
    end_col_letter   = chr(64+start_col+ncols)
    end_row          = start_row+nrows

    cell_range = start_col_letter+str(start_row)+":"+end_col_letter+str(end_row)
    cell_list = wks.range(cell_range)

    find_cell(cell_list,start_row,start_col).value=title
    for i,col in enumerate(df.columns):
        find_cell(cell_list,start_row+1,start_col+i).value=col

    for i,(idx, item) in enumerate(df.iterrows()):
        for j, col in enumerate(df.columns):
            find_cell(cell_list, start_row+i+2,start_col+j).value=item[col]

    wks.update_cells(cell_list)

def compute_grades(sheet_name, gc=None):
    if gc is None:
        app_email, gc, service = get_RLXMOOC_credentials()

    print "Processing", sheet_name,

    submissions = get_submissions(sheet_name, gc)
    gf = gc.open(sheet_name)
    wks = gf.worksheet("summary")
    clear_worksheet_range(wks, "A1:Z100")

    start_row = 5
    cols = ["sheet_name"]
    vals = [sheet_name]
    course_total = 0.0
    for k in sorted(course.keys()):
        if k=="name":
            continue
        course_part = course[k]
        grades  = get_coursepart_grades(course_part["defs"], submissions)
        summary = get_coursepart_summary(course_part["defs"], grades)

        # save detail and summary in student sheet
        dataframe_to_gsheet(wks, grades, k, start_row=start_row, start_col=1)
        dataframe_to_gsheet(wks, summary, k+" SUMMARY", start_row=start_row, start_col=8)
        start_row += len(grades)+4

        # remove total and recalculate it
        summary = summary[summary.problemset!="TOTAL"]

        cols += list(summary.problemset)+ [k+"_TOTAL"]
        vals += list(summary.grade)+[np.mean(summary.grade)]
       # cols += [k]
       # vals += [np.mean(summary.grade)]
        course_total += np.mean(summary.grade)*course[k]["weight"]
    cols += ["TOTAL"]
    vals += [course_total]
    grades_summary = pd.DataFrame([vals], columns=cols)
    grades_summary_for_student = grades_summary[[col for col in grades_summary.columns if "TOTAL" in col]]
    dataframe_to_gsheet(wks, grades_summary_for_student, "COURSE SUMMARY", start_row=1, start_col=1)

    return grades_summary

def save_class_grades(class_grades, gc=None):
    if gc is None:
        app_email, gc, service = get_RLXMOOC_credentials()

    sname=course["name"]+"-grades"

    if not google_drive_file_exists(service, sname):
         google_drive_create_file_grade_final(gc, sname)
         print "The grade sheet for",course_id,"was created, check your email"
         sys.stdout.flush()

def compute_all_grades(course):
    app_email, gc, service = get_RLXMOOC_credentials()
    sheet_names = get_course_sheets(course, service)

    class_grades = None
    for sheet_name in sheet_names:
        if sheet_name==course["name"]+"-grades":
            continue

        grades_summary = compute_grades(course, sheet_name, gc)

        if class_grades is None:
            class_grades = pd.DataFrame([], columns = grades_summary.columns)
        class_grades.loc[len(class_grades)] = grades_summary.iloc[0]

    return class_grades

def fix_sharing():
    print "Course is", course_id
    app_email, gc, service = get_RLXMOOC_credentials()
    files = retrieve_all_files(service)
    sheets = [f for f in files["files"] if f["name"].startswith(course_id)]

    rlxmooc_permision = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': '##EMAIL##'
    }

    for s in sheets:
        if s["name"].startswith(course_id):
            # user mail is in sheet name
            usermail = s["name"][len(course_id)+1:]

            user_permision = {
                'type': 'user',
                'role': 'reader',
                'emailAddress': usermail
            }

            # sets permissions
            service.permissions().create(fileId = s["id"], body=rlxmooc_permision, fields="id").execute()
            service.permissions().create(fileId = s["id"], body=user_permision, fields="id").execute()
            print "permissions set", usermail

def check_result(result,pid):
    ## VERFICIAR CUANDO SEA MAYOR A LA NOTA MAXIMA
    comentario = ""
    maxgrade = 0

    ids = [ i for i in course.keys() if i!='name']
    for i in ids:
        if(pid[:-2] in course[i]['defs'].keys()):
            maxgrade = course[i]['defs'][pid[:-2]]['maxgrade']

    if (result<0 or result>maxgrade):
        comentario = "NOTA FUERA DEL RANGO"
    return comentario

def add_deadline():
    deadlines ={}
    l = {}
    for i in course:
        if i!="name":
            for j in course[i]['defs']:
                deads = course[i]['defs'][j]['deadlines'].keys()
                for k in deads:
                    l.update({k:course[i]['defs'][j]['deadlines'][k]['name']})
                deadlines.update({j:l})
    line = []
    for i in deadlines:
        for j in deadlines[i]:
            line.append((course_id+"::"+i+"::"+deadlines[i][j],j))

    for i in line:
        hl = i[0]
        sl = i[1].replace(" ","_")

        app_email, gc, service = get_RLXMOOC_credentials()
        config = gc.open("MOOCGRADER CONFIGS").worksheet("config")
        config. append_row([hl,sl.replace("_"," ")])
        print "OK deadline"

if len(sys.argv)<2:
    sys.exit(0)

if sys.argv[1]=="CREATE_MOOCGRADER":

    print "Conecting.."
    app_email, gc, service = get_RLXMOOC_credentials()
    template = gc.create("MOOCGRADER CONFIGS")

    print "Creating moocgrader"
    template.add_worksheet('config', 1, 1)
    print "Creating worksheet config"
    template.share('pruebadaielchom@gmail.com', perm_type='user', role='writer')
    print "Sharing moocgrader"
    print "Adding Deadlines"
    add_deadline()
    print "OK"
    print "https://docs.google.com/spreadsheets/d/"+template.id

if sys.argv[1]=="CHECK_SOLUTION":
   pid = sys.argv[2]
   src = urllib.unquote_plus(sys.argv[3])
   result = check_solution(pid, src)
   comentario = check_result(result,pid)
   print "evaluation result", result, comentario


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
   comentario = check_result(result,pid)
   datestr = datetime2str(get_localized_inet_time())
   wks.update_cell(i+1,1,datestr)
   wks.update_cell(i+1,2,pid)
   wks.update_cell(i+1,3,result)
   wks.update_cell(i+1,5,src)
   wks.update_cell(i+1,6,comentario)
   if hard_deadline_expired:
       wks.update_cell(i+1,4, "HARD DEADLINE EXPIRED")
       print "SUBMITTED AFTER HARD DEADLINE"
   elif soft_deadline_expired:
       wks.update_cell(i+1,4, "DEADLINE EXPIRED")
       print "SUBMITTED AFTER DEADLINE"
   print "your submissions sheet is https://docs.google.com/spreadsheets/d/"+gf.id
   print "----"
   print "evaluation result", result, ", submission registered"
