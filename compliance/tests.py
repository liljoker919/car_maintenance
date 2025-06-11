from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from vehicles.models import Vehicle
from .models import CarRegistration


class CarRegistrationModelTest(TestCase):
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

    def test_car_registration_creation(self):
        """Test that a CarRegistration can be created with all required fields"""
        registration = CarRegistration.objects.create(
            vehicle=self.vehicle,
            registration_number='ABC123',
            state='NC',
            registration_date=date.today(),
            expiration_date=date.today() + timedelta(days=365)
        )
        
        self.assertEqual(registration.vehicle, self.vehicle)
        self.assertEqual(registration.registration_number, 'ABC123')
        self.assertEqual(registration.state, 'NC')
        self.assertEqual(registration.registration_date, date.today())
        self.assertEqual(registration.expiration_date, date.today() + timedelta(days=365))
        self.assertIsNotNone(registration.created_at)
        self.assertIsNotNone(registration.updated_at)

    def test_car_registration_with_optional_fields(self):
        """Test that a CarRegistration can be created with optional fields"""
        inspection_due = date.today() + timedelta(days=180)
        inspection_completed = date.today() - timedelta(days=30)
        
        registration = CarRegistration.objects.create(
            vehicle=self.vehicle,
            registration_number='XYZ789',
            state='CA',
            registration_date=date.today(),
            expiration_date=date.today() + timedelta(days=365),
            inspection_due_date=inspection_due,
            inspection_completed_date=inspection_completed,
            notes='Annual inspection completed'
        )
        
        self.assertEqual(registration.inspection_due_date, inspection_due)
        self.assertEqual(registration.inspection_completed_date, inspection_completed)
        self.assertEqual(registration.notes, 'Annual inspection completed')

    def test_car_registration_str_method(self):
        """Test the string representation of CarRegistration"""
        registration = CarRegistration.objects.create(
            vehicle=self.vehicle,
            registration_number='TEST123',
            state='NY',
            registration_date=date.today(),
            expiration_date=date.today() + timedelta(days=365)
        )
        
        expected_str = f"{self.vehicle} - NY TEST123"
        self.assertEqual(str(registration), expected_str)

    def test_car_registration_state_choices(self):
        """Test that state field accepts valid state codes"""
        valid_states = ['NC', 'CA', 'NY', 'TX', 'FL']
        
        for state in valid_states:
            registration = CarRegistration(
                vehicle=self.vehicle,
                registration_number=f'TEST{state}',
                state=state,
                registration_date=date.today(),
                expiration_date=date.today() + timedelta(days=365)
            )
            # This should not raise a validation error
            registration.full_clean()

    def test_car_registration_ordering(self):
        """Test that CarRegistrations are ordered by expiration_date desc, then vehicle"""
        # Create registrations with different expiration dates
        reg1 = CarRegistration.objects.create(
            vehicle=self.vehicle,
            registration_number='FIRST',
            state='NC',
            registration_date=date.today(),
            expiration_date=date.today() + timedelta(days=30)  # Expires first
        )
        
        reg2 = CarRegistration.objects.create(
            vehicle=self.vehicle,
            registration_number='SECOND',
            state='NC',
            registration_date=date.today(),
            expiration_date=date.today() + timedelta(days=365)  # Expires later
        )
        
        registrations = list(CarRegistration.objects.all())
        # Should be ordered by expiration_date descending (latest first)
        self.assertEqual(registrations[0], reg2)
        self.assertEqual(registrations[1], reg1)

    def test_car_registration_related_name(self):
        """Test that the related_name 'car_registrations' works correctly"""
        registration = CarRegistration.objects.create(
            vehicle=self.vehicle,
            registration_number='RELATED',
            state='NC',
            registration_date=date.today(),
            expiration_date=date.today() + timedelta(days=365)
        )
        
        # Test the reverse relationship
        vehicle_registrations = self.vehicle.car_registrations.all()
        self.assertEqual(vehicle_registrations.count(), 1)
        self.assertEqual(vehicle_registrations.first(), registration)

    def test_car_registration_cascade_delete(self):
        """Test that CarRegistration is deleted when Vehicle is deleted"""
        registration = CarRegistration.objects.create(
            vehicle=self.vehicle,
            registration_number='CASCADE',
            state='NC',
            registration_date=date.today(),
            expiration_date=date.today() + timedelta(days=365)
        )
        
        registration_id = registration.id
        self.vehicle.delete()
        
        # Registration should be deleted due to CASCADE
        with self.assertRaises(CarRegistration.DoesNotExist):
            CarRegistration.objects.get(id=registration_id)
