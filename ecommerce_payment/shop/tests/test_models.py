from django.test import TestCase
from shop.models import Category, Product
from django.contrib.auth.models import User

class TestCategoriesModel(TestCase):
    # create category 
    def setUp(self):
        self.data1 = Category.objects.create(name='wedding', slug='wedding')

    # test category model created    
    def test_category_model_entry(self):
        data = self.data1 
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        data = self.data1 
        self.assertEqual(str(data), 'wedding')

class TestProductsModel(TestCase):
    def setUp(self):
        Category.objects.create(name='wedding', slug='wedding')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, name='wedding photo', created_by_id=1, 
                                            slug='wedding-photo', price='20.00', image='wedding') 

    def test_product_model_entry(self):
        data=self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'wedding photo')