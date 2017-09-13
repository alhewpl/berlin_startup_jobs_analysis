from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()
driver.get("http://www.berlinstartupjobs.com")
assert "Berlin Startup" in driver.title
elem = driver.find_element_by_name("h1")
time.sleep(20)
elem.clear()
elem.send_keys("python")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
#driver.close()