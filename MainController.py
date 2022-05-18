from selenium import webdriver
import time
import linecache
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Enter the video URL")
videoURL = input()

print("Instances amount")
instancesAmount = int(input())

print("Proxy: true/false")
proxyStatus = str(input())

currentInstancesRemaining = instancesAmount
proxyCurrent = 0

QUALITY = {
    1: ['144p', "tiny"],
    2: ['240p', "small"],
    3: ['360p', "medium"]
}

def runProxy(proxyc):
    
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    chr_options.add_argument("--log-level=3")
    chr_options.add_argument('--disable-features=UserAgentClientHint')
    chr_options.add_argument("--disable-web-security")
    chr_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chr_options.add_argument("--disable-extensions")
    chr_options.add_experimental_option('useAutomationExtension', False)
    chr_options.add_argument('--disable-blink-features=AutomationControlled')
    chr_options.add_argument('--disable-dev-shm-usage')   
    chr_options.add_argument('--disable-gpu')
    chr_options.add_argument("--mute-audio")
    chr_options.add_argument('--no-sandbox')
    chr_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chr_options.add_experimental_option(
    'prefs', 
        {
            'profile.managed_default_content_settings.images': 2,
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False,
            'profile.managed_default_content_settings.stylesheets': 2,
            'profile.default_content_setting_values.notifications': 2,
            'download_restrictions': 3
        }
    )
    
    proxy = '0000:0000'
            
    proxyList = list()

    with open('proxys.txt') as f:
        lines = f.readlines()
        for line in lines:
            proxyList.append(line.strip())        

    proxy = proxyList[proxyc]

    print (proxy)
    
    chr_options.add_argument('--proxy-server=%s' % proxy)
    chr_options.add_argument("--disable-extensions")
    
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }    

    driver = webdriver.Chrome('chromedriver', options=chr_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    driver.get("https://consent.youtube.com/d?continue=https://www.youtube.com/%3Fcbrd%3D1&gl=FR&m=0&pc=yt&uxe=eomn&hl=en&src=2")
    
    time.sleep(3)

    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@jsname='vaX9ac']"))).click()
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@jsname='lW531d']"))).click()
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@jsname='Vosabd']"))).click()
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@jsname='j6LnYe']"))).click()
    
    time.sleep(2)

    driver.get("http://ec2-54-92-197-123.compute-1.amazonaws.com/")
    time.sleep(3)

    random_quality = QUALITY[1][0]

    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@width='560']"));
    time.sleep(3)
    video = driver.find_element_by_id('movie_player')
    time.sleep(1)
    video.click()

    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "button.ytp-button.ytp-settings-button").click()
    driver.find_element(By.XPATH, "//div[contains(text(),'Quality')]").click()
    quality = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(string(),'{random_quality}')]")))
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", quality)
    quality.click()

    time.sleep(10)

    driver.get(videoURL)

    time.sleep(5)

    while 1 == 1:
        driver.find_element(By.XPATH, "//button[@id='button' and @aria-label='Share']").click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='button' and @aria-label='Copy']"))).click()
        driver.find_element(By.XPATH, "//*[@id='close-button']/button[@aria-label='Cancel']").click()
        time.sleep(15)
    
def run(proxyc=proxyCurrent):
    
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    chr_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chr_options.add_argument("--disable-extensions")
    chr_options.add_experimental_option('useAutomationExtension', False)
    chr_options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome('chromedriver', options=chr_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(videoURL)
    
    video = driver.find_element_by_id('movie_player')
    video.send_keys(Keys.SPACE)
    
while currentInstancesRemaining != 0:

    if proxyStatus.lower() == "true":
        threading.Thread(target=runProxy, args=[proxyCurrent]).start()
        time.sleep(30)
    else:
        run()
        
    currentInstancesRemaining -= 1
    proxyCurrent += 1
