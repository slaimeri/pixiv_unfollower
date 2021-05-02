from selenium import webdriver
from os import path
import time
import configparser

class Config():

    def __init__(self):
        self.create_cfg()

    def create_cfg(self):
        if path.exists("./config.ini"):
            return
        else:
            default_conf = """
            [Network]
            web_driver_path = C:/Utils/chromedriver/chromedriver.exe
            web_driver_proxy = 
            sleep_between_refreshes = 5

            [Cookies]
            phpsessid =
            """

            config = configparser.ConfigParser(allow_no_value=True)
            config.read_string(default_conf)

            with open("./config.ini", "w") as configfile:
                config.write(configfile)
                configfile.close()

    def read_cfg(self):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        return config


class WebDriver(Config):

    def __init__(self):
        self.create_cfg()
        self.cfg = self.read_cfg()
    
    def web_driver(self):

        driver_path = self.cfg["Network"]["web_driver_path"]
        
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=%s" % self.cfg["Network"]["web_driver_proxy"])        

        try:
            return webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
        except Exception as e:
            print(e)
            print(f"Web driver not found in pwd, trying {driver_path}")
            try:
                return webdriver.Chrome(executable_path=f"{driver_path}", options=options)
            except Exception as e:
                print(e)
                print("Web driver was not found; Exiting")
                return None

    def start_driver(self, URL):
        driver = self.web_driver()      
        if driver == None:
            return
        else:
            driver.get(URL)
            driver.add_cookie({"name": "PHPSESSID", "domain": "pixiv.net", "value": "%s" %
                              self.cfg["Cookies"]["phpsessid"]})
            driver.refresh()
            return driver

def Unfollow(URL):

    wd = WebDriver()
    driver_obj = wd.start_driver(URL)

    time.sleep(5)

    buttons = ["1", "2"]

    while len(buttons) > 0:
        buttons = driver_obj.find_elements_by_xpath(
            "//button[contains(text(),'Following')]")
        for obj in range(0, len(buttons)):
            driver_obj.execute_script("arguments[0].click();", buttons[obj])        
        driver_obj.refresh()
        cfg = wd.read_cfg()
        time.sleep(int(cfg["Network"]["sleep_between_refreshes"]))

    print("Finished unfollowing")

if __name__ == '__main__':
    while True:
        cfg = Config()
        prompt = int(input("1 - Start unfollowing\n2 - Set PHPSESSID\n3 - Create config\n0 - Exit\n> "))
        if prompt == 1:
            user_input = input("Followers page link: ")
            Unfollow(user_input)
        elif prompt == 2:
            user_input = input("PHPSESSID: ")
            try:     
                cfg = cfg.read_cfg()
                cfg.set("Cookies", "phpsessid", user_input)
                with open("./config.ini", "w") as configfile:
                    cfg.write(configfile)
                    configfile.close()
                    print("Setting PHPSESSID succeeded")
            except Exception as e:
                print("Setting PHPSESSID failed")
        elif prompt == 3:
            cfg.create_cfg()
        elif prompt == 0:
            try:
                quit()
            except Exception as e:
                pass




