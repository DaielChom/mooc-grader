import sys, urllib, re, datetime, ntplib, pytz, tzlocal, traceback, httplib2, gspread
import numpy as np
import pandas as pd
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials
import subprocess
import json

course_name = "##COURSE##"

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
    template = gc.open(fname)
    template.del_worksheet(template.worksheet('Sheet1'))
    template.share('##EMAIL##', perm_type='user', role='writer')
    template.share(email, perm_type='user', role='reader')

def google_drive_create_file_grade_final(gc, sname):
    grade = gc.create(sname)
    grade.add_worksheet('grades', 1, 1)
    grade.share('##EMAIL##', perm_type='user', role='writer')

def check_solution (pid):

   grader_fname = "utils/graders/grader_"+pid+".grader"
   with open(grader_fname, 'r') as myfile:
        grader_src = str(encryptDecrypt(myfile.read()))

   output_file = subprocess.check_output(grader_src, shell=True, executable=grader_src.split()[0][2:]).split("##")
   print output_file[0]
   return float(output_file[1])

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

def get_config(gc, course_name, problem_set_id, configvar, debug=False):
    try:
        row = 0
        name = problem_set_id
        index = 7 if configvar == "harddeadline" else 9

        if debug:
            print "looking for", name

        config = gc.open(course_name+" - MOOCGRADER CONFIGS").worksheet("config")
        pids = config.col_values(3)

        for j,i in enumerate(pids):
            if i == name[:-2]:
                row = j

        v = config.col_values(index)[row]
        return v

    except gspread.CellNotFound:
        if debug:
            print "not found"
        return None

def remove_from_list(list_to_remove, for_remove):
    for i in reversed(for_remove):
        list_to_remove.pop(int(i))
    return list_to_remove

def check_deadline_expired(gc, course_name, problemset_id, deadline_id="harddeadline"):

    now = get_localized_inet_time()
    deadline_str = get_config(gc, course_name, problemset_id, deadline_id)

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
    sheet_names = [f["name"] for f in files["files"] if f["name"].startswith(course_name)]
    return sheet_names

def get_coursepart_grades(sheet_name, for_remove, submissions_df):

    r = pd.DataFrame([], columns=submissions_df.columns)

    pids = remove_from_list(get_colums_moocgrader(3), for_remove)
    type_dynamic = remove_from_list(get_colums_moocgrader(6), for_remove)
    count_section = remove_from_list(get_colums_moocgrader(4), for_remove)
    len_banco = remove_from_list(get_colums_moocgrader(4), for_remove)

    for j, pset in enumerate(pids):

        problems_ids = []
        deadslines = []
        penalty = ""
        dnames = ["HARDDEADLINE", "SOFTDEADLINE"]

        if type_dynamic[j] == "dynamic":

            list_count = generate_seed( email_to_seed(sheet_name.split("-")[1], pset),int(len_banco[j].split("-")[1]), pset)
            problems_ids = [pset+"_"+str(i+1) for i in list_count]
            deadslines.append(remove_from_list(get_colums_moocgrader(7), for_remove)[j])
            penalty = remove_from_list(get_colums_moocgrader(8), for_remove)[j]

        elif type_dynamic[j] == "static":

            problems_ids = [pset+"_"+str(i+1) for i in range(int(count_section[j]))]
            deadslines.append(remove_from_list(get_colums_moocgrader(7), for_remove)[j])
            deadslines.append(remove_from_list(get_colums_moocgrader(9), for_remove)[j])

        for pid in problems_ids:

            dfp = submissions_df[submissions_df.problem_id==pid]

            # Problem Submit
            if len(dfp)>0:

                dfpmax = dfp[dfp['result']==dfp['result'].max()]
                dfpgrade = dfpmax['result'].copy()
                dname = dnames[1]

                for k,strdate in enumerate(deadslines):

                    date = str2datetime(strdate)

                    if type_dynamic[j] == "static":
                        penalty = remove_from_list(get_colums_moocgrader(8+k*2), for_remove)[j]

                    if dfpmax['date'][0] > date:

                        if k == 0:
                            dname = dnames[0]

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

def get_coursepart_summary(sheet_name, for_remove, grades):

    r = []
    pids = remove_from_list(get_colums_moocgrader(3), for_remove)
    type_dynamic = remove_from_list(get_colums_moocgrader(6), for_remove)
    count_section = remove_from_list(get_colums_moocgrader(4), for_remove)
    len_banco = remove_from_list(get_colums_moocgrader(4), for_remove)

    for j,pset in enumerate(pids):
        pids = []

        if type_dynamic[j] == "dynamic":
            list_count = generate_seed( email_to_seed(sheet_name.split("-")[1], pset),int(len_banco[j].split("-")[1]), pset)
            pids = [pset+"_"+str(i+1) for i in list_count]

        elif type_dynamic[j] == "static":
            pids = [pset+"_"+str(i+1) for i in range(int(count_section[j]))]

        psetgrades = []
        for pid in pids:
            pgrade = grades[grades.problem_id==pid].grade
            pgrade = pgrade.iloc[0] if len(pgrade)>0 else 0
            psetgrades.append(pgrade)
        r.append([pset, np.mean(np.array(psetgrades).astype(np.float))])
    r.append(["TOTAL", np.mean([i[1] for i in r])])
    return pd.DataFrame(r, columns=["problemset", "grade"]).sort_values(by=["problemset"])

def get_colums_moocgrader(colum):

    list_return = []
    app_email, gc, service = get_RLXMOOC_credentials()
    config = gc.open(course_name+" - MOOCGRADER CONFIGS").worksheet("config")
    list_col = config.col_values(colum)
    list_title = config.row_values(1)

    for i in list_col:
        if len(i) and i not in list_title:
            list_return.append(i)

    return list_return

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

    keys = get_colums_moocgrader(1)
    weight = get_colums_moocgrader(2)

    start_row = 5
    cols = ["sheet_name"]
    vals = [sheet_name]
    course_total = 0.0

    for j,k in enumerate(keys):

        pids = get_colums_moocgrader(3)
        for_remove = []
        idp = k.split("::")[1]

        for u,h in enumerate(pids):
            if idp not in h:
                for_remove.append(u)

        grades  = get_coursepart_grades(sheet_name, for_remove, submissions)
        summary = get_coursepart_summary(sheet_name, for_remove, grades)

        # save detail and summary in student sheet
        dataframe_to_gsheet(wks, grades, k.split("::")[0], start_row=start_row, start_col=1)
        dataframe_to_gsheet(wks, summary, k.split("::")[0]+" SUMMARY", start_row=start_row, start_col=8)
        start_row += len(grades)+4

        # remove total and recalculate it
        summary = summary[summary.problemset!="TOTAL"]

        cols += list(summary.problemset)+ [k.split("::")[0]+"_TOTAL"]
        vals += list(summary.grade)+[np.mean(summary.grade)]
       # cols += [k]
       # vals += [np.mean(summary.grade)]
        course_total += float(np.mean(summary.grade))*float(weight[j])
    cols += ["TOTAL"]
    vals += [course_total]
    grades_summary = pd.DataFrame([vals], columns=cols)
    grades_summary_for_student = grades_summary[[col for col in grades_summary.columns if "TOTAL" in col]]
    dataframe_to_gsheet(wks, grades_summary_for_student, "COURSE SUMMARY", start_row=1, start_col=1)

    return grades_summary

def save_class_grades(class_grades, gc=None):

    if gc is None:
        app_email, gc, service = get_RLXMOOC_credentials()

    sname=course_name+"-grades"

    if not google_drive_file_exists(service, sname):
         google_drive_create_file_grade_final(gc, sname)
         print "The grade sheet for",course_name,"was created, check your email"

    grades = gc.open(course['name']+"-grades").worksheet("grades")
    grades.append_row(class_grades.columns)
    row = class_grades.iterrows()
    for i in row:
        grades.append_row(i[1].get_values())

def compute_all_grades():

    app_email, gc, service = get_RLXMOOC_credentials()
    sheet_names = get_course_sheets(service)

    d = []
    d.append(sheet_names[0])
    sheet_names = d+sheet_names[6:]

    class_grades = None

    for sheet_name in sheet_names:
        if sheet_name==course_name+"-grades":
            continue

        grades_summary = compute_grades(sheet_name, gc)

        if class_grades is None:
            class_grades = pd.DataFrame([], columns = grades_summary.columns)
        class_grades.loc[len(class_grades)] = grades_summary.iloc[0]

    return class_grades

def fix_sharing():
    print "Course is", course_name
    app_email, gc, service = get_RLXMOOC_credentials()
    files = retrieve_all_files(service)
    sheets = [f for f in files["files"] if f["name"].startswith(course_name)]

    rlxmooc_permision = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': '##EMAIL##'
    }

    for s in sheets:
        if s["name"].startswith(course_name):
            # user mail is in sheet name
            usermail = s["name"][len(course_name)+1:]

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

    comentario = ""
    maxgrade = 0
    row = 0

    app_email, gc, service = get_RLXMOOC_credentials()
    config = gc.open(course_name+" - MOOCGRADER CONFIGS").worksheet("config")
    cols = config.col_values(1)

    for j,i in enumerate(cols):
        if pid[:-2] in i:
            row = j

    maxgrade = config.col_values(5)[row]

    if (result<0 or result>maxgrade):
        comentario = "NOTA FUERA DEL RANGO"
    return comentario

def generar_banco_py(pid):

    PATH = "./instrucciones_quices_dinamicos"

    json_notebook = json.load(open(PATH+'.ipynb'))

    quices = []
    quiz = []
    switch = False

    for i in json_notebook['cells']:

        if len(i['source']):

            if switch:
                if i['source'][0] != "###END###":
                    quiz.append(i)

            if i['source'][0] == "###INIT###":
                switch = True

            if i['source'][0] == "###END###":
                switch = False
                quices.append(quiz)
                quiz = []

    archivo_py = open("banco.py","w")
    archivo_py.write("quizzes = "+ str(quices))
    archivo_py.write("\n")
    archivo_py.write("pid = \""+pid+"\"")
    archivo_py.close()

def read_banco():
    import banco as bc
    return bc.quizzes, bc.pid

def read_quiz(banco, list_points):
    for i in list_points:
        yield banco[i]

def generate_seed(seed,len_banco, pid):

    count_quiz = 0
    cols = get_colums_moocgrader(3)

    for j,i in enumerate(cols):
        if pid in i:
            count_quiz = get_colums_moocgrader(4)[j].split("-")[0]

    list_points = []

    list_points = np.random.RandomState(seed=seed).permutation(len_banco)

    return list_points[:int(count_quiz)]

def email_to_seed(email, pid):
  seed = str(abs(hash(pid+email)))[:9]
  return int(seed)

def render_quiz(email):

    cells = []
    banco, pid = read_banco()
    seed = email_to_seed(email, pid)
    list_points = generate_seed(seed,len(banco), pid)
    quiz_for_student = read_quiz(banco,list_points)

    for i in quiz_for_student:

        for j in i:
            if j['cell_type']=="markdown":
                cells.append([j['source'][0],"markdown"])

            if j['cell_type']=="code":
                if len(j['source']) != 0:
                    code_lines = j['source']

                    z = ""
                    for k in code_lines:
                        z = z + k
                    cells.append([z,"code"])

    return cells

if len(sys.argv)<2:
    sys.exit(0)

if sys.argv[1]=="CREATE_MOOCGRADER":

    fname = course_name+" - MOOCGRADER CONFIGS"

    print "Conecting.."
    app_email, gc, service = get_RLXMOOC_credentials()

    if google_drive_file_exists(service, fname):
        template = gc.open(fname)
        print ".. The file "+ fname+" already exists .."
        print "https://docs.google.com/spreadsheets/d/"+template.id

    else:
        template = gc.create(fname)

        print "Creating "+fname+" ..."
        template.add_worksheet('config', 100, 10)
        template.get_worksheet(0).update_acell('A1', "BLOCK NAME")
        template.get_worksheet(0).update_acell('B1', "BLOCK WEIGHT")
        template.get_worksheet(0).update_acell('C1', "SECTION NAME")
        template.get_worksheet(0).update_acell('D1', "SECTION COUNT")
        template.get_worksheet(0).update_acell('E1', "SECTION MAXGRADE")
        template.get_worksheet(0).update_acell('F1', "SECTION TYPE")
        template.get_worksheet(0).update_acell('G1', "SECTION HARDDEADLINE")
        template.get_worksheet(0).update_acell('H1', "SECTION HARDDEADLINE PENALTY")
        template.get_worksheet(0).update_acell('I1', "SECTION SOFTDEADLINE")
        template.get_worksheet(0).update_acell('J1', "SECTION SOFTDEADLINE PENALTY")

        print "Creating worksheet config"+"..."
        template.share('##EMAIL##', perm_type='user', role='writer')
        template = gc.open(fname)
		template.del_worksheet(template.worksheet('Sheet1'))
        print "Sharing "+fname+"..."
        print "OK.. "+fname+" created"
        print "https://docs.google.com/spreadsheets/d/"+template.id

if sys.argv[1]=="GENERAR_BANCO_PY":
    generar_banco_py(sys.argv[2])

if sys.argv[1]=="RENDER_QUIZ":

    is_authorized, email = check_user_auth()

    if not is_authorized:
        print "user not authenticsated, please run the first cell of this notebook to authenticate"
        sys.exit(0)

    f = open("quiz_for_student.py","w")
    f.write("l = "+str(render_quiz(email)))

if sys.argv[1]=="CHECK_SOLUTION":

   pid = sys.argv[2]
   result = check_solution(pid)
   comentario = check_result(result,pid)
   print "evaluation result", result, comentario

if sys.argv[1]=="SUBMIT_SOLUTION":

   pid = sys.argv[2]

   grader_fname = subprocess.check_output("ls utils/student_function/ | grep "+pid, shell=True, executable="/bin/bash")

   with open("utils/student_function/"+grader_fname.split()[0], 'r') as myfile:
       grader_src = myfile.read()

   src = grader_src
   problemset_id = pid

   print "connecting ...",
   sys.stdout.flush()

   is_authorized, email = check_user_auth()

   if not is_authorized:
      print "user not authenticated, please run the first cell of this notebook to authenticate"
      sys.exit(0)

   print "registering submission for", email,"..."
   sys.stdout.flush()

   app_email, gc, service = get_RLXMOOC_credentials()

   fname = course_name+'-'+email

   if not google_drive_file_exists(service, fname):
      google_drive_create_file(gc, fname, email)
      print "your personal submissions sheet for",course_name,"was created, check your email"
      sys.stdout.flush()

   config = gc.open(course_name+" - MOOCGRADER CONFIGS").worksheet("config")
   row = 0

   for j, i in enumerate(config.col_values(3)):
       if i == problemset_id[:-2]:
           row = j

   soft_deadline_expired = False

   if config.col_values(6)[row] == "static":
       soft_deadline_expired = check_deadline_expired(gc, course_name, problemset_id, "softdeadline")

   hard_deadline_expired = check_deadline_expired(gc, course_name, problemset_id, "harddeadline")

   gf = gc.open(fname)

   wks = gf.worksheet("submissions")
   col1 = wks.col_values(1)
   for i in range(len(col1)):
       if col1[i]=='':
           break

   result = check_solution(pid)
   comentario = check_result(result,pid)
   datestr = datetime2str(get_localized_inet_time())
   wks.update_cell(i+1,1,datestr)
   wks.update_cell(i+1,2,pid)
   wks.update_cell(i+1,3,result)
   wks.update_cell(i+1,5,src)
   wks.update_cell(i+1,6,comentario)

   if hard_deadline_expired:
       wks.update_cell(i+1,4, "HARDDEADLINE EXPIRED")
       print "SUBMITTED AFTER HARDDEADLINE"

   elif soft_deadline_expired:
       wks.update_cell(i+1,4, "SOFTDEADLINE EXPIRED")
       print "SUBMITTED AFTER SOFTDEADLINE"

   print "your submissions sheet is https://docs.google.com/spreadsheets/d/"+gf.id
   print "----"
   print "evaluation result", result, ", submission registered"
