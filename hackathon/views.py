from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404,HttpResponseForbidden
from django.db import transaction,IntegrityError
from django.utils import timezone
from .models import Event,Track,Registration,Team,Membership,Submission,Announcement,JudgeAssignment
from .forms import SignupForm,RegistrationForm,TeamForm,SubmissionForm,ScoreForm

def landing(request):return render(request,'hackathon/landing.html',{'events':Event.objects.filter(published=True).order_by('start_at')})
def event_detail(request,slug):
 event=get_object_or_404(Event,slug=slug,published=True)
 return render(request,'hackathon/event.html',{'event':event,'tracks':event.tracks.all()})
def signup(request):
 form=SignupForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  user=form.save();login(request,user);messages.success(request,'Account created. Please register for an event.');return redirect('hackathon')
 return render(request,'hackathon/form.html',{'form':form,'heading':'Create account','button':'Sign up'})
@login_required
def register(request,slug):
 event=get_object_or_404(Event,slug=slug,published=True)
 if not event.registration_open():messages.error(request,'Registration is closed.');return redirect('event',slug=slug)
 if Registration.objects.filter(user=request.user,event=event).exists():return redirect('dashboard')
 form=RegistrationForm(request.POST or None);form.fields['track'].queryset=event.tracks.all()
 if request.method=='POST' and form.is_valid():
  obj=form.save(commit=False);obj.user=request.user;obj.event=event;obj.save();messages.success(request,'Registration successful.');return redirect('dashboard')
 return render(request,'hackathon/form.html',{'form':form,'heading':'Event registration','button':'Register'})
@login_required
def dashboard(request):
 registrations=Registration.objects.filter(user=request.user).select_related('event')
 memberships=Membership.objects.filter(user=request.user).select_related('team','event')
 return render(request,'hackathon/dashboard.html',{'registrations':registrations,'memberships':memberships,'announcements':Announcement.objects.filter(published=True,event__in=registrations.values('event')).order_by('-created_at')[:10]})
@login_required
def create_team(request,slug):
 event=get_object_or_404(Event,slug=slug,published=True)
 if not event.registration_open():return HttpResponseForbidden('Team formation is closed')
 if not Registration.objects.filter(user=request.user,event=event).exists():return HttpResponseForbidden('Register for the event first')
 if Membership.objects.filter(user=request.user,event=event).exists():return HttpResponseForbidden('Already in a team')
 form=TeamForm(request.POST or None);form.fields['track'].queryset=event.tracks.all()
 if request.method=='POST' and form.is_valid():
  try:
   with transaction.atomic():
    team=form.save(commit=False);team.event=event;team.leader=request.user;team.save();Membership.objects.create(team=team,event=event,user=request.user)
   messages.success(request,'Team created. Share your invite code.');return redirect('dashboard')
  except IntegrityError:form.add_error(None,'Team name is already used or membership exists')
 return render(request,'hackathon/form.html',{'form':form,'heading':'Create a team','button':'Create team'})
@login_required
def join_team(request):
 if request.method!='POST':return redirect('dashboard')
 code=request.POST.get('invite_code','').strip();team=get_object_or_404(Team,invite_code=code)
 if not team.event.registration_open():return HttpResponseForbidden('Team joining is closed')
 if not Registration.objects.filter(user=request.user,event=team.event).exists():return HttpResponseForbidden('Register first')
 try:
  with transaction.atomic():
   locked=Team.objects.select_for_update().get(pk=team.pk)
   if locked.memberships.count()>=locked.event.max_team_size:return HttpResponseForbidden('Team is full')
   Membership.objects.create(team=locked,event=locked.event,user=request.user)
  messages.success(request,'You joined the team')
 except IntegrityError:messages.error(request,'You are already on a team for this event')
 return redirect('dashboard')
@login_required
def submit(request,team_id):
 team=get_object_or_404(Team,pk=team_id)
 if not Membership.objects.filter(team=team,user=request.user).exists():return HttpResponseForbidden('Not a team member')
 if not team.event.submission_open():return HttpResponseForbidden('Submission window is closed')
 existing=Submission.objects.filter(team=team).first()
 if existing and existing.status=='disqualified':return HttpResponseForbidden('Submission is disqualified')
 form=SubmissionForm(request.POST or None,request.FILES or None,instance=existing)
 if request.method=='POST' and form.is_valid():
  obj=form.save(commit=False);obj.team=team
  if request.POST.get('action')=='submit':obj.status='submitted';obj.submitted_at=timezone.now()
  else:obj.status='draft'
  obj.save();messages.success(request,'Project saved');return redirect('dashboard')
 return render(request,'hackathon/form.html',{'form':form,'heading':'Project submission','button':'Save draft','submission':True})
@login_required
def judge(request):
 if not request.user.groups.filter(name='Judges').exists() and not request.user.is_superuser:return HttpResponseForbidden('Judges only')
 return render(request,'hackathon/judge.html',{'assignments':JudgeAssignment.objects.filter(judge=request.user).select_related('submission','submission__team')})
@login_required
def score(request,assignment_id):
 assignment=get_object_or_404(JudgeAssignment,pk=assignment_id,judge=request.user)
 if assignment.submission.status!='submitted':return HttpResponseForbidden('Not eligible for scoring')
 form=ScoreForm(request.POST or None,instance=getattr(assignment,'score',None))
 if request.method=='POST' and form.is_valid():
  item=form.save(commit=False);item.assignment=assignment;item.full_clean();item.save();messages.success(request,'Score saved');return redirect('judge')
 return render(request,'hackathon/form.html',{'form':form,'heading':'Score: '+assignment.submission.title,'button':'Save score'})
def results(request,slug):
 event=get_object_or_404(Event,slug=slug,published=True)
 if not event.results_published:raise Http404('Results not published')
 from django.db.models import Avg,F,ExpressionWrapper,FloatField
 submissions=Submission.objects.filter(team__event=event,status='submitted').annotate(avg_score=Avg(F('assignments__score__innovation')+F('assignments__score__technical')+F('assignments__score__impact')+F('assignments__score__design')+F('assignments__score__presentation'),output_field=FloatField())).order_by('-avg_score')
 return render(request,'hackathon/results.html',{'event':event,'submissions':submissions})
