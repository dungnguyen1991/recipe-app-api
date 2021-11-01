from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg20pError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.core.management.base.BaseCommand.check') as ch:
            ch.return_value = True
            call_command('wait_for_db')
            self.assertEqual(ch.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.core.management.base.BaseCommand.check') as ch:
            ch.side_effect = ([OperationalError] * 5 +
                              [Psycopg20pError]*2 +
                              [True])
            call_command('wait_for_db')
            self.assertEqual(ch.call_count, 8)
