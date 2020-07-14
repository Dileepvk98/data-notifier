from notify_run import Notify
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
from pyvirtualdisplay import Display

def convert_MBtoGB(mb):
    return int(float(mb)/1024)

with Display():
    # we can now start Firefox and it will run inside the virtual display
    browser = webdriver.Firefox()
    # put the rest of our selenium code in a try/finally
    # to make sure we always clean up at the end
    try:
        # browser.get('http://www.google.com')
        # print(browser.title) #this should print "Google"
        # opts = Options()
        # opts.headless = True
        # browser = Firefox(options=opts)
        browser.get('https://??.in')

        un = browser.find_element_by_id('DUser')
        un.send_keys("")
        pw = browser.find_element_by_id('Pwd')
        pw.send_keys("")
        browser.find_element_by_id("button").click()
        print("url after login : ", browser.current_url)
        msg = ""

        try:
            browser.find_element_by_link_text("USAGE").click()
            # print(browser.current_url)
            time.sleep(3)
            used_data_mb = browser.find_element_by_id('totalOctet').text
            rem_data_mb = browser.find_element_by_id('totalOctets').text
            today = date.today()
            browser.get('https://???.in/signout')

        except:
            # print(browser.current_url)
            msg = "login/nav error"

        browser.close()

        if msg != "login/nav error":
            print(used_data_mb)
            print(rem_data_mb)
            print(today)

            try:
                used_data = convert_MBtoGB(used_data_mb)
                rem_data = convert_MBtoGB(rem_data_mb)

                f1 = open('prev_usage.txt', 'r')
                prev_usage = convert_MBtoGB(f1.read())

                daily_usage = used_data - prev_usage
                if daily_usage < 0:
                    msg = "Renewed ?? GB"
                else:
                    msg = "Todays Usage : " + str(daily_usage) + " GB  |  Remaining : " + str(rem_data)+" GB"

                f1 = open('prev_usage.txt', 'w')
                f1.write(str(used_data_mb))

            except:
                msg = "ValueError : empty var"

        print(msg)

        notify = Notify()
        notify.send(msg)

    finally:
        browser.quit()


