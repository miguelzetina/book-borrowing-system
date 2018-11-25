# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from bookborrowing.core.api.tests.tests_viewsets import ApiTestMixin


class AuthenticationTests(APITestCase, ApiTestMixin):

    fixtures = [
        'roles'
    ]

    def test_register_login_backoffice_201_like_superadmin(self):
        user = self.create_superuser()
        endpoint_url = reverse('api:v1:auth-local')
        request_data = {
            "email": user.email,
            "password": "password"
        }
        response = self.client.post(
            endpoint_url,
            request_data,
            format='json'
        )

        self.assertEqual('token' in response.data, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_login_backoffice_403_bad_password(self):
        user = self.create_superuser()
        endpoint_url = reverse('api:v1:auth-local')
        request_data = {
            "email": user.email,
            "password": "12323"
        }
        response = self.client.post(
            endpoint_url,
            request_data,
            format='json'
        )

        self.assertEqual('token' in response.data, False)
        self.assertEqual(response.data[0]["source"]["pointer"], '/data')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_login_backoffice_403_bad_email(self):
        endpoint_url = reverse('api:v1:auth-local')
        request_data = {
            "email": "dont_exist@mail.com",
            "password": "12323"
        }
        response = self.client.post(
            endpoint_url,
            request_data,
            format='json'
        )

        self.assertEqual('token' in response.data, False)
        self.assertEqual(response.data[0]["source"]["pointer"], '/data')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)