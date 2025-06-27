from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Address

class AccountsTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create a profile (should be created automatically by signal)
        self.profile = UserProfile.objects.get(user=self.user)
        
        # Create an address for the user
        self.address = Address.objects.create(
            user_profile=self.profile,
            address_line1='123 Test Street',
            city='Test City',
            state='Test State',
            postal_code='12345',
            is_default=True
        )
        
        # Set up client
        self.client = Client()
        
    def test_profile_created_automatically(self):
        """Test that UserProfile is created automatically when User is created"""
        self.assertIsNotNone(self.profile)
        
    def test_login_view(self):
        """Test login view"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        # Test successful login
        login_successful = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_successful)
        
    def test_register_view(self):
        """Test register view and functionality"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        
        # Test user registration
        new_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(reverse('register'), new_user_data)
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
    def test_profile_view(self):
        """Test profile view with authenticated user"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
