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

options = XCUITestOptions()
options.platformVersion = '16.4.1'
options.platform_name = 'iOS'
options.device_name = 'iPhone SE (2nd generation)'
options.automation_name = 'XCUITest'

# other pre-installed iOS apps bundle ids can be found here:
# https://support.apple.com/en-gb/guide/deployment/depece748c41/web
options.bundle_id = 'com.apple.calculator'

# enter udid of device you would like to run test on
# to get udid of your device run in terminal following command:
# idevice_id -l
# or
# ios-deploy -c
# to get some additional basic info about connected device
options.udid = ''

# following options are doing some 'magic' that helps establish connection to real device
# based on hints from:
# https://stackoverflow.com/questions/69315482/appium-and-desktop-unable-to-launch-wda-session-since-xcode13-and-ios15
# https://discuss.appium.io/t/unable-to-start-webdriveragent-session-because-of-xcodebuild-failure/24542/9
options.new_command_timeout = '60'
options.wda_startup_retries = '3'
options.wda_startup_retry_interval = '20000'
options.wda_local_port = '8132'
# always fresh installation of webDriverAgent
# options.use_new_wda = 'true'


appium_server_url = 'http://localhost:4723'
appium_service = AppiumService()


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        appium_service.start()
        # Appium1 points to http://127.0.0.1:4723/wd/hub by default
        self.driver = webdriver.Remote(appium_server_url, options=options)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
        if appium_service.is_running:
            appium_service.stop()

    def test_compute_sum(self) -> None:
        # values to be summed
        x = 1
        y = 2
        # finding all elements needed for summing 2 integers. Based on my Slovak localization of iPhone accesibility ids
        # are in Slovak language. Always check yours locators in app using Appium Inspector
        num1 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=str(x))
        num2 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=str(y))
        sum_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='pričítať')
        equals_btn = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='rovná sa')
        result = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Výsledok')
        # calculation actions performed in app
        num1.click()
        sum_btn.click()
        num2.click()
        equals_btn.click()
        # assertion of result
        assert result.text == '3'


if __name__ == '__main__':
    unittest.main()
