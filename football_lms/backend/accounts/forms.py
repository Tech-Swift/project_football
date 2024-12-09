from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        help_text="Your password must be at least 8 characters long.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
    )
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('coach', 'Coach'),
        ('staff', 'Staff'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.Select)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    # Override the save method to hash the password
    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password before saving
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        # Ensure both fields are filled out
        if not username_or_email or not password:
            raise ValidationError('Both username/email and password are required.')

        # Try to find the user by username or email
        user = None
        if '@' in username_or_email:
            # If it looks like an email, search by email
            user = CustomUser.objects.filter(email=username_or_email).first()
        else:
            # Otherwise, search by username
            user = CustomUser.objects.filter(username=username_or_email).first()

        if not user:
            raise ValidationError('No user found with this username/email.')

        # Check if the password is correct
        if not user.check_password(password):
            raise ValidationError('Incorrect password. Please try again.')

        # Return cleaned data if everything is fine
        cleaned_data['user'] = user  # Store the user instance for use later
        return cleaned_data
