from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ResiBuyer.views import index, order_place, order_view, place_order, checkout, register, view_blockchain, make_invoice
from django.contrib.auth.views import LoginView, LogoutView

# Test Urls resolve
class TestUrls(SimpleTestCase) :
    def test_index_url_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_order_place_url_resolved(self):
        url = reverse('order_place')
        print(resolve(url))
        self.assertEquals(resolve(url).func, order_place)

    def test_order_view_url_resolved(self):
        url = reverse('order_view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, order_view)
    
    def test_place_order_url_resolved(self):
        url = reverse('place_order')
        print(resolve(url))
        self.assertEquals(resolve(url).func, place_order)

    def test_checkout_url_resolved(self):
        url = reverse('checkout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, checkout)

    def test_register_url_resolved(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEquals(resolve(url).func, register)

    def test_checkout_url_resolved(self):
        url = reverse('checkout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, checkout)

    def test_login_url_resolved(self):
        url = reverse('login')
        print(resolve(url).func)
        self.assertEquals(resolve(url).func.view_class, LoginView)
    
    def test_logout_url_resolved(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    # def test_invoice_url_resolved(self):
    #     url = reverse('invoice',args='')
    #     print(resolve(url))
    #     self.assertEquals(resolve(url).func.view_class, make_invoice)

    def test_blockchain_url_resolved(self):
        url = reverse('view_blockchain')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_blockchain)