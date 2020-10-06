from django import forms
from .models import Address


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(min_length=6)
    password_confirm = forms.CharField()

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'line1', 'line2', 'city', 'province', 'country', 'postal_code']
