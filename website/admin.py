from django.contrib import admin
from .models import Service,Project,TeamMember,Testimonial,FAQ,Post,Lead
class ContentAdmin(admin.ModelAdmin):
 list_display=['title','published','featured','sort_order'];list_filter=['published','featured'];search_fields=['title','summary'];prepopulated_fields={'slug':('title',)}
for model in [Service,Project,TeamMember,Testimonial,FAQ,Post]:admin.site.register(model,ContentAdmin)
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
 list_display=['name','email','type','status','created_at'];list_filter=['type','status'];search_fields=['name','email']
