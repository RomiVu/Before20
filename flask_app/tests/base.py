import unittest

from application import create_app
from application.models import db
from config import TestingConfig


class BaseTestCase(unittest.TestCase):
    """A base test case."""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()