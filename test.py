import os
import unittest
# iOS environment
from appium import webdriver
# Options are only available since client version 2.3.0
# If you use an older client then switch to desired_capabilities
# instead: https://github.com/appium/python-client/pull/720
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = XCUITestOptions()
options.platform_name = 'iOS'
options.automation_name = 'XCUITest'
options.no_reset = True

# Platform version and device name is matching simulator that is available at my MacBook, to use relevant simulator
# on your machine check available devices using command:
# xcrun simctl list
options.platformVersion = '14.5'
options.device_name = 'iPhone 14'

# path to application package to be installed on simulator
options.app = 'com.apple.mobilecal'

# following options are doing some 'magic' that helps establish connection to real device
# based on hints from:
# https://stackoverflow.com/questions/69315482/appium-and-desktop-unable-to-launch-wda-session-since-xcode13-and-ios15
# https://discuss.appium.io/t/unable-to-start-webdriveragent-session-because-of-xcodebuild-failure/24542/9
options.new_command_timeout = '60'
options.wda_startup_retries = '3'
options.wda_startup_retry_interval = '20000'
options.wda_local_port = '8132'

appium_server_url = 'http://localhost:4723'
appium_service = AppiumService()


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        appium_service.start()
        # Appium1 points to http://127.0.0.1:4723/wd/hub by default
        self.driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

    

   

    def test_delete_event(self):  # Rename this function to make it a test
        try:
            # Wait for the "Today" text to appear and click it
            delete_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//XCUIElementTypeButton[@name='Delete Event']")))
           
            delete_button.click()
        except NoSuchElementException :
            self.fail("Failed to click 'Delete' button")
        

        try:
            delete_future_events = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//XCUIElementTypeOther[@name='Horizontal scroll bar, 1 page'])[2]")))
            delete_future_events.click()
        except NoSuchElementException: 
            self.fail("Future events buttons not found")
    # Additional wait or check to make sure the next page is loaded
       # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//XCUIElementTypeApplication[@name='Calendar']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")))

        
      
    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
        if appium_service.is_running:
            appium_service.stop()        

if __name__ == '__main__':
    unittest.main()