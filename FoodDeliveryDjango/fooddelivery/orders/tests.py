from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, OrderItem
from restaurants.models import Restaurant, Category, MenuItem
from decimal import Decimal

class OrdersTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
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
            name='Pizza'
        )
        
        # Create a menu item
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name='Margherita Pizza',
            description='Classic cheese and tomato pizza',
            price=12.99,
            is_available=True
        )
        
        # Create a client for testing
        self.client = Client()
        
    def test_add_to_cart(self):
        """Test adding an item to the cart"""
        # Login
        self.client.login(username='testuser', password='testpassword123')
        
        # Add item to cart
        response = self.client.post(reverse('add_to_cart'), {
            'menu_item_id': self.menu_item.id,
            'quantity': 2
        })
        
        # Check for successful redirect
        self.assertEqual(response.status_code, 302)
        
        # Check if the item was added to the session cart
        session = self.client.session
        cart = session.get('cart', {})
        
        self.assertIn(str(self.menu_item.id), cart)
        self.assertEqual(cart[str(self.menu_item.id)]['quantity'], 2)
        
    def test_cart_view(self):
        """Test the cart view"""
        # Login
        self.client.login(username='testuser', password='testpassword123')
        
        # Set up cart in session
        session = self.client.session
        session['cart'] = {
            str(self.menu_item.id): {
                'quantity': 2,
                'price': str(self.menu_item.price)
            }
        }
        session.save()
        
        # Get cart page
        response = self.client.get(reverse('cart'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Margherita Pizza')
        self.assertContains(response, '2')  # Quantity
        
    def test_checkout_process(self):
        """Test the entire checkout process"""
        # Login
        self.client.login(username='testuser', password='testpassword123')
        
        # Set up cart in session
        session = self.client.session
        session['cart'] = {
            str(self.menu_item.id): {
                'quantity': 2,
                'price': str(self.menu_item.price)
            }
        }
        session.save()
        
        # Get checkout page
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        
        # Submit checkout form
        checkout_data = {
            'delivery_address': '456 Delivery St, Test City, TS 67890',
            'contact_phone': '987-654-3210',
            'payment_method': 'cash',
            'delivery_instructions': 'Leave at the door'
        }
        
        response = self.client.post(reverse('checkout'), checkout_data)
        
        # Check if order was created
        self.assertEqual(Order.objects.count(), 1)
        
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.restaurant, self.restaurant)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.delivery_address, checkout_data['delivery_address'])
        self.assertEqual(order.contact_phone, checkout_data['contact_phone'])
        self.assertEqual(order.payment_method, checkout_data['payment_method'])
        self.assertEqual(order.delivery_instructions, checkout_data['delivery_instructions'])
        
        # Check order items
        self.assertEqual(order.items.count(), 1)
        order_item = order.items.first()
        self.assertEqual(order_item.menu_item, self.menu_item)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, self.menu_item.price)
        
        # Check total amount
        expected_total = Decimal('25.98')  # 12.99 * 2
        self.assertEqual(order.total_amount, expected_total)
        
        # Check cart is cleared after checkout
        self.assertNotIn('cart', self.client.session)
