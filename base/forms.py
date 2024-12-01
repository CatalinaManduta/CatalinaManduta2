from django import forms
from .models import ContactMessage  # Import your model

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3



class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)  # Use the invisible reCAPTCHA widget

    class Meta:
        model = ContactMessage  # Link the form to the ContactMessage model
        fields = ['name', 'email', 'company', 'phone', 'message']  # Define which fields to include
        widgets = {  # Add placeholders or other attributes for better UX
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'company': forms.TextInput(attrs={'placeholder': 'Your Company'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message'}),
        }
