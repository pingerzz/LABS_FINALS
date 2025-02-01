from django import forms
from .models import LostAndFoundItem

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostAndFoundItem
        fields = ['item', 'status', 'category', 'location', 'date', 'contact_name', 'contact_phone']  # Adjust based on your model fields
