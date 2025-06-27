from django.test import TestCase
from django.urls import reverse
from .models import Restaurant, Category, MenuItem

class RestaurantTests(TestCase):
    
    def setUp(self):
        # Create a test restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine_type='Italian',
            address='123 Test Street',
            city='Test City',
            state='Test State',
            postal_code='12345',
            phone='123-456-7890',
            opening_time='09:00:00',
            closing_time='22:00:00',
            delivery_fee=2.99,
            minimum_order=10.00
        )
        
        # Create a category
        self.category = Category.objects.create(
            restaurant=self.restaurant,
            name='Pasta'
        )
        
        # Create menu items
        self.menu_item1 = MenuItem.objects.create(
            category=self.category,
            name='Spaghetti Carbonara',
            description='Classic Italian pasta dish with eggs, cheese, and bacon',
            price=12.99,
            is_available=True
        )
        
        self.menu_item2 = MenuItem.objects.create(
            category=self.category,
            name='Fettuccine Alfredo',
            description='Fettuccine tossed with Parmesan cheese and butter',
            price=14.99,
            is_vegetarian=True,
            is_available=True
        )
    
    def test_restaurant_list_view(self):
        """Test the restaurant list view"""
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
        self.assertContains(response, 'Italian')
    
    def test_restaurant_detail_view(self):
        """Test the restaurant detail view"""
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
        self.assertContains(response, 'Spaghetti Carbonara')
        self.assertContains(response, 'Fettuccine Alfredo')
    
    def test_restaurant_search(self):
        """Test restaurant search functionality"""
        # Search by name
        response = self.client.get(reverse('restaurant_list'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
        
        # Search by cuisine type
        response = self.client.get(reverse('restaurant_list'), {'q': 'Italian'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
        
        # Search with no results
        response = self.client.get(reverse('restaurant_list'), {'q': 'NonExistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Restaurant')
        self.assertContains(response, 'No restaurants found')
