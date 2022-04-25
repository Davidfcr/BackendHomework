from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import User


class UserTestModel(APITestCase):

    def test_create_user_with_correct_email_and_password(self):
        user = User.objects.create_user(email='testemail@email.com', password='Password123!', username='')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testemail@email.com')

    def test_raise_exception_when_create_user_password_with_not_min_length(self):
        self.assertRaises(ValidationError, User.objects.create_user, email='testemail@email.com',
                          password='Pass', username='')

    def test_raise_exception_when_create_user_with_empty_email(self):
        self.assertRaises(ValidationError, User.objects.create_user, email='', password='Password123!', username='')

    def test_raise_exception_when_create_user_with_incorrect_email_format(self):
        user = User.objects.create_user(email='testemailemail.com', password='Password123!', username='')
        try:
            user.full_clean()
        except ValidationError as e:
            self.assertTrue('email' in e.message_dict)

    def test_create_user_with_square_bracket_password(self):
        user = User.objects.create_user(email='testemail@email.com', password='Password123]')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testemail@email.com')

    def test_raise_exception_when_create_user_password_with_not_lowercase(self):
        with self.assertRaisesMessage(ValidationError, 'Validate the password value contains at least one ' +
                                                       'lowercase letter'):
            User.objects.create_user(email='testemail@email.com', password='PASSWORD123!')

    def test_raise_exception_when_create_user_password_with_not_uppercase(self):
        with self.assertRaisesMessage(ValidationError, 'Validate the password value contains at least one ' +
                                                       'uppercase letter'):
            User.objects.create_user(email='testemail@email.com', password='password123!')

    def test_raise_exception_when_create_user_password_with_not_special_character(self):
        with self.assertRaisesMessage(ValidationError, 'Validate the password value contains at least one ' +
                                                       'of the following characters: !, @, #, ? or ]'):
            User.objects.create_user(email='testemail@email.com', password='Password1234')

    def test_register_user_correct(self):
        user = {
            'email': "testuser@email.com",
            'password': "Password123!"
        }
        response = self.client.post(reverse('register'), user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_incorrect_data_password(self):
        user = {
            'email': "testuser@email.com",
            'password': "Pass"
        }
        response = self.client.post(reverse('register'), user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_correct(self):
        user = {
            'email': "testuser@email.com",
            'password': "Password123!"
        }
        self.client.post(reverse('register'), user)
        response = self.client.post(reverse('login'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_incorrect_data_email(self):
        user = {
            'email': "testuseremail.com",
            'password': "Password123!"
        }
        self.client.post(reverse('register'), user)
        response = self.client.post(reverse('login'), user)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
