import secrets
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
U=settings.AUTH_USER_MODEL
class Event(models.Model):
 name=models.CharField(max_length=180);slug=models.SlugField(unique=True);description=models.TextField(blank=True);rules=models.TextField(blank=True);start_at=models.DateTimeField();end_at=models.DateTimeField();registration_open_at=models.DateTimeField();registration_close_at=models.DateTimeField();submission_open_at=models.DateTimeField();submission_close_at=models.DateTimeField();max_team_size=models.PositiveSmallIntegerField(default=4);published=models.BooleanField(default=False);results_published=models.BooleanField(default=False);created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self):return self.name
 def registration_open(self):return self.registration_open_at<=timezone.now()<=self.registration_close_at
 def submission_open(self):return self.submission_open_at<=timezone.now()<=self.submission_close_at
class Track(models.Model):
 event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='tracks');name=models.CharField(max_length=100);description=models.TextField(blank=True)
 class Meta:unique_together=[('event','name')]
 def __str__(self):return self.name
class Registration(models.Model):
 user=models.ForeignKey(U,on_delete=models.CASCADE,related_name='registrations');event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='registrations');phone=models.CharField(max_length=30);city=models.CharField(max_length=100);institution=models.CharField(max_length=180);skills=models.CharField(max_length=300,blank=True);github=models.URLField(blank=True);linkedin=models.URLField(blank=True);track=models.ForeignKey(Track,on_delete=models.SET_NULL,null=True,blank=True);consent_at=models.DateTimeField(default=timezone.now);created_at=models.DateTimeField(auto_now_add=True)
 class Meta:constraints=[models.UniqueConstraint(fields=['user','event'],name='unique_registration_per_event')]
 def __str__(self):return f'{self.user} / {self.event}'
class Team(models.Model):
 event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='teams');name=models.CharField(max_length=120);leader=models.ForeignKey(U,on_delete=models.PROTECT,related_name='led_teams');track=models.ForeignKey(Track,on_delete=models.PROTECT);idea=models.TextField(blank=True);invite_code=models.CharField(max_length=24,unique=True,editable=False);created_at=models.DateTimeField(auto_now_add=True)
 class Meta:constraints=[models.UniqueConstraint(fields=['event','name'],name='unique_team_name_per_event')]
 def save(self,*a,**kw):
  if not self.invite_code:self.invite_code=secrets.token_urlsafe(12)
  super().save(*a,**kw)
 def __str__(self):return self.name
class Membership(models.Model):
 team=models.ForeignKey(Team,on_delete=models.CASCADE,related_name='memberships');user=models.ForeignKey(U,on_delete=models.CASCADE);event=models.ForeignKey(Event,on_delete=models.CASCADE);joined_at=models.DateTimeField(auto_now_add=True)
 class Meta:constraints=[models.UniqueConstraint(fields=['event','user'],name='one_team_per_event'),models.UniqueConstraint(fields=['team','user'],name='one_membership_per_team')]
 def clean(self):
   if self.team and self.event and self.event.pk!=self.team.event.pk:raise ValidationError('Event mismatch')
 def __str__(self):return f'{self.user} in {self.team}'
class Submission(models.Model):
 STATUS=[('draft','Draft'),('submitted','Submitted'),('disqualified','Disqualified')]
 team=models.OneToOneField(Team,on_delete=models.CASCADE,related_name='submission');title=models.CharField(max_length=180);description=models.TextField();problem=models.TextField(blank=True);solution=models.TextField(blank=True);tech_stack=models.CharField(max_length=300);repo_url=models.URLField();demo_url=models.URLField(blank=True);video_url=models.URLField(blank=True);slides=models.FileField(upload_to='decks/',blank=True);status=models.CharField(max_length=20,choices=STATUS,default='draft');submitted_at=models.DateTimeField(null=True,blank=True);disqualification_reason=models.TextField(blank=True);updated_at=models.DateTimeField(auto_now=True)
 def __str__(self):return self.title
class Announcement(models.Model):
 event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='announcements');title=models.CharField(max_length=180);body=models.TextField();published=models.BooleanField(default=False);created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self):return self.title
class JudgeAssignment(models.Model):
 submission=models.ForeignKey(Submission,on_delete=models.CASCADE,related_name='assignments');judge=models.ForeignKey(U,on_delete=models.CASCADE,related_name='judging_assignments')
 class Meta:constraints=[models.UniqueConstraint(fields=['submission','judge'],name='unique_judge_assignment')]
class Score(models.Model):
 assignment=models.OneToOneField(JudgeAssignment,on_delete=models.CASCADE,related_name='score');innovation=models.PositiveSmallIntegerField();technical=models.PositiveSmallIntegerField();impact=models.PositiveSmallIntegerField();design=models.PositiveSmallIntegerField();presentation=models.PositiveSmallIntegerField();comments=models.TextField(blank=True);created_at=models.DateTimeField(auto_now_add=True)
 @property
 def total(self):return self.innovation+self.technical+self.impact+self.design+self.presentation
 def clean(self):
  for field in ('innovation','technical','impact','design','presentation'):
   value=getattr(self,field,None)
   if value is not None and not 0<=value<=10:raise ValidationError({field:'Score must be between 0 and 10'})
