from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from ResiBuyer.models import Product, Order, Information
import json

class TestViews(TestCase):

    #def setUp(self):

    def test_index(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEquals(response.status_code,302)

    def test_order_place(self):
        client = Client()
        response = client.get(reverse('order_place'))
        self.assertEquals(response.status_code,302)

    def test_order_view(self):
        client = Client()
        response = client.get(reverse('order_view'))
        self.assertEquals(response.status_code,302)
    
    def test_checkout(self):
        client = Client()
        response = client.get(reverse('checkout'))
        self.assertEquals(response.status_code,302)
    
    def test_register_GET(self):
        client = Client()
        response = client.get(reverse('register'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'UI/authentication_page/register.html')

    def test_place_order_GET(self):
        client = Client()
        response = client.get(reverse('place_order'))
        self.assertEquals(response.status_code,404)

    # def test_make_invoice(self):
    #     client = Client()
    #     response = client.get(reverse('invoice'))
    #     self.assertEquals(response.status_code,302)


    # def test_register_POST_new_user(self):
    #    response = self.client.post(reverse('register'),{self.user},format='text/html')
    #    self.assertEquals(response.status_code,302)
    
