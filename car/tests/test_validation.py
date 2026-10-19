from django.test import TestCase
from rest_framework.exceptions import ParseError, ValidationError

from car.models import Car
from car.serializers import CarSerializer
from main import deserialize_car_object, serialize_car_object


class CarValidationTests(TestCase):
    def setUp(self):
        self.payload = {
            "manufacturer": "Audi",
            "model": "A4",
            "horse_powers": 200,
            "is_broken": False,
        }

    def test_horse_power_boundaries(self):
        for value in (1, 1914):
            with self.subTest(value=value):
                serializer = CarSerializer(
                    data={**self.payload, "horse_powers": value}
                )
                self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_optional_description_values(self):
        for value in (None, "", "Needs new tires"):
            with self.subTest(value=value):
                serializer = CarSerializer(
                    data={**self.payload, "problem_description": value}
                )
                serializer.is_valid(raise_exception=True)
                car = serializer.save()
                car.refresh_from_db()
                self.assertEqual(car.problem_description, value)

    def test_required_fields(self):
        for field in self.payload:
            with self.subTest(field=field):
                data = self.payload.copy()
                data.pop(field)
                serializer = CarSerializer(data=data)
                self.assertFalse(serializer.is_valid())
                self.assertIn(field, serializer.errors)

    def test_update_persists_and_retains_omitted_fields(self):
        car = Car.objects.create(**self.payload)
        serializer = CarSerializer(
            car, data={"is_broken": True}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        updated.refresh_from_db()
        self.assertEqual(updated.pk, car.pk)
        self.assertTrue(updated.is_broken)
        self.assertEqual(updated.manufacturer, "Audi")
        self.assertEqual(Car.objects.count(), 1)

    def test_deserialization_round_trip(self):
        car = Car(**self.payload, problem_description=None)
        restored = deserialize_car_object(serialize_car_object(car))
        self.assertIsNotNone(restored.pk)
        self.assertTrue(Car.objects.filter(pk=restored.pk).exists())
        for field, value in self.payload.items():
            self.assertEqual(getattr(restored, field), value)
        self.assertIsNone(restored.problem_description)

    def test_invalid_json_data_does_not_create_a_car(self):
        with self.assertRaises(ValidationError):
            deserialize_car_object(b'{"horse_powers":0}')
        self.assertEqual(Car.objects.count(), 0)

    def test_malformed_json_raises_parse_error(self):
        with self.assertRaises(ParseError):
            deserialize_car_object(b"{invalid")
        self.assertEqual(Car.objects.count(), 0)

    def test_primary_key_is_read_only(self):
        serializer = CarSerializer(data={"id": 999, **self.payload})
        serializer.is_valid(raise_exception=True)
        car = serializer.save()
        self.assertNotEqual(car.pk, 999)
