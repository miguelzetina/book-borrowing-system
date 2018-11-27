# -*- coding: utf-8 -*-
import json

from django.core.management import call_command
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from bookborrowing.core.api.tests.tests_viewsets import ApiTestMixin
from bookborrowing.books.models import Book


class BooksTests(APITestCase, ApiTestMixin):
    fixtures = (
        'roles',
        'genres',
        'authors',
        'books'
    )

    def test_books_list_superadmin_200(self):
        user = self.create_superuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:books-list')
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        data = json.loads(response._container[0].decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["meta"]["pagination"]["count"], 1)
        self.assertEqual(data["data"][0]["type"], "books")
        self.assertTrue("id" in data["data"][0])
        self.assertEqual(data["data"][0]["id"], '1')
        self.assertEqual(data["data"][0]["attributes"]["name"], "Book name")
        self.assertEqual(
            data["data"][0]["attributes"]["isbn"],
            "1234567890123"
        )
        self.assertTrue("genre" in data["data"][0]["relationships"])
        self.assertTrue("author" in data["data"][0]["relationships"])
    
    def test_books_list_search_superadmin_200(self):
        user = self.create_superuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:books-list')
        response = self.client.get(
            endpoint_url,
            {'q': 'search'},
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_books_detail_superadmin_200(self):
        user = self.create_superuser()
        token = self.create_token(user)
        book = Book.objects.first()
        endpoint_url = reverse('api:v1:books-detail', kwargs={'pk': book.id})
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        data = json.loads(response._container[0].decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["data"]["type"], "books")
        self.assertTrue("id" in data["data"])
        self.assertEqual(data["data"]["id"], str(book.id))

    def test_books_detail_superadmin_404(self):
        user = self.create_superuser()
        token = self.create_token(user)
        endpoint_url = reverse('api:v1:books-detail', kwargs={'pk': -1})
        response = self.client.get(
            endpoint_url,
            HTTP_AUTHORIZATION=token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)