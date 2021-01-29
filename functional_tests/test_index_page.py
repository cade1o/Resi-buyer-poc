from selenium import webdriver
from ResiBuyer.models import Product, Order, Information
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestIndexPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_login_page_is_displayed(self):
        self.browser.get(self.live_server_url)

        #user requests for the page for the first time

        alert = self.browser.find_element_by_class_name('content-section')
        self.assertEquals(
            alert.find_element_by_tag_name('button').text,
            'Login'
        )

    def test_sign_up_button_redirect(self):
        self.browser.get(self.live_server_url)

        alert = self.browser.find_element_by_class_name('content-section')

        register_url = self.live_server_url + reverse('register')

        alert.find_element_by_tag_name('a').click()
        
        self.assertEquals(
            self.browser.current_url,
            register_url
        )
    
    # def test_login_page_redirect(self):
    #     self.browser.get(self.live_server_url)

    #     alert = self.browser.find_element_by_class_name('content-section')

    #     alert.find_element_by_id('login').click()

    #     home_url = self.live_server_url

    #     print("This is the home url: " + home_url)
    #     print("this is the current url: " + self.browser.current_url)
    #     self.assertEquals(
    #         self.browser.current_url,
    #         home_url
    #     )



    