from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Vehicle


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
