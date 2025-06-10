from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date
from .models import Vehicle, Insurance


class InsuranceModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test vehicle
        self.vehicle = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Camry',
            year=2020,
            current_mileage=50000,
            condition='good'
        )

    def test_insurance_creation(self):
        """Test that an Insurance object can be created with all required fields"""
        insurance = Insurance.objects.create(
            provider='State Farm',
            renewal_date=date(2024, 12, 31),
            cost=Decimal('1200.50'),
            policy_number='SF123456789',
            vehicle=self.vehicle
        )
        
        self.assertEqual(insurance.provider, 'State Farm')
        self.assertEqual(insurance.renewal_date, date(2024, 12, 31))
        self.assertEqual(insurance.cost, Decimal('1200.50'))
        self.assertEqual(insurance.policy_number, 'SF123456789')
        self.assertEqual(insurance.vehicle, self.vehicle)
        self.assertIsNotNone(insurance.created_at)
        self.assertIsNotNone(insurance.updated_at)

    def test_insurance_str_representation(self):
        """Test the string representation of Insurance model"""
        insurance = Insurance.objects.create(
            provider='Geico',
            renewal_date=date(2024, 6, 15),
            cost=Decimal('950.00'),
            policy_number='GC987654321',
            vehicle=self.vehicle
        )
        
        expected_str = f"Geico - GC987654321 ({self.vehicle})"
        self.assertEqual(str(insurance), expected_str)

    def test_vehicle_insurance_relationship(self):
        """Test that vehicle can have multiple insurances and the relationship works"""
        insurance1 = Insurance.objects.create(
            provider='AllState',
            renewal_date=date(2024, 3, 15),
            cost=Decimal('1100.00'),
            policy_number='AS111111111',
            vehicle=self.vehicle
        )
        
        insurance2 = Insurance.objects.create(
            provider='Progressive',
            renewal_date=date(2024, 9, 20),
            cost=Decimal('950.00'),
            policy_number='PR222222222',
            vehicle=self.vehicle
        )
        
        # Test that vehicle has insurances
        vehicle_insurances = self.vehicle.insurances.all()
        self.assertEqual(vehicle_insurances.count(), 2)
        self.assertIn(insurance1, vehicle_insurances)
        self.assertIn(insurance2, vehicle_insurances)

    def test_insurance_ordering(self):
        """Test that insurances are ordered by renewal_date in descending order"""
        insurance1 = Insurance.objects.create(
            provider='Provider1',
            renewal_date=date(2024, 1, 15),
            cost=Decimal('1000.00'),
            policy_number='P1111111111',
            vehicle=self.vehicle
        )
        
        insurance2 = Insurance.objects.create(
            provider='Provider2',
            renewal_date=date(2024, 12, 15),
            cost=Decimal('1200.00'),
            policy_number='P2222222222',
            vehicle=self.vehicle
        )
        
        insurance3 = Insurance.objects.create(
            provider='Provider3',
            renewal_date=date(2024, 6, 15),
            cost=Decimal('1100.00'),
            policy_number='P3333333333',
            vehicle=self.vehicle
        )
        
        insurances = Insurance.objects.all()
        self.assertEqual(insurances[0], insurance2)  # Latest renewal_date first
        self.assertEqual(insurances[1], insurance3)  # Middle renewal_date second
        self.assertEqual(insurances[2], insurance1)  # Earliest renewal_date last
