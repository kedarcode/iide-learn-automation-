import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.browser import CreateDriver
import os
from Resource import PathResource as path
import pygsheets
import pandas as pd

driver = CreateDriver(False)
driver.get('https://learn.iide.co/wp-admin/admin.php?page=learndash-lms-reports')
driver.find_element(By.CLASS_NAME, 'learndash-data-reports-button').click()

sheetname = ''

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
    sub=[item for item in cur_files if item not in prev_files]
    if len(sub)>0:
        sub=sub[0]
    if sub and '.csv' in sub and '.crdownload' not in sub:
        print(sub)
        sheetname=sub
        break

print('done Downloaed')
print(path.resource_path('client_secret.json'))
gc = pygsheets.authorize(service_file=path.resource_path('windy-forge-364809-19af218316ad.json'))
sh = gc.open('learn_iide')
wks = sh.sheet1

mong = json.loads(pd.read_csv(path.resource_path(os.environ.get('DOWNLOADPATH') + f'/{sheetname}')).to_json())

cols='ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def update_sheet(keys):
    global wks,mong
    for n,i in enumerate(keys):
        col=cols[n]
        cell=col+'1'
        wks.update_value(cell,i)
        print(f'{cols[n] + "2"}:{cols[n]+str(len(mong[i]))}',[[str(mong[i][j])]  for j in mong[i]])
        wks.update_values(f'{cols[n] + "2"}:{cols[n]+str(len(mong[i])+2)}',[[str(mong[i][j])]  for j in mong[i]])


update_sheet(mong.keys())
