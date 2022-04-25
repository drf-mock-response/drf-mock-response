<a href="https://github.com/drf-mock-response/drf-mock-response/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/drf-mock-response/drf-mock-response"></a>
<a href="https://pypi.org/project/drfmockresponse/"><img alt="PyPI" src="https://img.shields.io/pypi/v/drfmockresponse"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

# drf-mock-response
**drf-mock-response** is a DRF middleware that can mock REST API responses. It can be used to
simulate various common or uncommon scenarios.

## Installation
```bash
$ pip install drfmockresponse
```

Add ```drfmockresponse.apps.DrfmockresponseConfig``` to your ```INSTALLED_APPS```.
```python
INSTALLED_APPS = [
    ...,
    'drfmockresponse.apps.DrfmockresponseConfig',
    ...,
]
```

Add ```djangomockresponse.middleware.MockResponseMiddleware``` to your ```MIDDLEWARE```.
```python
MIDDLEWARE = (
    ...,
    'drfmockresponse.middleware.MockResponseMiddleware',
    ...,
)
```

Then apply the drf-mock-response models:
```python
python manage.py migrate
```

## Usage
Assume the following API that returns a random integer [0 - 100],
every time it is called:

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import routers
from django.urls import path
from django.contrib import admin
import random


class Random0to100ViewSet(GenericViewSet):
    def list(self, request):
        return Response(random.randint(0, 100))


router = routers.DefaultRouter()
router.register("random0to100", Random0to100ViewSet, basename="random0to100")


urlpatterns = router.urls
urlpatterns += [
    path("admin/", admin.site.urls),
]
```

### Normal URI response
The URI returns a random integer [0-100] every time it is called (54 in this case).
![Normal URI response](https://raw.githubusercontent.com/drf-mock-response/drf-mockup-response-static/main/case_1_normal_response.png)

### Custom mock response
Let's assume that there is a need to make the URI to return a specific number, for example 88. The first step is to 
create a MockResponse object via the Admin panel:
![Custom mock response](https://raw.githubusercontent.com/drf-mock-response/drf-mockup-response-static/main/mock_88_create.png)

The Content, Status, and Content-Type of the request can be mocked. The Content-Types that are currently supported are:

- text/plain
- application/json (Specified Content must be JSON serializable!)

The name of the MockResponse in this example is "mock-return-88". This name can then be specified as a
*Mock-Response-ID* request header:
![Custom mock response](https://raw.githubusercontent.com/drf-mock-response/drf-mockup-response-static/main/case_2_custom_mock.png)

The URI returned the mocked value 88.

### Default HTTP Status mock response
For convenience any standard HTTP Status can be used as a *Mock-Response-ID*. However, it is not possible to specify a 
response Content, therefore this feature is useful when only the response Status is important.
![Response with delay](https://raw.githubusercontent.com/drf-mock-response/drf-mockup-response-static/main/case_4_default_http_status.png)

The HTTP Status Codes that are supported are:
- 100: CONTINUE
- 101: SWITCHING PROTOCOLS
- 200: OK
- 201: CREATED
- 202: ACCEPTED
- 203: NON AUTHORITATIVE INFORMATION
- 204: NO CONTENT
- 205: RESET CONTENT
- 206: PARTIAL CONTENT
- 207: MULTI STATUS
- 208: ALREADY REPORTED
- 226: IM USED
- 300: MULTIPLE CHOICES
- 301: MOVED PERMANENTLY
- 302: FOUND
- 303: SEE OTHER
- 304: NOT MODIFIED
- 305: USE PROXY
- 306: RESERVED
- 307: TEMPORARY REDIRECT
- 308: PERMANENT REDIRECT
- 400: BAD REQUEST
- 401: UNAUTHORIZED
- 402: PAYMENT REQUIRED
- 403: FORBIDDEN
- 404: NOT FOUND
- 405: METHOD NOT ALLOWED
- 406: NOT ACCEPTABLE
- 407: PROXY AUTHENTICATION REQUIRED
- 408: REQUEST TIMEOUT
- 409: CONFLICT
- 410: GONE
- 411: LENGTH REQUIRED
- 412: PRECONDITION FAILED
- 413: REQUEST ENTITY TOO LARGE
- 414: REQUEST URI TOO LONG
- 415: UNSUPPORTED MEDIA TYPE
- 416: REQUESTED RANGE NOT SATISFIABLE
- 417: EXPECTATION FAILED
- 418: IM A TEAPOT
- 422: UNPROCESSABLE ENTITY
- 423: LOCKED
- 424: FAILED DEPENDENCY
- 426: UPGRADE REQUIRED
- 428: PRECONDITION REQUIRED
- 429: TOO MANY REQUESTS
- 431: REQUEST HEADER FIELDS TOO LARGE
- 451: UNAVAILABLE FOR LEGAL REASONS
- 500: INTERNAL SERVER ERROR
- 501: NOT IMPLEMENTED
- 502: BAD GATEWAY
- 503: SERVICE UNAVAILABLE
- 504: GATEWAY TIMEOUT
- 505: HTTP VERSION NOT SUPPORTED
- 506: VARIANT ALSO NEGOTIATES
- 507: INSUFFICIENT STORAGE
- 508: LOOP DETECTED
- 509: BANDWIDTH LIMIT EXCEEDED
- 510: NOT EXTENDED
- 511: NETWORK AUTHENTICATION REQUIRED

### Response delay
A delay (in seconds) may be specified for normal or mock responses by specifying the *Mock-Response-Delay* header. Keep 
in mind that a specified delay is added to any processing / IO times, so resulting delays will always be bigger than the specified value (eg. 3.83 instead of specified 3.8).
![Response with delay](https://raw.githubusercontent.com/drf-mock-response/drf-mockup-response-static/main/case_3_custom_mock_and_delay.png)

## Development
TODO

## License
MIT licensed. See the bundled LICENSE file for more details.
