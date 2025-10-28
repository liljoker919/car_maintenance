from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError
from .models import Vehicle, ServiceRecord
from .forms import VehicleForm, ServiceRecordForm
from datetime import date
from decimal import Decimal


class VehicleListTemplateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.vehicle1 = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Camry',
            year=2020,
            current_mileage=25000
        )
        self.vehicle2 = Vehicle.objects.create(
            user=self.user,
            make='Honda',
            model='Civic',
            year=2019,
            current_mileage=30000
        )

    def test_vehicle_list_grid_layout(self):
        """Test that vehicles are displayed in proper Bootstrap grid layout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_list'))
        
        # Check that the response contains the vehicles
        self.assertContains(response, 'Toyota Camry')
        self.assertContains(response, 'Honda Civic')
        
        # Check for proper Bootstrap grid classes
        self.assertContains(response, 'col-md-6 col-lg-4 mb-3')
        
        # Check that there's no duplicate anchor tags
        content = response.content.decode()
        card_sections = content.split('<div class="card shadow-sm h-100">')
        
        # Should have 3 sections: before first card, after first card, after second card
        self.assertEqual(len(card_sections), 3)
        
        # Verify each vehicle card is in its own column
        self.assertContains(response, '<div class="col-md-6 col-lg-4 mb-3">', count=2)

    def test_vehicle_mileage_display_in_list(self):
        """Test that vehicle mileage is correctly displayed in the vehicle list cards"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_list'))
        
        # Check that actual mileage values are displayed, not "N/A"
        self.assertContains(response, 'Mileage: 25000')
        self.assertContains(response, 'Mileage: 30000')
        
        # Ensure "N/A" is not shown when mileage data exists
        content = response.content.decode()
        self.assertNotIn('Mileage: N/A', content)

    def test_add_vehicle_modal_form_fields_displayed(self):
        """Test that the Add Vehicle modal contains form fields"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_list'))
        
        # Check that form is in context
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], VehicleForm)
        
        # Check that the modal contains form fields
        content = response.content.decode()
        
        # Verify modal exists
        self.assertIn('id="addVehicleModal"', content)
        
        # Check for specific form fields that should be rendered
        self.assertIn('name="make"', content)
        self.assertIn('name="model"', content)
        self.assertIn('name="year"', content)
        self.assertIn('name="current_mileage"', content)
        
        # Check for field labels
        self.assertIn('Make', content)
        self.assertIn('Model', content)
        self.assertIn('Year', content)

    def test_add_vehicle_form_submission(self):
        """Test that vehicle can be added via the modal form"""
        self.client.login(username='testuser', password='testpass123')
        
        # Submit form data to the vehicle_add URL (where modal form posts to)
        form_data = {
            'make': 'Ford',
            'model': 'F-150',
            'year': 2022,
            'current_mileage': 15000,
            'vin': '1FTFW1ET5NFC01234',
            'condition': 'excellent',
            'nickname': 'My Truck'
        }
        
        response = self.client.post(reverse('vehicles:vehicle_add'), data=form_data)
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        
        # Verify vehicle was created
        new_vehicle = Vehicle.objects.filter(make='Ford', model='F-150').first()
        self.assertIsNotNone(new_vehicle)
        self.assertEqual(new_vehicle.user, self.user)
        self.assertEqual(new_vehicle.year, 2022)

    def test_add_vehicle_shows_success_message(self):
        """Test that adding a vehicle shows a success toast message"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'make': 'Ford',
            'model': 'F-150',
            'year': 2022,
            'current_mileage': 15000,
            'vin': '1FTFW1ET5NFC01234',
            'condition': 'excellent',
            'nickname': 'My Truck'
        }
        
        response = self.client.post(reverse('vehicles:vehicle_add'), data=form_data, follow=True)
        
        # Check that success message is present
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Vehicle created successfully.')
        self.assertEqual(messages[0].tags, 'success')

    def test_toast_html_rendered_correctly(self):
        """Test that toast HTML is correctly rendered with proper Bootstrap classes"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'make': 'Ford',
            'model': 'F-150',
            'year': 2022,
            'current_mileage': 15000,
            'vin': '1FTFW1ET5NFC01234',
            'condition': 'excellent',
            'nickname': 'My Truck'
        }
        
        response = self.client.post(reverse('vehicles:vehicle_add'), data=form_data, follow=True)
        content = response.content.decode()
        
        # Check that toast container is present
        self.assertIn('toast-container position-fixed top-0 end-0 p-3', content)
        
        # Check that success toast is rendered with correct classes
        self.assertIn('toast align-items-center text-white bg-success border-0 show', content)
        
        # Check that toast body contains the message
        self.assertIn('Vehicle created successfully.', content)
        
        # Check that close button is present
        self.assertIn('btn-close btn-close-white me-2 m-auto', content)


class VehicleDetailTemplateTest(TestCase):
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
            current_mileage=25000,
            vin='JT2BF28K8X0012345',
            condition='good',
            nickname='My Camry'
        )

    def test_vehicle_detail_page_renders_correctly(self):
        """Test that vehicle detail page renders without URL reverse errors"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_detail', kwargs={'pk': self.vehicle.pk}))
        
        # Should render successfully
        self.assertEqual(response.status_code, 200)
        
        # Should contain vehicle information
        self.assertContains(response, 'Toyota Camry')
        self.assertContains(response, '2020')
        self.assertContains(response, '25000')
        
        # Should contain Edit, Delete, and Back buttons
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')
        self.assertContains(response, 'Back')
        
        # This test will fail before the fix due to NoReverseMatch error
        # for 'vehicle_edit' URL name


class VehicleUpdateViewTest(TestCase):
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
            current_mileage=25000,
            vin='JT2BF28K8X0012345',
            condition='good',
            nickname='My Camry'
        )

    def test_vehicle_update_view_redirects_get(self):
        """Test that the vehicle update view redirects GET requests since we use modals"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_update', kwargs={'pk': self.vehicle.pk}))
        
        # Should redirect instead of rendering a template
        self.assertEqual(response.status_code, 302)
        
        # Should redirect to vehicle list by default
        self.assertRedirects(response, reverse('vehicles:vehicle_list'))

    def test_vehicle_update_view_post_works(self):
        """Test that the vehicle update view handles POST requests properly"""
        self.client.login(username='testuser', password='testpass123')
        
        updated_data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'current_mileage': 30000,
            'vin': 'JT2BF28K8X0012346',
            'condition': 'excellent',
            'nickname': 'My Honda'
        }
        
        response = self.client.post(
            reverse('vehicles:vehicle_update', kwargs={'pk': self.vehicle.pk}), 
            data=updated_data
        )
        
        # Should redirect after successful update
        self.assertEqual(response.status_code, 302)
        
        # Vehicle should be updated
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.make, 'Honda')
        self.assertEqual(self.vehicle.model, 'Civic')
        self.assertEqual(self.vehicle.current_mileage, 30000)

    def test_vehicle_update_shows_success_message(self):
        """Test that updating a vehicle shows a success toast message"""
        self.client.login(username='testuser', password='testpass123')
        
        updated_data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'current_mileage': 30000,
            'vin': 'JT2BF28K8X0012346',
            'condition': 'excellent',
            'nickname': 'My Honda'
        }
        
        response = self.client.post(
            reverse('vehicles:vehicle_update', kwargs={'pk': self.vehicle.pk}), 
            data=updated_data,
            follow=True
        )
        
        # Check that success message is present
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Vehicle updated successfully.')
        self.assertEqual(messages[0].tags, 'success')

    def test_vehicle_delete_shows_success_message(self):
        """Test that deleting a vehicle shows a success toast message"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('vehicles:vehicle_delete', kwargs={'pk': self.vehicle.pk}),
            follow=True
        )
        
        # Check that success message is present
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Vehicle deleted successfully.')
        self.assertEqual(messages[0].tags, 'success')
        
        # Vehicle should be deleted
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle.pk).exists())

    def test_vehicle_create_view_redirects_get(self):
        """Test that the vehicle create view redirects GET requests since we use modals"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_add'))
        
        # Should redirect instead of rendering a template
        self.assertEqual(response.status_code, 302)
        
        # Should redirect to vehicle list
        self.assertRedirects(response, reverse('vehicles:vehicle_list'))


class ServiceRecordViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.vehicle = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Camry',
            year=2020,
            current_mileage=25000,
            vin='JT2BF28K8X0012345',
            condition='good',
            nickname='My Camry'
        )
        self.other_vehicle = Vehicle.objects.create(
            user=self.other_user,
            make='Honda',
            model='Civic',
            year=2019,
            current_mileage=30000
        )
        self.service_record = ServiceRecord.objects.create(
            vehicle=self.vehicle,
            service_type='oil_change',
            date=date.today(),
            mileage=25000,
            cost=Decimal('35.99'),
            notes='Regular oil change'
        )

    def test_service_record_create_requires_login(self):
        """Test that service record creation requires login"""
        response = self.client.get(reverse('vehicles:service_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_service_record_create_success(self):
        """Test successful service record creation"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'vehicle': self.vehicle.id,
            'service_type': 'tire_rotation',
            'date': date.today(),
            'mileage': 25500,
            'cost': '25.00',
            'notes': 'Rotated all four tires'
        }
        
        response = self.client.post(reverse('vehicles:service_add'), data=form_data)
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vehicles:vehicle_detail', kwargs={'pk': self.vehicle.pk}))
        
        # Verify service record was created
        new_record = ServiceRecord.objects.filter(service_type='tire_rotation').first()
        self.assertIsNotNone(new_record)
        self.assertEqual(new_record.vehicle, self.vehicle)
        self.assertEqual(new_record.mileage, 25500)

    def test_service_record_create_prevents_other_users_vehicle(self):
        """Test that users can't add service records to other users' vehicles"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'vehicle': self.other_vehicle.id,  # Try to add to other user's vehicle
            'service_type': 'oil_change',
            'date': date.today(),
            'mileage': 30000,
            'cost': '40.00',
            'notes': 'Unauthorized service'
        }
        
        response = self.client.post(reverse('vehicles:service_add'), data=form_data)
        
        # Should redirect (not create the record)
        self.assertEqual(response.status_code, 302)
        
        # Should not create the service record
        self.assertFalse(ServiceRecord.objects.filter(notes='Unauthorized service').exists())

    def test_service_record_update_requires_ownership(self):
        """Test that users can only edit service records for their own vehicles"""
        # Create service record for other user's vehicle
        other_record = ServiceRecord.objects.create(
            vehicle=self.other_vehicle,
            service_type='brake_service',
            date=date.today(),
            mileage=30000,
            cost=Decimal('150.00'),
            notes='Brake pad replacement'
        )
        
        self.client.login(username='testuser', password='testpass123')
        url = reverse('vehicles:service_update', kwargs={'pk': other_record.pk})
        response = self.client.get(url)
        
        # Should return 404 (record not in queryset for this user)
        self.assertEqual(response.status_code, 404)

    def test_service_record_update_success(self):
        """Test successful service record update"""
        self.client.login(username='testuser', password='testpass123')
        
        updated_data = {
            'vehicle': self.vehicle.id,
            'service_type': 'brake_service',
            'date': date.today(),
            'mileage': 25100,
            'cost': '125.50',
            'notes': 'Updated service notes'
        }
        
        response = self.client.post(
            reverse('vehicles:service_update', kwargs={'pk': self.service_record.pk}), 
            data=updated_data
        )
        
        # Should redirect after successful update
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vehicles:vehicle_detail', kwargs={'pk': self.vehicle.pk}))
        
        # Service record should be updated
        self.service_record.refresh_from_db()
        self.assertEqual(self.service_record.service_type, 'brake_service')
        self.assertEqual(self.service_record.mileage, 25100)
        self.assertEqual(str(self.service_record.cost), '125.50')

    def test_service_record_delete_requires_ownership(self):
        """Test that users can only delete service records for their own vehicles"""
        # Create service record for other user's vehicle
        other_record = ServiceRecord.objects.create(
            vehicle=self.other_vehicle,
            service_type='repair',
            date=date.today(),
            mileage=30000,
            cost=Decimal('500.00'),
            notes='Engine repair'
        )
        
        self.client.login(username='testuser', password='testpass123')
        url = reverse('vehicles:service_delete', kwargs={'pk': other_record.pk})
        response = self.client.get(url)
        
        # Should return 404 (record not in queryset for this user)
        self.assertEqual(response.status_code, 404)

    def test_service_record_delete_success(self):
        """Test successful service record deletion"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('vehicles:service_delete', kwargs={'pk': self.service_record.pk})
        )
        
        # Should redirect after successful deletion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vehicles:vehicle_detail', kwargs={'pk': self.vehicle.pk}))
        
        # Service record should be deleted
        self.assertFalse(ServiceRecord.objects.filter(pk=self.service_record.pk).exists())

    def test_vehicle_detail_shows_service_records(self):
        """Test that vehicle detail page displays service records"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_detail', kwargs={'pk': self.vehicle.pk}))
        
        # Should render successfully
        self.assertEqual(response.status_code, 200)
        
        # Should contain service records section
        self.assertContains(response, 'Service Records')
        self.assertContains(response, 'Add Service Record')
        
        # Should show the existing service record
        self.assertContains(response, 'Oil Change')
        self.assertContains(response, '$35.99')
        self.assertContains(response, 'Regular oil change')

    def test_service_record_form_limits_vehicles_to_user(self):
        """Test that ServiceRecordForm only shows vehicles belonging to the user"""
        form = ServiceRecordForm(user=self.user)
        
        # Should only include the user's vehicles in the queryset
        vehicle_choices = list(form.fields['vehicle'].queryset)
        self.assertIn(self.vehicle, vehicle_choices)
        self.assertNotIn(self.other_vehicle, vehicle_choices)

    def test_service_record_create_shows_success_message(self):
        """Test that creating a service record shows a success toast message"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'vehicle': self.vehicle.id,
            'service_type': 'inspection',
            'date': date.today(),
            'mileage': 25200,
            'cost': '20.00',
            'notes': 'Annual inspection'
        }
        
        response = self.client.post(reverse('vehicles:service_add'), data=form_data, follow=True)
        
        # Check that success message is present
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Service record created successfully.')
        self.assertEqual(messages[0].tags, 'success')

    def test_service_record_update_shows_success_message(self):
        """Test that updating a service record shows a success toast message"""
        self.client.login(username='testuser', password='testpass123')
        
        updated_data = {
            'vehicle': self.vehicle.id,
            'service_type': 'tune_up',
            'date': date.today(),
            'mileage': 25300,
            'cost': '150.00',
            'notes': 'Full tune-up service'
        }
        
        response = self.client.post(
            reverse('vehicles:service_update', kwargs={'pk': self.service_record.pk}), 
            data=updated_data,
            follow=True
        )
        
        # Check that success message is present
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Service record updated successfully.')
        self.assertEqual(messages[0].tags, 'success')

    def test_service_record_delete_shows_success_message(self):
        """Test that deleting a service record shows a success toast message"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('vehicles:service_delete', kwargs={'pk': self.service_record.pk}),
            follow=True
        )
        
        # Check that success message is present
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Service record deleted successfully.')
        self.assertEqual(messages[0].tags, 'success')


class VehicleUniqueVINTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

    def test_duplicate_vin_raises_integrity_error(self):
        """Test that creating vehicles with duplicate VINs raises IntegrityError"""
        # Create first vehicle with a VIN
        vehicle1 = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Camry',
            year=2020,
            current_mileage=25000,
            vin='JT2BF28K8X0012345'
        )
        
        # Attempt to create second vehicle with the same VIN should raise error
        with self.assertRaises(IntegrityError):
            Vehicle.objects.create(
                user=self.other_user,
                make='Honda',
                model='Civic',
                year=2019,
                current_mileage=30000,
                vin='JT2BF28K8X0012345'  # Same VIN as vehicle1
            )

    def test_null_vins_are_allowed(self):
        """Test that multiple vehicles can have null VINs"""
        # Create first vehicle without a VIN
        vehicle1 = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Camry',
            year=2020,
            current_mileage=25000,
            vin=None
        )
        
        # Create second vehicle without a VIN should succeed
        vehicle2 = Vehicle.objects.create(
            user=self.user,
            make='Honda',
            model='Civic',
            year=2019,
            current_mileage=30000,
            vin=None
        )
        
        # Both vehicles should exist
        self.assertIsNotNone(vehicle1.pk)
        self.assertIsNotNone(vehicle2.pk)

    def test_unique_vins_are_allowed(self):
        """Test that vehicles with different VINs can be created"""
        # Create first vehicle with a VIN
        vehicle1 = Vehicle.objects.create(
            user=self.user,
            make='Toyota',
            model='Camry',
            year=2020,
            current_mileage=25000,
            vin='JT2BF28K8X0012345'
        )
        
        # Create second vehicle with a different VIN should succeed
        vehicle2 = Vehicle.objects.create(
            user=self.other_user,
            make='Honda',
            model='Civic',
            year=2019,
            current_mileage=30000,
            vin='1HGBH41JXMN109186'
        )
        
        # Both vehicles should exist
        self.assertIsNotNone(vehicle1.pk)
        self.assertIsNotNone(vehicle2.pk)
