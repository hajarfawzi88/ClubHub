import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService

class TestDefaultSuite:
    def setup_method(self, method):
        # Specify the path to the GeckoDriver executable
        geckodriver_path = 'E:\\Downloads\\geckodriver-v0.34.0-win32\\geckodriver.exe'  # Update this path to your geckodriver location
        firefox_binary_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'  # Update this path to your Firefox binary location

        options = webdriver.FirefoxOptions()
        options.binary_location = firefox_binary_path
        service = FirefoxService(executable_path=geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()
 


    def test_test1signup(self):
      self.driver.get("http://localhost:5000/")
      self.driver.set_window_size(786, 656)
      self.driver.find_element(By.CSS_SELECTOR, "body").click()
      self.driver.find_element(By.LINK_TEXT, "Home").click()

      self.driver.find_element(By.LINK_TEXT, "Signup").click()
      self.driver.find_element(By.NAME, "email").click()
      self.driver.find_element(By.NAME, "email").send_keys("HajarFawzi12@gmail.com")
      self.driver.find_element(By.NAME, "username").click()
      self.driver.find_element(By.NAME, "username").send_keys("HajarFawzi12")
      self.driver.find_element(By.NAME, "password").click()
      self.driver.find_element(By.NAME, "password").send_keys("HajarFawzi@123")
      self.driver.find_element(By.NAME, "confirm_password").click()
      self.driver.find_element(By.NAME, "confirm_password").send_keys("HajarFawzi@123")
      self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").click()
      self.driver.find_element(By.CSS_SELECTOR, ".title-2").click()
  
    def test_test2login(self):
        self.driver.get("http://localhost:5000/")
        self.driver.find_element(By.CSS_SELECTOR, "body").click()
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "password").send_keys("Hajar@123")
        self.driver.find_element(By.ID, "username").send_keys("hajar123")
        self.driver.find_element(By.ID, "remember-me").click()
        self.driver.find_element(By.CSS_SELECTOR, "button:nth_child(4)").click()
  
    def test_test3Editusername(self):
        self.driver.get("http://localhost:5000/olduser")
        self.driver.find_element(By.ID, "Edit-button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".info_container:nth-child(3) > .edit_button").click()
        self.driver.find_element(By.ID, "emailInput").click()
        self.driver.find_element(By.ID, "emailInput").send_keys("Hajarrr@gmail.com")
        self.driver.find_element(By.ID, "saveEmailButton").click()
        self.driver.find_element(By.CSS_SELECTOR, ".info_container:nth-child(7) > .edit_button").click()
        self.driver.find_element(By.ID, "usernameInput").click()
        self.driver.find_element(By.ID, "usernameInput").send_keys("HajarFawzi253")
        self.driver.find_element(By.ID, "usernameInput").send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "saveUsernameButton").click()
        self.driver.find_element(By.CSS_SELECTOR, ".edit_button:nth-child(11)").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").click()
        element = self.driver.find_element(By.ID, "password")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.NAME, "new_password").click()
        self.driver.find_element(By.NAME, "new_password").send_keys("Eman@123")
        self.driver.find_element(By.NAME, "confirm_new_password").click()
        self.driver.find_element(By.NAME, "confirm_new_password").send_keys("Eman@123")
        self.driver.find_element(By.ID, "savePasswordButton").click()
  
    def test_test4edituser(self):
        self.driver.get("http://localhost:5000/Editprofile")
        self.driver.find_element(By.XPATH, "//button[@onclick=\"editField(\'username\')\"]").click()
        self.driver.find_element(By.ID, "usernameInput").click()
        self.driver.find_element(By.ID, "usernameInput").send_keys("Hajarrr")
        self.driver.find_element(By.ID, "usernameInput").send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "saveUsernameButton").click()
  
    def test_test5changepassword(self):
        self.driver.get("http://localhost:5000/Editprofile")
        self.driver.set_window_size(1648, 936)
        self.driver.find_element(By.XPATH, "//button[@onclick=\'editPassword()\']").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("Eman@123")
        self.driver.find_element(By.NAME, "new_password").click()
        self.driver.find_element(By.NAME, "new_password").send_keys("Eman1@23")
        self.driver.find_element(By.NAME, "confirm_new_password").click()
        self.driver.find_element(By.NAME, "confirm_new_password").send_keys("Eman1@123")
        self.driver.find_element(By.ID, "savePasswordButton").click()
        assert self.driver.switch_to.alert.text == "New passwords do not match."
        self.driver.find_element(By.NAME, "confirm_new_password").click()
        self.driver.find_element(By.NAME, "confirm_new_password").click()
        element = self.driver.find_element(By.NAME, "confirm_new_password")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.NAME, "confirm_new_password").send_keys("Eman1@23")
        self.driver.find_element(By.ID, "savePasswordButton").click()
        assert self.driver.switch_to.alert.text == "Profile updated successfully"
  
    def test_test7viewclubs(self):
        self.driver.get("http://localhost:5000/olduser")
        self.driver.find_element(By.ID, "view-all-joined-clubs").click()
  
    def test_test12discoverclubs(self):
        self.driver.get("http://localhost:5000/olduser")
        self.driver.set_window_size(1648, 936)
        self.driver.find_element(By.ID, "join-new-clubs").click()
        self.driver.find_element(By.CSS_SELECTOR, "input").click()
        self.driver.find_element(By.CSS_SELECTOR, ".welcome_section").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(1) > .btn").click()
  
    def test_test8editclubdetails(self):
        self.driver.get("http://localhost:5000/olduser")
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) .btn-primary").click()
        self.driver.find_element(By.ID, "name").click()
        self.driver.find_element(By.ID, "name").send_keys("IEEE juniors 2")
        self.driver.find_element(By.ID, "description").click()
        self.driver.find_element(By.ID, "description").send_keys("An international club for kids and teenagers")
        self.driver.find_element(By.ID, "image_url").click()
        self.driver.find_element(By.ID, "image_url").click()
        self.driver.find_element(By.ID, "image_url").click()
        element = self.driver.find_element(By.ID, "image_url")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.ID, "image_url").send_keys("https://github.com/hajarfawzi88/ClubHub/blob/main/Clubimagewebsite.png")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
  
    def test_test9requestevent(self):
        self.driver.get("http://localhost:5000/olduser")
        self.driver.find_element(By.ID, "Request-event").click()
        self.driver.find_element(By.ID, "Club-id").send_keys("1")
        self.driver.find_element(By.ID, "eventName").click()
        self.driver.find_element(By.ID, "eventName").send_keys("Cermony ")
        self.driver.find_element(By.ID, "location").click()
        self.driver.find_element(By.ID, "location").send_keys("Zewailcity")
        self.driver.find_element(By.ID, "expectedMembers").click()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("240")
        self.driver.find_element(By.ID, "date").click()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("241")
        self.driver.find_element(By.ID, "expectedMembers").click()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("242")
        self.driver.find_element(By.ID, "expectedMembers").click()
        element = self.driver.find_element(By.ID, "expectedMembers")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("243")
        self.driver.find_element(By.ID, "expectedMembers").click()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("244")
        self.driver.find_element(By.ID, "expectedMembers").click()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("245")
        self.driver.find_element(By.ID, "expectedMembers").click()
        element = self.driver.find_element(By.ID, "expectedMembers")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("246")
        self.driver.find_element(By.ID, "expectedMembers").click()
        self.driver.find_element(By.ID, "expectedMembers").send_keys("247")
        self.driver.find_element(By.ID, "expectedMembers").click()
        self.driver.find_element(By.ID, "date").click()
        self.driver.find_element(By.ID, "date").send_keys("3/6/2024")
        self.driver.find_element(By.ID, "description").click()
        self.driver.find_element(By.ID, "description").send_keys("Wegz cermony for students to be happy")
  
    def test_test6logout(self):
        self.driver.get("http://localhost:5000/olduser")
        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()
  
    def test_test13manager(self):
        self.driver.get("http://localhost:5000/")
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "password").send_keys("Finalmanager@123")
        self.driver.find_element(By.ID, "username").send_keys("Finalmanager")
        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()
        self.driver.find_element(By.ID, "Request-button").click()
  
    def test_test10requestclub(self):
        self.driver.get("http://localhost:5000/olduser")
        self.driver.find_element(By.ID, "club-name").send_keys("IEEE juniors")
        self.driver.find_element(By.ID, "club-description").click()
        self.driver.find_element(By.ID, "club-description").send_keys("An international club for kids")
        self.driver.find_element(By.ID, "club-image-url").click()
        self.driver.find_element(By.ID, "club-image-url").click()
        self.driver.find_element(By.ID, "club-image-url").send_keys("https://github.com/hajarfawzi88/ClubHub/blob/main/Clubimagewebsite.jpg")
        self.driver.find_element(By.ID, "club-head-email").click()
        self.driver.find_element(By.ID, "club-head-email").click()
        self.driver.find_element(By.ID, "club-head-email").click()
        self.driver.find_element(By.ID, "club-head-email").send_keys("Eman12345@gmail.com")
        self.driver.find_element(By.CSS_SELECTOR, ".create-club-button").click()
        assert self.driver.switch_to.alert.text == "Club Requested successfully!"
  
    def test_test14logout2(self):
        self.driver.find_element(By.ID, "logout-button").click()
  
    def test_tes15soc(self):
        def test_test11soc(self):
            self.driver.get("http://localhost:5000/soc")
            self.driver.find_element(By.CSS_SELECTOR, ".Review").click()
            self.driver.find_element(By.CSS_SELECTOR, ".Review").click()
            self.driver.find_element(By.CSS_SELECTOR, ".approve").click()
