from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")  # Redirect to login page after registration
    template_name = "registration/register.html"


from django.shortcuts import render

# Create your views here.
