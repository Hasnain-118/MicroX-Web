from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Event,Track,Registration,Team,Membership,Submission,Announcement,JudgeAssignment,Score
class ExportAdmin(admin.ModelAdmin):
 actions=['export_csv']
 @admin.action(description='Export selected rows as CSV')
 def export_csv(self,request,queryset):
  fields=[f.name for f in self.model._meta.fields]
  response=HttpResponse(content_type='text/csv');response['Content-Disposition']=f'attachment; filename="{self.model._meta.model_name}.csv"'
  writer=csv.writer(response);writer.writerow(fields)
  for obj in queryset:writer.writerow([getattr(obj,f) for f in fields])
  return response
@admin.register(Event)
class EventAdmin(ExportAdmin):list_display=['name','published','registration_close_at','submission_close_at','results_published'];prepopulated_fields={'slug':('name',)}
@admin.register(Registration)
class RegistrationAdmin(ExportAdmin):list_display=['user','event','city','institution'];list_filter=['event','city']
@admin.register(Team)
class TeamAdmin(ExportAdmin):list_display=['name','event','leader','track'];list_filter=['event']
@admin.register(Submission)
class SubmissionAdmin(ExportAdmin):list_display=['title','team','status','submitted_at'];list_filter=['status']
for model in [Track,Membership,Announcement,JudgeAssignment,Score]:admin.site.register(model,ExportAdmin)
