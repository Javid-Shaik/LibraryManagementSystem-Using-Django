from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from my_app.models import RegisterModel, Books, Member, Borrowings

class TestViews(TestCase):
    
    def setUp(self):
        # Create sample data for testing
        self.client = Client()
        self.register_url = reverse('signup:register')
        # Create test user
        self.user_data = {
            'fname': 'John',
            'lname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'testpassword',
            'phone': '1234567890',
            'address': '123, Test Street',
            'role': 'student'  # Modify as necessary
        }

    def test_register_view(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Check for successful redirect

    def test_login_view(self):
        login_url = reverse('signup:login_user')
        response = self.client.post(login_url, {'username': 'johndoe', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Check for successful redirect
        
    

    # Add more test methods for other views as necessary
from django.test import LiveServerTestCase
from selenium import webdriver

class LoginFunctionalTest(LiveServerTestCase):
    
    def setUp(self):
        self.selenium = webdriver.Chrome()  # or any other browser driver
        super().setUp()

    def test_login(self):
        self.selenium.get(self.live_server_url + '/login')
        username_input = self.selenium.find_element_by_name('username')
        password_input = self.selenium.find_element_by_name('password')
        login_button = self.selenium.find_element_by_id('login-button')

        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        login_button.click()

        # Add assertions to check if login is successful
        # Example: self.assertTrue('Welcome' in self.selenium.page_source)

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()
        
class IntegrationTest(TestCase):
    
    def test_register_user(self):
        user = RegisterModel.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.assertEqual(RegisterModel.objects.count(), 1)

    def test_create_book(self):
        book = Books.objects.create(title='Test Book', author_name='Test Author', isbn='1234567890',publication=date.today() )
        self.assertEqual(Books.objects.count(), 1)
