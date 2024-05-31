from django import forms
from .models import Domain, ScraperProduct

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name', 'url']

class ScraperProductForm(forms.ModelForm):
    class Meta:
        model = ScraperProduct
        fields = ['title', 'price', 'description', 'images', 'link']
