from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, TextInput
from .models import Advertisement, User


class AdvertisementFrom(ModelForm):
	class Meta:
		model = Advertisement
		fields = ['header', 'descriptions', 'price', 'sity', 'site', 'category', 'autor', 'phone']


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'email']


class ChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'img']

		widgets = {
			'username': TextInput(attrs={'placeholder': "Username"}),
			'first_name': TextInput(attrs={'placeholder': 'First name'}),
			'last_name': TextInput(attrs={'placeholder': 'Last name'}),
			'email': TextInput(attrs={'placeholder': 'Email'}),
			}