from webbot import Browser
from notify_run import Notify
import pandas as pd
from datetime import date

def convert_MBtoGB(mb):
    return int(float(mb)/1024)

web = Browser()
web.go_to('??.in')
web.type('', id='DUser')
web.type('', id='Pwd')
web.press(web.Key.ENTER)
print(web.get_current_url())

web.go_to('??.in/goToForm?formId=CUP001')

used_data_mb = web.find_elements(id='totalOctet')[0].text
rem_data_mb = web.find_elements(id='totalOctets')[0].text
today = date.today()

print(used_data_mb)
print(rem_data_mb)
print(today)

# # used_data_mb = '35100.55'
# # rem_data_mb = '5000.45'
used_data = convert_MBtoGB(used_data_mb)
rem_data = convert_MBtoGB(rem_data_mb)

web.go_to('??.in/signout')

# # log_file_df = pd.read_csv("log.csv")
# # log_file_df['usage(GB)'] = log_file_df['usage(GB)'].apply(lambda x: int(x))
# # total_usage = sum(log_file_df['usage(GB)'].tolist())

f1 = open('prev_usage.txt', 'r')
prev_usage = convert_MBtoGB(f1.read())
# print(prev_usage)

daily_usage = used_data - prev_usage
if daily_usage < 0:
    msg = "Renewed ?? GB"
else:
    msg = "Todays Usage : " + str(daily_usage) + " GB  |  Remaining : " + str(rem_data)+" GB"
print(msg)

f1 = open('prev_usage.txt', 'w')
f1.write(str(used_data_mb))

notify = Notify()
notify.send(msg)
