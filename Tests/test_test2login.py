# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestTest2login():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_test2login(self):
    self.driver.get("http://localhost:5000/")
    self.driver.set_window_size(1648, 936)
    self.driver.find_element(By.LINK_TEXT, "Log in").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "password").send_keys("EmanAllam@123")
    self.driver.find_element(By.ID, "username").send_keys("EmanAllam123")
    self.driver.find_element(By.ID, "remember-me").click()
    self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()
  
