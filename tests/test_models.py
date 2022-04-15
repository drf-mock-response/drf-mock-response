import json

from django.test import TestCase
from rest_framework import status

from drfmockresponse.models import MockResponse


class DjangoMockResponsesModelsTest(TestCase):
    def test_mock_response__str__(self):
        mock_response_name = "mock-1"
        mock, _ = MockResponse.objects.get_or_create(
            name=mock_response_name,
            defaults={
                "status": status.HTTP_201_CREATED,
                "content_type": MockResponse.CONTENT_TYPE__APPLICATION_JSON,
                "content": json.dumps({"name": "Alice"}),
            },
        )
        expected = mock_response_name
        actual = mock.__str__()
        self.assertEqual(expected, actual)
