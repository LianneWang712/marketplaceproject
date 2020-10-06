from django.test import TestCase, Client
from django.urls import reverse
from product.models import User, Product, Cart, InCart
from django.contrib.auth.models import User
from product.views import add_product, my_products


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.products_url = reverse('my_products')
        self.user1 = User.objects.create_user(username='Lianne', email='email123@gmail.com', password='Password123!')
        self.user2 = User.objects.create_user(username='Ruohan', email='email123@gmail.com', password='Password123!')
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart2 = Cart.objects.create(user=self.user2)
        Product.objects.create(name='TestObj1', price=1.99, description='Testing testing', stock=1,
                               seller=self.user1, image='cart.jpg')

    def test_add_products_something(self):
        self.client.login(username='Lianne', password='Password123!')

        response = self.client.post(reverse('add_product'),
                                    {'name': 'TestObj2', 'price': '1.99', 'description': 'A test object',
                                     'stock': '2', 'image': 'cart.jpg'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Product.objects.count(), 2)

    def test_add_products_nothing(self):
        self.client.login(username='Lianne', password='Password123!')

        response = self.client.post(reverse('add_product'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Product.objects.count(), 1)

    def test_add_to_cart_in_stock(self):
        self.client.login(username='Lianne', password='Password123!')
        self.assertEquals(self.cart1.products.count(), 0)
        product1 = Product.objects.create(name='TestObj3', price=1.99, description='Testing testing', stock=1,
                                          seller=self.user1, image='cart.jpg')
        response = self.client.post(reverse('add_to_cart', kwargs={'pid': product1.id}))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.cart1.products.count(), 1)
        self.assertEquals(product1.stock, 1)

    def test_add_to_cart_no_stock(self):
        self.client.login(username='Ruohan', password='Password123!')
        self.assertEquals(self.cart2.products.count(), 0)
        product1 = Product.objects.create(name='TestObj4', price=1.99, description='Testing testing', stock=0,
                                          seller=self.user1, image='cart.jpg')
        response = self.client.post(reverse('add_to_cart', kwargs={'pid': product1.id}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.cart1.products.count(), 0)
        self.assertEquals(product1.stock, 0)
