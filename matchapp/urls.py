from django.urls import path
from . import views
from .views import JobListView, JobDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        success_url='password-reset-done/'
    ), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='../../password-reset-complete/'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Jobs
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/new/', views.create_job, name='job_create'),
    path('jobs/<int:pk>/edit/', views.update_job, name='job_update'),
    
    # Applications
    path('jobs/<int:pk>/apply/', views.apply_job, name='job_apply'),
    path('my-applications/', views.my_applications, name='my_applications'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Manager URLs
    path('manage-jobs/', views.manage_jobs, name='manage_jobs'),
    path('manage-jobs/<int:pk>/', views.approve_job, name='approve_job'),
    
    # Review System URLs
    path('job/<int:job_id>/reviews/', views.job_reviews, name='job_reviews'),
    path('househelp/<int:househelp_id>/reviews/', views.househelp_reviews, name='househelp_reviews'),
    path('match/<int:match_id>/review/', views.create_review, name='create_review'),
    
    # Messaging System URLs
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('message/<int:user_id>/', views.send_message, name='send_message'),
    
    # OTP/2FA URLs
    path('setup-2fa/', views.setup_two_factor_auth, name='setup_two_factor_auth'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    
    # Location Based Filtering URLs
    path('location-jobs/', views.location_based_jobs, name='location_based_jobs'),
    path('setup-location/', views.setup_location, name='setup_location'),
    
    # Admin Analytics URLs
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('analytics/users/', views.user_statistics, name='user_statistics'),
]