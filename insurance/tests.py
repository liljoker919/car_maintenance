from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError
from vehicles.models import Vehicle
from .models import InsurancePolicy
from .forms import InsurancePolicyForm
import datetime


class InsuranceCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.vehicle = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Camry',
            year=2020,
            current_mileage=25000
        )

    def test_insurance_create_assigns_user(self):
        """Test that creating an insurance policy assigns the logged-in user"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'vehicle': self.vehicle.id,
            'provider': 'State Farm',
            'policy_number': 'SF123456789',
            'coverage_start': datetime.date.today(),
            'coverage_end': datetime.date.today() + datetime.timedelta(days=365),
            'premium': '1200.00'
        }
        
        response = self.client.post(reverse('insurance:insurance_add'), data=form_data)
        
        # Should not get IntegrityError and should create the policy
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        
        # Verify the insurance policy was created with the correct user
        policy = InsurancePolicy.objects.filter(policy_number='SF123456789').first()
        self.assertIsNotNone(policy)
        self.assertEqual(policy.user, self.user)
        self.assertEqual(policy.vehicle, self.vehicle)

    def test_insurance_create_without_login_redirects(self):
        """Test that accessing insurance create without login redirects to login"""
        form_data = {
            'vehicle': self.vehicle.id,
            'provider': 'State Farm',
            'policy_number': 'SF123456789',
            'coverage_start': datetime.date.today(),
            'coverage_end': datetime.date.today() + datetime.timedelta(days=365),
            'premium': '1200.00'
        }
        
        response = self.client.post(reverse('insurance:insurance_add'), data=form_data)
        
        # Should redirect to login (not authenticated)
        self.assertEqual(response.status_code, 302)
        
        # Should not create any insurance policy
        policy = InsurancePolicy.objects.filter(policy_number='SF123456789').first()
        self.assertIsNone(policy)
