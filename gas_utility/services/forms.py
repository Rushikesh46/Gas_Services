from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ServiceRequest,Customer
from phonenumber_field.formfields import PhoneNumberField 
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your Email'}))
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your Address'}))
    phone_number = PhoneNumberField(required=True,region="IN", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your phone number'}))

    class Meta:
        model = User
        fields = ['username','email','address','phone_number',  'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        }
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone_number']
            )
        return user
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'details', 'attachment']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ServiceRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'details', 'resolved_at']
        labels = {
            'status': 'Status',
            'resolved_at': 'Resolved At',
        }
        help_texts = {
            'status': 'Update the current status of the request.',
            'resolved_at': 'Specify the date and time when the request was resolved.',
        }
    
    def clean_resolved_at(self):
        status = self.cleaned_data.get('status')
        resolved_at = self.cleaned_data.get('resolved_at')
        if status == 'RESOLVED' and not resolved_at:
            raise forms.ValidationError("Resolved date and time must be provided when status is 'Resolved'.")
        return resolved_at 
        

