from django import forms

from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["name", "description", "homework", "tags",  "date"]

        widgets = {
            'date': forms.DateInput()
        }