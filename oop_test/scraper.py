from selenium import webdriver
CHROME_DERIVER = "E:\chromedriver_win32 (1)\chromedriver"

class Scraper():
    def __init__(self,url):
        self.url= url

    def get_code(self):
        url=self.url
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(executable_path=CHROME_DERIVER, options=options)
        driver.get(self.url)
        username = driver.find_element_by_id('username_or_email')
        password = driver.find_element_by_id('password')
        button = driver.find_element_by_id('allow')
        username.send_keys('mudholsrirang')
        password.send_keys('Warking@18')
        button.click()
        code = driver.find_element_by_xpath('//*[@id="oauth_pin"]/p/kbd/code')
        driver.quit()
        code=code.text
        print(code)
        return code

