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

Then apply the drfmockresponse models:
```python
python manage.py migrate
```

## Usage
TODO

## Development
TODO

## License
MIT licensed. See the bundled LICENSE file for more details.
