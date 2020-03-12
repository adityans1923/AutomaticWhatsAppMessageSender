import random
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

"""
Class which will open chrome instance and save the user data in a folder(here : "selenium")
Then it will open web.whatsapp and it will ask login for the first time 
then it will automatically select the chat whose name is @title and automatically send text=@text
and have timeout of 240 second in case if ur mobile is not connected to internet
params:
    title = "name of chat"
            exact name is required like if contact is not saved then it will show number like 
            "+91 89 12312" spaces included
    text = " the text you want to send"

"""


class SendMessage:
    def __init__(self, title="bakvas", text="Testing", timeout=120):
        # text = "hello"
        self.title = title
        self.text = text
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("user-data-dir=/home/adi/PycharmProjects/Scrapper/selenium")
        # self.chrome_options.add_argument('--headless')
        # service_args=["--verbose", "--log-path=/tmp/chromedriver.log"]  #Chrome's parameter below
        self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=self.chrome_options)
        self.driver.get("https://web.whatsapp.com/")
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        self.isMessageSent = False
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "side")
                )
            )
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.quit()
        print("after first wait")

    def is_message_sent(self):
        return self.isMessageSent

    def send_message(self, text):
        inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
        input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
        # print(input_box)
        text = text.replace('\n', Keys.SHIFT + Keys.ENTER + Keys.SHIFT)
        input_box.send_keys(text + Keys.ENTER)
        self.isMessageSent = True

        # checking whether the message is sent or not
        time.sleep(2)
        tickPath = '//*[@id="main"]/div[3]/div[1]/div[1]/div[3]/div'
        div_list = self.driver.find_elements_by_xpath(tickPath)
        div_len = len(div_list)
        print(str(div_len))
        tickPath = tickPath + '[' + str(
            div_len) + ']/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/span[@data-icon="msg-check"]'

        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, tickPath)
                )
            )
        except:
            print("Sending message timeout occurs")
        print("Send_message closed after sending")

    def main(self, sleep=0):
        time.sleep(sleep)
        xpath = '//*[@title="' + self.title + '"]'
        rightChat = self.driver.find_element_by_xpath(xpath)
        rightChat.click()
        print("Contact: " + self.title + " Clicked")
        self.send_message(text=self.text)
        self.driver.quit()

    def __del__(self):
        self.driver.quit()
        print("Destroyed Browser")


"""
Class it will run in for infinitely and when sendingTime happens it create a object of 
Above class and pass title and text to the above class object
same will repeat each day
"""


class BackgroundRunner:
    def __init__(self, title, text, sendingTime):
        self.isSendToday = False
        self.todayDate = str(datetime.date.today())
        self.title = title
        self.text = text
        self.sendingTime = sendingTime

    def sendIt(self):

        try:
            obj = SendMessage(title=self.title, text=self.text, timeout=240)
            try:
                obj.main()
                self.isSendToday = obj.is_message_sent()
                del obj
            except:
                print("error in sending message")
        except:
            print("error in Creating or Error in sending")
    
    def run(self):
        while True:

            current_date = str(datetime.date.today())
            # print(current_date)
            current_time = datetime.datetime.now().time()
            # print(current_time.hour)

            if not self.isSendToday:
                if current_time.hour > self.sendingTime and current_time.minute > random.randint(0, 30):
                    self.sendIt()
            else:
                if current_date != self.todayDate:
                    self.todayDate = current_date
                    self.isSendToday = False


contact_title = "group name/contact name"
msg_text = "hello tester"
sending_time = 20

obj = BackgroundRunner(contact_title, msg_text, sending_time)
obj.run()
