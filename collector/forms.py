from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        # We exclude 'user' and 'is_locked' because the system handles those automatically
        fields = ['name', 'address', 'email', 'phone_number', 'preferred_technology']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}), # Make address box smaller for mobile
        }