from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Service,Project,TeamMember,Testimonial,FAQ,Post
from .forms import LeadForm
def home(request):return render(request,'website/home.html',{'services':Service.objects.filter(published=True)[:6],'projects':Project.objects.filter(published=True,featured=True)[:3],'testimonials':Testimonial.objects.filter(published=True,approved=True)[:3]})
def services(request):return render(request,'website/services.html',{'items':Service.objects.filter(published=True),'heading':'What we do'})
def service_detail(request,slug):return render(request,'website/detail.html',{'item':get_object_or_404(Service,published=True,slug=slug),'kind':'Service'})
def projects(request):return render(request,'website/projects.html',{'items':Project.objects.filter(published=True),'heading':'Selected work'})
def project_detail(request,slug):return render(request,'website/detail.html',{'item':get_object_or_404(Project,published=True,slug=slug),'kind':'Case study'})
def about(request):return render(request,'website/about.html',{'members':TeamMember.objects.filter(published=True)})
def process(request):return render(request,'website/process.html')
def posts(request):return render(request,'website/posts.html',{'items':Post.objects.filter(published=True)})
def post_detail(request,slug):return render(request,'website/detail.html',{'item':get_object_or_404(Post,published=True,slug=slug),'kind':'Insight'})
def contact(request,kind='contact'):
 form=LeadForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  lead=form.save(commit=False);lead.type=kind;lead.save()
  try:send_mail('MicroX enquiry received','Thank you for contacting MicroX. We will review your enquiry.',settings.DEFAULT_FROM_EMAIL,[lead.email],fail_silently=False)
  except Exception:pass
  messages.success(request,'Thanks! Your enquiry has been received.');return redirect('home')
 return render(request,'website/contact.html',{'form':form,'kind':kind})
def legal(request,page):
 if page not in ('privacy','terms','cookies'):raise __import__('django.http',fromlist=['Http404']).Http404()
 return render(request,'website/legal.html',{'page':page})
def not_found(request,exception):return render(request,'404.html',status=404)
