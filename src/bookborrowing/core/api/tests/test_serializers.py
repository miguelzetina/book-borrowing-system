# -*- coding: utf-8 -*-
from django.test import TestCase

from rest_framework import serializers

from ....core.api.serializers import base


class DynamicFieldsSerializerTestCase(TestCase):
    """
    Test for the ```tandl.core.api.serializer.base.DynamicFieldsMixin``` class.
    """
    def setUp(self):
        class TestSerializer(base.DynamicFieldsMixin, serializers.Serializer):
            """
            Serializer class for testing.
            """
            field1 = serializers.IntegerField()
            field2 = serializers.IntegerField()
            field3 = serializers.IntegerField()

        self.serializer_class = TestSerializer
        self.test_data = {
            'field1': 1,
            'field2': 2,
            'field3': 3,
        }

    def test_creating_serializer_without_declaring_fields(self):
        serializer = self.serializer_class(self.test_data)
        self.assertDictEqual(serializer.data, self.test_data)

    def test_creating_serializer_declaring_fields(self):
        serializer = self.serializer_class(
            self.test_data, fields=['field1', 'field2'])

        self.assertDictEqual(serializer.data, {
            'field1': 1,
            'field2': 2,
        })

        serializer = self.serializer_class(
            self.test_data, fields=['field1', 'field3'])

        self.assertDictEqual(serializer.data, {
            'field1': 1,
            'field3': 3,
        })

        serializer = self.serializer_class(self.test_data, fields=['field2'])

        self.assertDictEqual(serializer.data, {
            'field2': 2,
        })

    def test_creating_serializer_with_empty_fields_hass_all_fields(self):
        serializer = self.serializer_class(self.test_data, fields=[])
        self.assertDictEqual(serializer.data, self.test_data)
