import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_prosperity_index.settings')
django.setup()
from ddf import G
from .models import YearIndexTable


from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class APITests(TestCase):
    @patch('requests.get')

    def test_get_index_Api(self, mock_get):
        years = ["2014", "2015", "2016", "2017"]
        for year in years:
            G(YearIndexTable, year=year)
        url = reverse("get_final_index")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
