from selenium import webdriver
from selenium_stealth import stealth
from Resource import PathResource as path
import os
from dotenv import load_dotenv

load_dotenv()


class CreateDriver:
    def __new__(cls, flag: bool= True):
            PATH = path.resource_path(os.environ.get('DRIVERPATH') + "chromedriver.exe")
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            prefs = {"download.default_directory": path.resource_path(os.environ.get('DOWNLOADPATH'))}
            options.add_experimental_option("prefs", prefs)
            options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/90.0.4430.212 Safari/537.36")
            # options.add_experimental_option("excludeSwitches", ["enable-automation"])
            # options.add_experimental_option('useAutomationExtension', False)
            # options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument("--user-data-dir=" + path.resource_path(os.environ.get('USER_DATA')))
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_experimental_option("detach", True)
            print(PATH)
            driver = webdriver.Chrome(PATH,options=options)
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win64",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )

            return driver



