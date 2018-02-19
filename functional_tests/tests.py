from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('./venv/selenium/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_starting_a_new_todo_list(self):
        # User want use a to-do lists app.
        # He goes to the Home Page
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header.text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # He types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When he hits enter, the page updates and now the page lists as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting him to add another item. He
        # enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on the list
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        
        self.fail('Finish the test')

if __name__ == "__main__":
    unittest.main(warnings='ignore')