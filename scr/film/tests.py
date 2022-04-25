from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Film


class TestFilmCreate(APITestCase):

    @property
    def film(self):
        return {
            'title': "The Godfather",
            'director': "Francis Ford Coppola",
            'rating': "9",
            'description': "The aging patriarch of an organized crime dynasty in postwar New York City transfers " +
                           "control of his clandestine empire to his reluctant youngest son",
            'is_private': False
        }

    def setup_authentication(self):
        user = {
            'email': "testuser@email.com",
            'password': "Password123!"
        }
        self.client.post(reverse('register'), user)
        response = self.client.post(reverse('login'), user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    def test_create_film_error_with_not_authentication(self):
        response = self.client.post(reverse('film'), self.film)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_film_error_with_wrong_rating(self):
        self.setup_authentication()
        wrong_film = self.film
        wrong_film['rating'] = 12
        response = self.client.post(reverse('film'), wrong_film)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_film_correct_with_authentication(self):
        self.setup_authentication()
        response = self.client.post(reverse('film'), self.film)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_public_film_correct(self):
        self.setup_authentication()
        response = self.client.get(reverse('all_film'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.filter(is_private=False).count(), response.data['count'])

    def test_get_all_private_film_correct(self):
        self.setup_authentication()
        privates_film_after = self.client.get(reverse('film'))
        self.client.post(reverse('film'), self.film)
        privates_film_before = self.client.get(reverse('film'))

        self.assertEqual(privates_film_after.data['count']+1, privates_film_before.data['count'])

    def test_update_film_correct(self):
        self.setup_authentication()
        film = self.client.post(reverse('film'), self.film)
        updated_film = {
            'rating': "10",
        }
        response = self.client.put(reverse('update_film', kwargs={'id': film.data['id']}), updated_film)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 10)



