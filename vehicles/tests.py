from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Vehicle
from .forms import VehicleForm


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
        self.assertContains(response, 'col-md-6 col-lg-4')
        
        # Check that there's no duplicate anchor tags
        content = response.content.decode()
        card_sections = content.split('<div class="card mb-4 hover-shadow">')
        
        # Should have 3 sections: before first card, after first card, after second card
        self.assertEqual(len(card_sections), 3)
        
        # Verify each vehicle card is in its own column
        self.assertContains(response, '<div class="col-md-6 col-lg-4">', count=2)

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

    def test_vehicle_create_view_redirects_get(self):
        """Test that the vehicle create view redirects GET requests since we use modals"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('vehicles:vehicle_add'))
        
        # Should redirect instead of rendering a template
        self.assertEqual(response.status_code, 302)
        
        # Should redirect to vehicle list
        self.assertRedirects(response, reverse('vehicles:vehicle_list'))
