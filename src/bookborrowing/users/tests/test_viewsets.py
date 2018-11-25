# -*- coding: utf-8 -*-
import json

from django.core.management import call_command
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from bookborrowing.core.api.tests.tests_viewsets import ApiTestMixin


class UsersTests(APITestCase, ApiTestMixin):
    fixtures = (
        'roles',
        'users'
    )

    def test_users_list_superadmin_200(self):
        user = self.create_superuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:users-list')
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        data = json.loads(response._container[0].decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["meta"]["pagination"]["count"], 3)
        self.assertEqual(data["data"][0]["type"], "users")
        self.assertTrue("id" in data["data"][0])

    def test_users_list_search_superadmin_200(self):
        user = self.create_superuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:users-list')
        response = self.client.get(
            endpoint_url,
            {'q': 'search'},
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        data = json.loads(response._container[0].decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_list_admin_200(self):
        user = self.create_adminuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:users-list')
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        data = json.loads(response._container[0].decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["meta"]["pagination"]["count"], 3)
        self.assertEqual(data["data"][0]["type"], "users")
        self.assertTrue("id" in data["data"][0])

    def test_users_detail_superadmin_200(self):
        user = self.create_superuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:users-detail', kwargs={'pk': user.id})
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        data = json.loads(response._container[0].decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["data"]["type"], "users")
        self.assertTrue("id" in data["data"])
        self.assertEqual(data["data"]["id"], str(user.id))

    def test_users_detail_superadmin_404(self):
        user = self.create_superuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:users-detail', kwargs={'pk': -1})
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_users_detail_admin_200(self):
        user = self.create_adminuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:users-detail', kwargs={'pk': user.id})
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        data = json.loads(response._container[0].decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["data"]["type"], "users")
        self.assertTrue("id" in data["data"])
        self.assertEqual(data["data"]["id"], str(user.id))

    def test_users_detail_admin_404(self):
        user = self.create_adminuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:users-detail', kwargs={'pk': -1})
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_detail_403(self):
        user = self.create_adminuser()
        endpoint_url = reverse('api:v1:users-detail', kwargs={'pk': user.id})
        response = self.client.get(
            endpoint_url,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_users_detail_dont_exist_403(self):
        user = self.create_adminuser()
        endpoint_url = reverse('api:v1:users-detail', kwargs={'pk': -1})
        response = self.client.get(
            endpoint_url,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)