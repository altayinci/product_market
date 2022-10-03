import unittest
import json
from django.test import Client
from rest_framework.test import RequestsClient
from market import settings
from model_bakery import baker
from urllib.parse import urljoin
from .models import Product


class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.product = baker.make(Product, price=22, currency="USD")

    def test_get_products(self):
        # Given
        client = RequestsClient()
        url = urljoin(settings.HOST_URL, 'api/products')

        # When
        response = client.get(url)

        # Then
        self.assertEqual(response.status_code, 200)

    def test_get_product(self):
        # Given
        product_id = self.product.id
        client = RequestsClient()

        # When
        url = urljoin(settings.HOST_URL, 'api/products')
        url = f"{url}/{product_id}"
        response = client.get(url)
        data = response.json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data["price"])
        self.assertIsNotNone(data["last_updated_on"])
        self.assertIsNotNone(data["currency"])

    def test_update_product(self):
        # Given
        product_id = self.product.id
        client = Client()

        # When
        url = urljoin(settings.HOST_URL, 'api/products')
        url = f"{url}/{product_id}/"
        data = {"description": "Electronical devices"}
        response = client.put(url, data=json.dumps(data), content_type='application/json')
        self.product.refresh_from_db()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(self.product.description, "Electronical devices")

    def test_delete_product(self):
        # Given
        product_id = self.product.id
        client = Client()

        # When
        url = urljoin(settings.HOST_URL, 'api/products')
        url = f"{url}/{product_id}/"
        response = client.delete(url)

        # Then
        self.assertEqual(response.status_code, 204)
