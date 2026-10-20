from django.db import models
from django.utils.text import slugify
class Publishable(models.Model):
 title=models.CharField(max_length=180);slug=models.SlugField(max_length=200,unique=True);summary=models.TextField(blank=True);body=models.TextField(blank=True);published=models.BooleanField(default=False);featured=models.BooleanField(default=False);sort_order=models.PositiveIntegerField(default=0);seo_title=models.CharField(max_length=180,blank=True);seo_description=models.CharField(max_length=300,blank=True);created_at=models.DateTimeField(auto_now_add=True);updated_at=models.DateTimeField(auto_now=True)
 class Meta: abstract=True;ordering=['sort_order','title']
 def __str__(self):return self.title
class Service(Publishable):
 icon=models.CharField(max_length=30,default='✦');benefits=models.TextField(blank=True);technologies=models.CharField(max_length=300,blank=True)
class Project(Publishable):
 client=models.CharField(max_length=160,blank=True);industry=models.CharField(max_length=100,blank=True);technologies=models.CharField(max_length=300,blank=True);challenge=models.TextField(blank=True);solution=models.TextField(blank=True);results=models.TextField(blank=True);image_url=models.URLField(blank=True);service=models.ForeignKey(Service,on_delete=models.SET_NULL,null=True,blank=True,related_name='projects')
class TeamMember(Publishable):
 role=models.CharField(max_length=100);photo_url=models.URLField(blank=True);linkedin=models.URLField(blank=True)
class Testimonial(Publishable):
 person=models.CharField(max_length=100);role=models.CharField(max_length=100,blank=True);company=models.CharField(max_length=100,blank=True);approved=models.BooleanField(default=False)
class FAQ(Publishable):
 category=models.CharField(max_length=80,default='General')
class Post(Publishable):
 category=models.CharField(max_length=80,blank=True);author=models.CharField(max_length=100,blank=True)
class Lead(models.Model):
 TYPES=[('contact','Contact'),('quote','Quote')];STATUSES=[('new','New'),('contacted','Contacted'),('closed','Closed')]
 type=models.CharField(max_length=20,choices=TYPES,default='contact');name=models.CharField(max_length=120);email=models.EmailField();phone=models.CharField(max_length=30,blank=True);service=models.ForeignKey(Service,null=True,blank=True,on_delete=models.SET_NULL);budget=models.CharField(max_length=80,blank=True);timeline=models.CharField(max_length=80,blank=True);message=models.TextField();status=models.CharField(max_length=20,choices=STATUSES,default='new');notes=models.TextField(blank=True);created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self):return f'{self.name} — {self.type}'
