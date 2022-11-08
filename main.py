import json
import mysql.connector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.browser import CreateDriver
from allocated import get_allocate
import os
from Resource import PathResource as path
import pandas as pd

mydb = mysql.connector.connect(
    host="reporting.iide.in",
    user="developer",
    database="bookmark_reporting",
    password="3.KkWZHu#4{..dgTF*kMC+cJ:qs2%@e?",
    port=3306
)

buff = 100
count = 1
driver = CreateDriver()
driver.get('https://learn.iide.co/wp-admin/admin.php?page=learndash-lms-reports')
try:
    driver.find_element(By.CLASS_NAME, 'learndash-data-reports-button').click()
except:
    WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.ID, 'user_login'))).send_keys('sudanprabjyot@gmail.com')
    driver.find_element(By.ID,'user_pass').send_keys('($b@v1P^838yr1VdXhnantMo')
    driver.find_element(By.ID,'wp-submit').click()
    WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.ID, 'learndash-data-reports-button'))).click()

sheetname = 'learndash_reports_user_courses_53f65102cb.csv'

prev_files = os.listdir(path.resource_path(os.environ.get('DOWNLOADPATH')))

while True:
    data = WebDriverWait(driver, 99999999).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'progress-label'))).get_attribute('innerText')
    p = int(data.split('of')[0].strip())
    t = int(data.split('of')[1].split(' ')[1].strip())
    print(p, t)
    if p == t:
        break

while True:
    cur_files = os.listdir(path.resource_path(os.environ.get('DOWNLOADPATH')))
    sub = [item for item in cur_files if item not in prev_files]
    if len(sub) > 0:
        sub = sub[0]
    if sub and '.csv' in sub and '.crdownload' not in sub:
        print(sub)
        sheetname = sub
        break

print('done Downloaed')

# gc = pygsheets.authorize(service_file=path.resource_path('windy-forge-364809-19af218316ad.json'))
# sh = gc.open('learn_iide')
# wks = sh.sheet1
# read = wks.get_all_values()

mong = json.loads(pd.read_csv(path.resource_path(os.environ.get('DOWNLOADPATH') + f'{sheetname}')).to_json())

tup = []
cols = list(mong.keys())
mc = mydb.cursor()
mc.execute('truncate table learndash')
driver.quit()


allocate_obj = get_allocate('windy-forge-364809-19af218316ad.json', 'Overall course Completion')

for j in range(1, len(mong[cols[0]])):
    obj = {}
    for c in cols:
        obj[c] = mong[c][str(j)]

    # completion status
    if obj['steps_completed'] == obj['steps_total']:
        obj['completion_status'] = 'Completed'
    elif int(obj['steps_completed']) == 0:
        obj['completion_status'] = 'Not Started'
    elif obj['steps_completed'] < obj['steps_total']:
        obj['completion_status'] = 'Incomplete'
    else:
        obj['completion_status'] = ""
    # module completed
    if obj['course_completed'] == 'NO':
        obj['module_completed'] = 0
    else:
        obj['module_completed'] = 1

    # steps_taken
    if obj['steps_completed'] == 0:
        obj['steps_taken'] = 0
    else:
        obj['steps_taken'] = 1

    # completed_yes
    if obj['course_completed'] == 'YES':
        obj['completed_yes'] = 1
    else:
        obj['completed_yes'] = ''

    # course_started
    if obj['steps_completed'] == 0:
        obj['course_started'] = 0
    else:
        obj['course_started'] = 1

    # batch_type
    if obj['Group(s)'] is not None:
        if 'certificationcourse' in obj['Group(s)'].lower().replace(' ',''):
            obj['batch_type'] = 'Certification Course'
        elif 'IIDE' in obj['Group(s)']:
            obj['batch_type'] = '4 Month Course'
        elif 'PGPDM' in obj['Group(s)']:
            obj['batch_type'] = 'Post Graduation Course'
        else:
            obj['batch_type'] = 'Null Batch'
    else:
        obj['batch_type'] = ' '

    # course_completion_status
    if obj['steps_completed'] == obj['steps_total']:
        obj['completion_status'] = 'Completed'
    elif int(obj['steps_completed']) == 0:
        obj['completion_status'] = 'Not Started'
    elif obj['steps_completed'] < obj['steps_total']:
        obj['completion_status'] = 'WIP'
    else:
        obj['completion_status'] = ''

        # time_m
    if obj['completion_time'] is not None:
        time_in_sheet = obj['completion_time'].split(':')
        hour = time_in_sheet[0]
        min = time_in_sheet[1]
        sec = time_in_sheet[2]
        obj['time_m'] = float((int(hour)*60) + int(min) + (int(sec)/60))
        print(obj['time_m'])
    else:
        obj['time_m'] = 0

    #total_time
    if obj['completion_time'] is not None:
        time_in_sheet = obj['completion_time'].split(':')
        hour = time_in_sheet[0]
        min = time_in_sheet[1]
        sec = time_in_sheet[2]
        obj['completion_time'] = float((int(hour)*60) + int(min) + (int(sec)/60))
        print(obj['completion_time'])
    else:
        obj['completion_time'] = 0

    #completion_time
    if obj['total_time'] is not None:
        time_in_sheet = obj['total_time'].split(':')
        hour = time_in_sheet[0]
        min = time_in_sheet[1]
        sec = time_in_sheet[2]
        obj['total_time'] = float((int(hour)*60) + int(min) + (int(sec)/60))
        print(obj['total_time'])
    else:
        obj['total_time'] = 0

    # allocated
    # obj['allocated'] = allocate_obj.check_allocate(obj['course_title'],obj['Group(s)'])
    obj['allocated']=0

    # allocated
    tup.append(tuple(obj.values()))

    example = {
        "user_id": 992,
        "name": "Zeeshaan",
        "email": "zeeshaan@gmail.com",
        "course_id": 26220,
        "course_title": "Online Reputation Management",
        "steps_completed": 0,
        "steps_total": 29,
        "course_completed": "NO",
        "course_completed_on": "",
        "Username": "zeeshaan@gmail.com",
        "First_name": "Zeeshaan",
        "Last_Name": "Dhawan",
        "Groupss": "IIDE April 2021 Weekday ( Old )",
        "Website": "http://919322602331",
        "Biographical_Info": "IIDE April 2021 Weekday",
        "total_time": "",
        "completion_time": "",
        "course_started_on": "",
        "course_total_time_on": "",
        "course_last_step_id": "",
        "course_last_step_type": "",
        "course_last_step_title": "",
        "last_login_date": "",
        "certificate_ids": "No tracked certificates.",
        "completion_status": "WIP",
        "module_completed": '',
        "steps_taken": '',
        "completed_yes": "",
        "course_started": '',
        "batch_type": " ",
        "time_m": '',
        "allocated": ''
    }
    colnames = str(tuple(example.keys())).replace("\'", "")
    if count % buff == 0:
        sql_command = f'insert into learndash {colnames}  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'\
                      f'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
        print(sql_command, tup)
        mc.executemany(sql_command, tup)
        tup = []
        mydb.commit()

    count += 1


mc = mydb.cursor()
mc.execute('select steps_completed ,course_title,Groupss from learndash where steps_completed>0 group by Groupss,course_title')
data = mc.fetchall()
for d in data :
    mc = mydb.cursor()
    query = f'update learndash set allocated = 1 where course_title = "{d[1]}" and Groupss="{d[2]}"'
    mc.execute(query)
    mydb.commit()
    print(query)
