from django import forms
from .models import Lead
class LeadForm(forms.ModelForm):
 class Meta:
  model=Lead;fields=['name','email','phone','service','budget','timeline','message'];widgets={'message':forms.Textarea(attrs={'rows':5})}
