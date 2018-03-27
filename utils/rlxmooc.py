import sys, urllib, re, datetime, ntplib, pytz, tzlocal, traceback, httplib2, gspread
import numpy as np
import pandas as pd
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials
import subprocess
import json

course = {'QUIZ': {'defs': {'QZ1': 'dynamic'}, 'weight': 0.5}, 'name': '2017BG', 'PROBLEM_SETS': {'defs': {'PS1': {'maxgrade': 5.0, 'problems': ['PS1_1', 'PS1_2'], 'deadlines': {'2018/10/18 00:00:00 [-0500]': {'penalty': 0.3, 'name': 'softdeadline'}, '2018/10/19 00:00:00 [-0500]': {'penalty': 1, 'name': 'harddeadline'}}}}, 'weight': 0.5}}
course_id   = course['name']

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

def google_drive_create_file(gc, fname, email):

    template = gc.create(fname)
    template.add_worksheet('submissions', 100, 100)
    template.add_worksheet('summary',100,100)
    template.get_worksheet(0).update_acell('A1', "SUBMISSION DATE")
    template.get_worksheet(0).update_acell('B1', "PROBLEM NUMBER")
    template.get_worksheet(0).update_acell('C1', "RESULT")
    template.get_worksheet(0).update_acell('D1', "REMARKS")
    template.get_worksheet(0).update_acell('E1', "CODE")
    template.share('pruebadaielchom@gmail.com', perm_type='user', role='writer')
    template.share(email, perm_type='user', role='reader')

def google_drive_create_file_grade_final(gc, sname):
    grade = gc.create(sname)
    grade.add_worksheet('grades', 1, 1)
    grade.share('pruebadaielchom@gmail.com', perm_type='user', role='writer')

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

    app_email, gc, service = get_RLXMOOC_credentials()
    config = gc.open("MOOCGRADER CONFIGS").worksheet("config")

    for pset in pdefs.keys():

        problems_ids = []
        deadslines = []
        penalty = ""
        dname = ""

        if pdefs[pset] == "dynamic":
            for i in submissions_df['problem_id'].get_values():
                if pset in i:
                    problems_ids.append(i)

            row = 0

            for j,i in enumerate(config.col_values(1)):
                if pset in i:

                    dname = i.split("::")[2]

                    row = j


            deadslines.append(config.col_values(2)[row])
            penalty = config.col_values(4)[row]


        else:
            problems_ids = pdefs[pset]["problems"]
            deadslines = pdefs[pset]["deadlines"]


        for pid in problems_ids:

            dfp = submissions_df[submissions_df.problem_id==pid]

            # Problem Submit
            if len(dfp)>0:
                dfpmax = dfp[dfp['result']==dfp['result'].max()]

                dfpgrade = dfpmax['result'].copy()

                for strdate in deadslines:
                    date = str2datetime(strdate)
                    if pdefs[pset] != "dynamic":
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
        pids = []

        if pdefs[pset] == "dynamic":
            pids = grades["problem_id"].get_values()

        else:
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

    grades = gc.open(course['name']+"-grades").worksheet("grades")
    grades.append_row(class_grades.columns)
    row = class_grades.iterrows()
    for i in row:
        grades.append_row(i[1].get_values())

def compute_all_grades():
    app_email, gc, service = get_RLXMOOC_credentials()
    sheet_names = get_course_sheets(service)

    class_grades = None
    for sheet_name in sheet_names:
        if sheet_name==course["name"]+"-grades":
            continue

        grades_summary = compute_grades(sheet_name, gc)

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
        'emailAddress': 'pruebadaielchom@gmail.com'
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

    if "QZ" in pid:
        row = 0
        app_email, gc, service = get_RLXMOOC_credentials()
        config = gc.open("MOOCGRADER CONFIGS").worksheet("config")
        cols = config.col_values(1)

        for j,i in enumerate(cols):
            if pid[:-2] in i:
                row = j

        maxgrade = config.col_values(5)[row]

    else:
        ids = [ i for i in course.keys() if i!='name']
        for i in ids:
            if(pid[:-2] in course[i]['defs'].keys()):
                maxgrade = course[i]['defs'][pid[:-2]]['maxgrade']

    if (result<0 or result>maxgrade):
        comentario = "NOTA FUERA DEL RANGO"
    return comentario

def add_deadline():
    """Agrega los deadlines del diccionario course al archivo MOOCGRADER CONFIGS"""

    deadlines ={}
    l = {}
    for i in course:
        if i!="name":
            for j in course[i]['defs']:
                if course[i]['defs'][j] != "dynamic":
                    deads = course[i]['defs'][j]['deadlines'].keys()
                    for k in deads:
                        l.update({k:course[i]['defs'][j]['deadlines'][k]['name']})
                    deadlines.update({j:l})
    line = []
    for i in deadlines:
        for j in deadlines[i]:
            line.append((course_id+"::"+i+"::"+deadlines[i][j],j))

    add_deadline_moocconfig(line)

def prepare_deadline_quiz(paramquiz, pid):

    line = []
    deads = []

    for i in paramquiz['deadlines']:
        deads.append(course['name']+"::"+pid+"::"+paramquiz['deadlines'][i]['name'],)
        deads.append(i,)
        deads.append(paramquiz['problems'],)
        deads.append(paramquiz['deadlines'][i]['penalty'],)
        deads.append(paramquiz['maxgrade'],)
        line.append(deads)

    add_deadline_moocconfig(line)

def add_deadline_moocconfig(line):
    """Agrega una lista con los deadlines y otros parametros a la hoja de calculo MOOCGRADER CONFIG """

    for i in line:
        hl = i[0]
        sl = i[1].replace(" ","_")

        app_email, gc, service = get_RLXMOOC_credentials()
        config = gc.open("MOOCGRADER CONFIGS").worksheet("config")

        if len(i) > 2:
            config.append_row([hl,sl.replace("_"," "),i[2],i[3],i[4]])
        else:
            config.append_row([hl,sl.replace("_"," ")])
        print " ... Deadline Added"

def generar_banco_py(pid):
    """Crea un achivo banco.py con todos los ejercicios de un quiz y la identificacion
    del quiz"""

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
    archivo_py.write("quices = "+ str(quices))
    archivo_py.write("\n")
    archivo_py.write("pid = \""+pid+"\"")
    archivo_py.close()

def read_banco():
    """Extrae la lista de ejercicios presente en el archivo banco.py"""
    import banco as bc
    return bc.quices, bc.pid

def read_quiz(banco, list_points):
    """Retorna aun lista de ejercicios del banco, a corde a list_points"""
    for i in list_points:
        yield banco[i]

def generate_seed(seed,len_banco, pid):
    """Genera una lista de numeros pseudoaleatoria"""

    app_email, gc, service = get_RLXMOOC_credentials()
    config = gc.open("MOOCGRADER CONFIGS").worksheet("config")
    cols = config.col_values(1)
    row = 0

    for j,i in enumerate(cols):
        if pid in i:
            row = j



    count_quiz = config.col_values(3)[row]

    list_points = []
    for i in range(int(count_quiz)):
        seed = int((997*(seed)+3)%len_banco)
        list_points.append(seed)
    return list_points

def email_to_seed(email, pid):
  seed = ""
  for i in email+pid:
    seed = seed + str(ord(i))
  return int(seed)

def render_quiz(email):
    """ Returna una lista con los ejercicios prpuestos para un estudiante
    en especifco teniendo en cuenta la lista generada aleatoriamente"""

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

    print "Conecting.."
    app_email, gc, service = get_RLXMOOC_credentials()
    template = gc.create("MOOCGRADER CONFIGS")

    print "Creating moocgrader"
    template.add_worksheet('config', 1, 6)
    template.get_worksheet(0).update_acell('A1', "DEADLINE")
    template.get_worksheet(0).update_acell('B1', "DATE")
    template.get_worksheet(0).update_acell('C1', "COUNT PROBLEMS")
    template.get_worksheet(0).update_acell('D1', "PENALTY")
    template.get_worksheet(0).update_acell('E1', "MAXGRADE")
    print "Creating worksheet config"
    template.share('pruebadaielchom@gmail.com', perm_type='user', role='writer')
    print "Sharing moocgrader"
    print "Adding Deadlines"
    add_deadline()
    print "OK"
    print "https://docs.google.com/spreadsheets/d/"+template.id

# GENERAR_BANCO_PY
# Crea el archivo banco.py con todos los ejercicios.
if sys.argv[1]=="GENERAR_BANCO_PY":
    generar_banco_py(sys.argv[2])

# RENDER_QUIZ
# se encarga de exraer los ejercicios de banco.py para el estudiante dependiendo de su correo electronico.
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
   final_deadline_expired = check_deadline_expired(gc, course_id, problemset_id, "finaldeadline")

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
       wks.update_cell(i+1,4, "HARD DEADLINE EXPIRED")
       print "SUBMITTED AFTER HARD DEADLINE"

   elif soft_deadline_expired:
       wks.update_cell(i+1,4, "DEADLINE EXPIRED")
       print "SUBMITTED AFTER DEADLINE"

   elif final_deadline_expired:
       wks.update_cell(i+1,4, "DEADLINE EXPIRED")
       print "SUBMITTED AFTER DEADLINE"

   print "your submissions sheet is https://docs.google.com/spreadsheets/d/"+gf.id
   print "----"
   print "evaluation result", result, ", submission registered"
