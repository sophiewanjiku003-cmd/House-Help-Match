from django.urls import path
from . import views
from .views import JobListView, JobDetailView

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    
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
]