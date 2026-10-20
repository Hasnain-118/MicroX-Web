from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from website import views as web
urlpatterns=[path('admin/',admin.site.urls),path('',include('website.urls')),path('hackathon/',include('hackathon.urls')),path('accounts/login/',auth_views.LoginView.as_view(template_name='auth/login.html'),name='login'),path('accounts/logout/',auth_views.LogoutView.as_view(),name='logout'),path('accounts/password-reset/',auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html',email_template_name='auth/password_reset_email.txt',success_url='/accounts/login/'),name='password_reset')]
handler404='website.views.not_found'
