

import Backend.website_url as const
from selenium.webdriver.common.by import By
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

class Scrap(webdriver.Chrome):
    def __init__(self, driver_path=r"./chromedriver.exe", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.headless=False
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        super(Scrap, self).__init__(options=options)
        self.implicitly_wait(300)
        self.maximize_window()
        self.main_list = []
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
    def land_first_page(self,id):
        web = const.BASE_URL+id
        self.get(web)
    def run(self):
        print("HIII")
        element = self.find_element(By.TAG_NAME,'h2')
        table = self.find_elements(By.CSS_SELECTOR, 'tr')
        store =[]
        for i in table:
            store.append(str(i.text))

        x=0
        y=0
        z=0


        for i in store:


            if 'Oaklands Estate Reserve parkrun' in i:
                x+=1
            elif 'Seacliff Esplanade parkrun' in i:
                y+=1
            elif 'Edithburgh parkrun' in i:
                z+=1
        #     print(i)
        #     print(x,y,z)
        # print(x,y,z)

        if x!=0 and y!=0 and z!=0:
            print('Found')
            name = str(element.text)
            name = name.split('(')
            current_date = datetime.now().strftime('%d-%b-%Y')
            return [name[0],current_date]
        else:
            return ['Not Found']

