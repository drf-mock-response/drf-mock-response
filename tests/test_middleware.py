import json

from django.test import RequestFactory, TestCase
from mock import patch
from rest_framework import status

from drfmockresponse.http_headers import (
    HEADER_KEY__HTTP_MOCK_RESPONSE_DELAY_KEY,
    HEADER_KEY__HTTP_MOCK_RESPONSE_ID_KEY,
)
from drfmockresponse.middleware import MockResponseMiddleware
from drfmockresponse.models import MockResponse


def http_response_matcher(this, other):
    return all(
        [
            this.status_code == other.status_code,
            this.headers["content-type"] == other.headers["content-type"],
            this.content == other.content,
        ]
    )


class DjangoMockResponsesMiddlewareTest(TestCase):
    def setUp(self):
        def get_response(request):
            return request

        self.request_factory = RequestFactory()
        self.middleware = MockResponseMiddleware(get_response)

    def test_mock_not_requested(self):
        request = self.request_factory.get("")
        expected = None
        actual = self.middleware.process_view(request, None, None, None)
        self.assertEqual(expected, actual)

    def test_mock_requested_but_not_found(self):
        request = self.request_factory.get(
            "", **{HEADER_KEY__HTTP_MOCK_RESPONSE_ID_KEY: "does_not_exist"}
        )
        expected = None
        actual = self.middleware.process_view(request, None, None, None)
        self.assertEqual(expected, actual)

    def test_mock_requested_custom_response(self):
        mock_response_name = "mock-1"
        mock, _ = MockResponse.objects.get_or_create(
            name=mock_response_name,
            defaults={
                "status": status.HTTP_201_CREATED,
                "content_type": MockResponse.CONTENT_TYPE__APPLICATION_JSON,
                "content": json.dumps({"name": "Alice"}),
            },
        )

        request = self.request_factory.get(
            "",
            **{
                HEADER_KEY__HTTP_MOCK_RESPONSE_ID_KEY: mock_response_name,
            }
        )
        expected = mock.get_http_response()
        actual = self.middleware.process_view(request, None, None, None)
        self.assertTrue(http_response_matcher(expected, actual))

    def test_mock_requested_standard_http_response(self):
        request = self.request_factory.get(
            "", **{HEADER_KEY__HTTP_MOCK_RESPONSE_ID_KEY: str(status.HTTP_410_GONE)}
        )
        expected = MockResponse(status=status.HTTP_410_GONE).get_http_response()
        actual = self.middleware.process_view(request, None, None, None)
        self.assertTrue(http_response_matcher(expected, actual))

    def test_mock_not_requested_with_valid_delay(self):
        delay_seconds = 10.4
        request = self.request_factory.get(
            "", **{HEADER_KEY__HTTP_MOCK_RESPONSE_DELAY_KEY: str(delay_seconds)}
        )
        with patch("time.sleep") as sleep_mock:
            _ = self.middleware.process_view(request, None, None, None)
            self.assertEqual(1, sleep_mock.call_count)
            sleep_mock.assert_called_with(delay_seconds)

    def test_mock_not_requested_with_not_valid_delay(self):
        request = self.request_factory.get(
            "", **{HEADER_KEY__HTTP_MOCK_RESPONSE_DELAY_KEY: "this-is-invalid"}
        )
        with patch("time.sleep") as sleep_mock:
            _ = self.middleware.process_view(request, None, None, None)
            sleep_mock.assert_not_called()
