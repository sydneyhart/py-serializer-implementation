# Serializer Implementation

**Please note:** read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md)
before start.

In this task, you should implement the `CarSerializer` serializer for the `Car` model in `serializers.py`.

The `Car` model has the following fields:
- manufacturer (with the `max_length` of 64);
- model (with the `max_length` of 64);
- horse_powers (with the minimum and maximum validators);
- is_broken;
- problem_description (can be `null`).

Serializer should be created using **serializers.Serializer**.

Also, you should implement 2 functions that use the `CarSerializer` in `main.py`:
- `serialize_car_object`, that accepts the `Car` object and returns `json` with its data;
- `deserialize_car_object`, that accepts `json` and returns the `Car` instance.

## Run and verify

Use Python 3.10 or 3.11 with the repository's pinned dependencies:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
flake8
```

`serialize_car_object` renders a car as JSON bytes. `deserialize_car_object`
parses JSON bytes, validates the fields, and saves and returns a new Car.
Invalid data raises DRF ValidationError; malformed JSON raises ParseError.
IDs are read-only. Horse power must be between 1 and 1914 inclusive;
problem_description can be omitted, null, or blank.

The test suite includes the seven supplied tests and eight additional tests for
validation boundaries, optional descriptions, required fields, updates,
round-trip persistence, invalid input, and read-only IDs.
