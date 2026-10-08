#uses temporary in memory database for test
import sys
import unittest

from flask import Flask

from app import db
from app import models  
from app.services import trip_service, traveler_service
from app.validators.errors import ValidationError, ConflictError


class ServiceTests(unittest.TestCase):

    def setUp(self):
        # small throwaway app with an empty in-memory database for every test
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        db.init_app(self.app)
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    # helper functions 
    def make_trip(self, **changes):
        data = {
            "destination": "Cox's Bazar",
            "start_date": "2026-10-20",
            "end_date": "2026-10-23",
            "budget": 30000,
            "max_travelers": 2,
        }
        data.update(changes)
        return trip_service.create_trip(data)
    
    def person(self, email):
        return {"name": "Test Person", "email": email}




    # ######################## TESTS #######################################

    #unit test for create trip
    def test_create_trip_starts_planned_and_rejects_bad_dates(self):
        trip = self.make_trip()
        self.assertEqual(trip.status, "PLANNED")

        with self.assertRaises(ValidationError):
            self.make_trip(start_date="2026-10-23", end_date="2026-10-20")

    #ubit check for duplicate traveler add

    def test_traveler_cannot_join_twice_or_beyond_capacity(self):
        trip = self.make_trip(max_travelers=2)
        traveler_service.add_traveler(trip.id, self.person("sakibshehan@example.com"))

        # same email, different letter case, is still a duplicate
        with self.assertRaises(ConflictError) as error:
            traveler_service.add_traveler(trip.id, self.person("SAKIBSHEHAN@example.com"))
        self.assertEqual(error.exception.code, "DUPLICATE_TRAVELER")

        # the second seat is full, the third is not
        traveler_service.add_traveler(trip.id, self.person("rahim@example.com"))
        with self.assertRaises(ConflictError) as error:
            traveler_service.add_traveler(trip.id, self.person("karim@example.com"))
        self.assertEqual(error.exception.code, "TRIP_FULL")


class Result(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.passed = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed.append(test)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ServiceTests)
    result = Result()
    suite.run(result)

    total = result.testsRun
    bad = len(result.failures) + len(result.errors)

    # first line: the overall result
    print("PASSED" if bad == 0 else "FAILED", f"- {total - bad} of {total} tests passed")
    print()
    for test in result.passed:
        print("  PASS ", test._testMethodName)
    for test, trace in result.failures + result.errors:
        print("  FAIL ", test._testMethodName)
        print("       ", trace.strip().splitlines()[-1])
    sys.exit(1 if bad else 0)