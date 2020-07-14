import requests
from notify_run import Notify
from datetime import date
import json

def convert_MBtoGB(mb):
    return int(float(mb)/1024)


username = ""
password = ""
notify_link = ""
msg = ""

f_cred = open("/home/dvk/Programs/data-notifier/credentials.txt",'r')
all_lines = f_cred.readlines()
username = all_lines[0]
password = all_lines[1]
notify_link = all_lines[2]


session = requests.Session()
data =  {"DUser":username, "Pwd":password}

try:
	res = session.post("https://?????/loginVal?userId="+data["DUser"], data, timeout=10)
except:
	msg = "Login Error"

if msg != "Login Error":
	data = {'ACTIVE_PCC_RULE_NAMES':'','CREATE_TIME':'',
			'CS.GatewayAddress':'','CS.GatewayName':'',
			'CS.SessionID':'',
			"CS.SessionIPv4":"","CS.UserIdentity":"",
			"LAST_UPDATE_TIME":"","QoSProfile.Name":"",
			"Sub.DataPackage":"","Sub.SubscriberIdentity":"",
			"addOnEndTime":"","addOnStartTime":"",
			"cMonth":"","cYear":"","connType":"",
			"downloadByte":"","packageName":"",
			"subscriberCode":data["DUser"],"totalByte":""}

	try:
		data_usage = session.post("https://?????/totalBalance", data=data, timeout=10)
		logout = session.get("https://??????/signout")
		list_data = json.loads(data_usage.text)
	except:
		msg = "Navigation Error"

	if msg != "Navigation Error":
		# try:
		today = date.today()
		list_data = json.loads(data_usage.text)
		usage_log = json.loads(list_data[0]["usage"])

		rem_data_mb = usage_log[0]["balance"]["totalOctets"]
		used_data_mb = usage_log[0]["curretUsage"]["totalOctets"]
		up_mb = usage_log[0]["curretUsage"]["uploadOctets"]
		down_mb = usage_log[0]["curretUsage"]["downloadOctets"]

		# print(rem_data_mb, used_data_mb, up_mb, down_mb)

		used_data = convert_MBtoGB(used_data_mb)
		rem_data = convert_MBtoGB(rem_data_mb)
		up = convert_MBtoGB(up_mb)
		down = convert_MBtoGB(down_mb)

		f1 = open('/home/dvk/Desktop/data-notifier/prev_usage.txt', 'r')
		f1_data = f1.readlines()
		prev_usage = convert_MBtoGB(f1_data[0])
		prev_up = convert_MBtoGB(f1_data[1])
		prev_down = convert_MBtoGB(f1_data[2])

		daily_usage = used_data - prev_usage
		daily_up = up - prev_up
		daily_down = down - prev_down

		if daily_usage < 0:
			msg = "Renewed ???GB"
		else:
			msg = "Down : " + str(daily_down)+"GB | " + "Up : " + str(daily_up)+"GB  |  Remaining : " + str(rem_data)+"GB"

		f1 = open('/home/dvk/Programs/data-notifier/prev_usage.txt', 'w')
		f1.write(str(used_data_mb)+"\n")
		f1.write(str(up_mb)+"\n")
		f1.write(str(down_mb))
		# except:
		# 	msg = "Other Error"

notify = Notify(endpoint=notify_link)
notify.send(msg)

# print(msg)
