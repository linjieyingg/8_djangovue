from django import forms

from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['name', 'homework', 'tags', 'description', 'date']
        widgets = {
            'date': forms.DateInput()
        }