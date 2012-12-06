from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

from urlparse import urljoin


class SansaLiverServerTestCase(LiveServerTestCase):
    """
    Generic SANSA LiveServerTestCase
    """

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        # maximum time to wait for page load
        cls.browser.implicitly_wait(5)
        cls.actionChains = ActionChains(cls.browser)
        super(SansaLiverServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SansaLiverServerTestCase, cls).tearDownClass()


class Menu():
    """
    Menu PageObject

    * menu interactions
    * checks menu items availability
    """

    ANONYMOUS_MENU = [
        u' Home', u' Login', u' Register', u' Reset Password', u' About',
        u' Contact']

    STAFF_MENU = [
        u' Home', u' Search', u' My Cart', u' Order Now!', u' Popular Links',
        u' Staff', u' Account', u' About', u' Contact']

    REGULAR_MENU = [
        u' Home', u' Search', u' My Cart', u' Order Now!', u' Popular Links',
        u' Account', u' About', u' Contact']

    def __init__(self, theWebDriver):
        self.browser = theWebDriver
        # check if menu is available (also inits menu)
        self.is_available()

    def is_available(self):
        try:
            self.menu = self.browser.find_element_by_id("menu")
            return True
        except NoSuchElementException:
            return False

    def get_menu_items(self):
        # store all links by using css selector
        self.menu_items = self.menu.find_elements_by_css_selector('a, span')

    def for_anonymous_user(self):
        return self.check_menu_items('ANONYMOUS')

    def for_staff_user(self):
        return self.check_menu_items('STAFF')

    def for_regular_user(self):
        return self.check_menu_items('REGULAR')

    def check_menu_items(self, theMenuType):
        self.get_menu_items()
        # get menu titles (text)
        self.menu_item_titles = [
            ele.text for ele in self.menu_items if ele.is_displayed()]

        if theMenuType == 'ANONYMOUS':
            if self.menu_item_titles == self.ANONYMOUS_MENU:
                return True
            else:
                raise Exception('Expected %s, got %s' % (
                    self.ANONYMOUS_MENU, self.menu_item_titles))

        elif theMenuType == 'STAFF':
            if self.menu_item_titles == self.STAFF_MENU:
                return True
            else:
                raise Exception('Expected %s, got %s' % (
                    self.STAFF_MENU, self.menu_item_titles))

        elif theMenuType == 'REGULAR':
            if self.menu_item_titles == self.REGULAR_MENU:
                return True
            else:
                raise Exception('Expected %s, got %s' % (
                    self.REGULAR_MENU, self.menu_item_titles))
        else:
            raise Exception('Unknown menu type')

    def click_home(self):
        self.menu.find_element_by_partial_link_text('Home').click()

    def click_login(self):
        self.menu.find_element_by_partial_link_text('Login').click()

    def click_logout(self):
        self.menu.find_element_by_partial_link_text('Logout').click()

    def click_search(self):
        self.menu.find_element_by_partial_link_text('Search').click()


class Login():
    """
    Login PageObject, abstracting login
    """
    def __init__(self, theWebDriver, theUser, thePassword):
        self.browser = theWebDriver
        # find login menu option
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys(theUser)
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys(thePassword)

        # find login button and click it
        self.browser.find_element_by_xpath('//input[@value="Login"]').click()


class SeleniumLogin(SansaLiverServerTestCase):
    fixtures = ['test_user.json']

    def test_login_staff(self):
        # we use 'urljoin' to prepare URL
        self.browser.get(urljoin(self.live_server_url, reverse('index')))

        # for this test we need menu PageObject
        myMenu = Menu(self.browser)

        # check if we have menu
        self.assertTrue(myMenu.is_available())
        # check if menu is for anonymous user
        self.assertTrue(myMenu.for_anonymous_user())

        # click login menu item
        myMenu.click_login()

        # after ANY page refresh, we basically invalidate DOM, so we need to
        # reinitialize any PageObjects if we are going to use them
        # in this case we would reinitialize myMenu
        # myMenu = Menu(self.browser)

        # login staff user
        Login(self.browser, 'timlinux', 'password')

        myMenu = Menu(self.browser)
        self.assertTrue(myMenu.for_staff_user())

    def test_login_user(self):
        # we use 'urljoin' to prepare URL
        self.browser.get(urljoin(self.live_server_url, reverse('index')))

        # for this test we need menu PageObject
        myMenu = Menu(self.browser)

        # check if we have menu
        self.assertTrue(myMenu.is_available())

        # click login menu item
        myMenu.click_login()

        # login staff user
        Login(self.browser, 'pompies', 'password')

        myMenu = Menu(self.browser)
        self.assertTrue(myMenu.for_regular_user())
