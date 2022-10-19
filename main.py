import json
import mysql.connector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.browser import CreateDriver
from allocated import get_allocate
import os
from Resource import PathResource as path
import pygsheets
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="learndash",
    password="",
    port=3307

)
buff = 1000
count = 1
driver = CreateDriver()
driver.get('https://learn.iide.co/wp-admin/admin.php?page=learndash-lms-reports')
driver.find_element(By.CLASS_NAME, 'learndash-data-reports-button').click()

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
# print(path.resource_path('client_secret.json'))
# ----------------------------------------------------------------------------------------------------------------------------------

gc = pygsheets.authorize(service_file=path.resource_path('windy-forge-364809-19af218316ad.json'))
sh = gc.open('learn_iide')
wks = sh.sheet1
read = wks.get_all_values()

mong = json.loads(pd.read_csv(path.resource_path(os.environ.get('DOWNLOADPATH') + f'{sheetname}')).to_json())

# cols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# def update_sheet(keys):
#     global wks, mong
#     for n, i in enumerate(keys):
#         col = cols[n]
#         cell = col + '1'
#         wks.update_value(cell, i)
#         print(f'{cols[n] + "2"}:{cols[n] + str(len(mong[i]))}', [[str(mong[i][j])] for j in mong[i]])
#         wks.update_values(f'{cols[n] + "2"}:{cols[n] + str(len(mong[i]) + 2)}', [[str(mong[i][j])] for j in mong[i]])
# update_sheet(mong.keys())

tup = []
cols = list(mong.keys())
mc = mydb.cursor()
mc.execute('truncate table new_table')
driver.quit()

allocate_obj = get_allocate('windy-forge-364809-19af218316ad.json', 'Overall course Completion')

for j in range(1, len(mong[cols[0]])):
    obj = {}
    for c in cols:
        obj[c] = mong[c][str(j)]

    # completion status
    if obj['steps_completed'] == obj['steps_total']:
        obj['completion_status'] = 'Completed'
    elif obj['steps_completed'] < obj['steps_total']:
        obj['completion_status'] = 'Incomplete'
    elif int(obj['steps_completed']) == 0:
        obj['completion_status'] = 'Not Started'
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
        if 'certificationcourse' in obj['Group(s)'].lower().strip():
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
    elif obj['steps_completed'] < obj['steps_total']:
        obj['completion_status'] = 'WIP'
    elif int(obj['steps_completed']) == 0:
        obj['completion_status'] = 'Not Started'
    else:
        obj['completion_status'] = ''

        # time_m
    if obj['completion_time'] is not None:
        time_in_sheet = obj['completion_time'].split(':')
        hour = time_in_sheet[0]
        min = time_in_sheet[1]
        sec = time_in_sheet[2]
        obj['time_m'] = int(hour) + int(min) + int(sec)
    else:
        obj['time_m'] = ' '

    # allocated
    obj['allocated'] = allocate_obj.check_allocate(obj['course_title'],obj['Group(s)'])

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
        sql_command = f'insert into new_table {colnames}  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'\
                      f'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
        print(sql_command, tup)
        mc.executemany(sql_command, tup)
        tup = []
        mydb.commit()

    count += 1
