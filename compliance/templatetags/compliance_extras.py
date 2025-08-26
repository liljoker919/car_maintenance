import json
from django import template
from compliance.models import CarRegistration

register = template.Library()


@register.simple_tag
def get_field_errors(errors_json, field_name):
    """Extract errors for a specific field from JSON error string"""
    if not errors_json:
        return []
    try:
        errors_dict = json.loads(errors_json)
        return errors_dict.get(field_name, [])
    except (json.JSONDecodeError, TypeError):
        return []


@register.simple_tag  
def get_current_value(form_data, form_id, registration_id, field_name, default_value):
    """Get current value for a field, preferring form_data if available"""
    if form_data and form_id == registration_id:
        return form_data.get(field_name, default_value)
    return default_value


@register.simple_tag
def get_state_choices():
    """Get state choices from the model"""
    return CarRegistration.STATE_CHOICES