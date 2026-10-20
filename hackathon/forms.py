from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Registration,Team,Submission,Score
class SignupForm(UserCreationForm):
 email=forms.EmailField(required=True)
 class Meta: model=User;fields=['username','first_name','last_name','email','password1','password2']
 def clean_email(self):
  email=self.cleaned_data['email'].strip().lower()
  if User.objects.filter(email__iexact=email).exists():raise forms.ValidationError('Email already registered')
  return email
class RegistrationForm(forms.ModelForm):
 consent=forms.BooleanField(required=True,label='I accept the hackathon rules and privacy policy')
 class Meta:model=Registration;fields=['phone','city','institution','skills','github','linkedin','track']
class TeamForm(forms.ModelForm):
 class Meta:model=Team;fields=['name','track','idea']
class SubmissionForm(forms.ModelForm):
 class Meta:model=Submission;fields=['title','description','problem','solution','tech_stack','repo_url','demo_url','video_url','slides']
 def clean_slides(self):
  f=self.cleaned_data.get('slides')
  if f:
   if f.size>20*1024*1024:raise forms.ValidationError('PDF must be 20MB or smaller')
   if not f.name.lower().endswith('.pdf'):raise forms.ValidationError('Upload a PDF')
   pos=f.tell();signature=f.read(5);f.seek(pos)
   if signature!=b'%PDF-':raise forms.ValidationError('Invalid PDF file')
  return f
class ScoreForm(forms.ModelForm):
 class Meta:model=Score;fields=['innovation','technical','impact','design','presentation','comments']
