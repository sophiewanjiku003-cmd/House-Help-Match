from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count, Sum
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
import random
import secrets
from .models import *
from .forms import *

# Helper functions
def is_manager(user):
    try:
        return user.userprofile.user_type == 'manager'
    except:
        return False

def is_employer(user):
    try:
        return user.userprofile.user_type == 'employer'
    except:
        return False

def is_househelp(user):
    try:
        return user.userprofile.user_type == 'househelp'
    except:
        return False

# Public views
def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'total_jobs': JobPosting.objects.filter(status='approved').count(),
        'total_househelps': HouseHelpProfile.objects.count(),
        'total_employers': UserProfile.objects.filter(user_type='employer').count(),
    }
    return render(request, 'matchapp/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'matchapp/about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'matchapp/contact.html')

# Authentication views
def register(request):
    """User registration view"""
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save user
            user = user_form.save()
            
            # Save profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Create househelp profile if applicable
            if profile.user_type == 'househelp':
                HouseHelpProfile.objects.create(profile=profile)
            
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/register.html', context)

# Dashboard view
@login_required
def dashboard(request):
    """User dashboard view"""
    try:
        profile = request.user.userprofile
    except:
        # Create profile if doesn't exist
        profile = UserProfile.objects.create(
            user=request.user,
            user_type='employer',
            phone='',
            address='',
            city=''
        )
    
    context = {
        'profile': profile,
    }
    
    # Employer dashboard
    if profile.user_type == 'employer':
        jobs = JobPosting.objects.filter(employer=profile)
        applications = Application.objects.filter(job__employer=profile)
        
        context.update({
            'jobs': jobs,
            'applications': applications,
            'total_jobs': jobs.count(),
            'active_jobs': jobs.filter(is_active=True, status='approved').count(),
            'total_applications': applications.count(),
        })
    
    # HouseHelp dashboard
    elif profile.user_type == 'househelp':
        try:
            househelp_profile = profile.househelp_profile
            applications = Application.objects.filter(applicant=househelp_profile)
            
            # Get matching jobs
            skills_list = househelp_profile.get_skills_list()
            q_objects = Q()
            for skill in skills_list:
                q_objects |= Q(requirements__icontains=skill)
            
            matching_jobs = JobPosting.objects.filter(
                q_objects,
                is_active=True,
                status='approved'
            ).exclude(
                applications__applicant=househelp_profile
            )[:5]
            
            context.update({
                'househelp_profile': househelp_profile,
                'applications': applications,
                'matching_jobs': matching_jobs,
                'total_applications': applications.count(),
                'accepted_applications': applications.filter(status='accepted').count(),
            })
        except HouseHelpProfile.DoesNotExist:
            pass
    
    # Manager dashboard
    elif profile.user_type == 'manager':
        pending_jobs = JobPosting.objects.filter(status='pending')
        pending_applications = Application.objects.filter(status='applied')
        
        context.update({
            'pending_jobs': pending_jobs,
            'pending_applications': pending_applications,
            'total_users': UserProfile.objects.count(),
            'total_jobs_pending': pending_jobs.count(),
        })
    
    return render(request, 'matchapp/dashboard.html', context)

# Job views
class JobListView(ListView):
    """List all approved jobs"""
    model = JobPosting
    template_name = 'matchapp/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = JobPosting.objects.filter(
            is_active=True,
            status='approved'
        ).order_by('-created_at')
        
        # Filter by search query
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(requirements__icontains=query)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by job type
        job_type = self.request.GET.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        return context

class JobDetailView(DetailView):
    """Job detail view"""
    model = JobPosting
    template_name = 'matchapp/jobposting_detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        
        # Check if user has applied
        has_applied = False
        if self.request.user.is_authenticated:
            try:
                profile = self.request.user.userprofile
                if profile.user_type == 'househelp':
                    househelp_profile = profile.househelp_profile
                    has_applied = Application.objects.filter(
                        job=job,
                        applicant=househelp_profile
                    ).exists()
            except:
                pass
        
        context['has_applied'] = has_applied
        context['can_apply'] = job.can_apply()
        return context

@login_required
@user_passes_test(is_employer)
def create_job(request):
    """Create a new job posting"""
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.userprofile
            
            # Set status based on user type
            if request.user.userprofile.user_type == 'manager':
                job.status = 'approved'
                job.approved_by = request.user
                job.approved_at = timezone.now()
                messages.success(request, 'Job posted successfully!')
            else:
                job.status = 'pending'
                messages.success(request, 'Job posted successfully! Awaiting manager approval.')
            
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostingForm()
    
    return render(request, 'matchapp/job_form.html', {'form': form, 'title': 'Post New Job'})

@login_required
@user_passes_test(is_employer)
def update_job(request, pk):
    """Update a job posting"""
    job = get_object_or_404(JobPosting, pk=pk, employer=request.user.userprofile)
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostingForm(instance=job)
    
    return render(request, 'matchapp/job_form.html', {'form': form, 'title': 'Update Job'})

# Application views
@login_required
@user_passes_test(is_househelp)
def apply_job(request, pk):
    """Apply for a job"""
    job = get_object_or_404(JobPosting, pk=pk)
    
    # Check if job is available
    if not job.can_apply():
        messages.error(request, 'This job is no longer accepting applications.')
        return redirect('job_detail', pk=pk)
    
    # Check if already applied
    househelp_profile = request.user.userprofile.househelp_profile
    if Application.objects.filter(job=job, applicant=househelp_profile).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = househelp_profile
            application.save()
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', pk=pk)
    else:
        form = ApplicationForm()
    
    return render(request, 'matchapp/apply_job.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    """View user's applications"""
    try:
        profile = request.user.userprofile
        
        if profile.user_type == 'househelp':
            applications = Application.objects.filter(applicant=profile.househelp_profile)
        elif profile.user_type == 'employer':
            applications = Application.objects.filter(job__employer=profile)
        elif profile.user_type == 'manager':
            applications = Application.objects.all()
        else:
            applications = None
        
        context = {
            'applications': applications,
        }
        return render(request, 'matchapp/my_applications.html', context)
    except:
        return redirect('dashboard')

# Profile views
@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    # Add househelp profile form if applicable
    try:
        if request.user.userprofile.user_type == 'househelp':
            househelp_profile = request.user.userprofile.househelp_profile
            if request.method == 'POST':
                househelp_form = HouseHelpProfileForm(request.POST, instance=househelp_profile)
                if househelp_form.is_valid():
                    househelp_form.save()
            else:
                househelp_form = HouseHelpProfileForm(instance=househelp_profile)
            context['househelp_form'] = househelp_form
    except:
        pass
    
    return render(request, 'matchapp/profile.html', context)

# Manager views
@login_required
@user_passes_test(is_manager)
def manage_jobs(request):
    """Manager job approval view"""
    jobs = JobPosting.objects.filter(status='pending')
    return render(request, 'matchapp/manage_jobs.html', {'jobs': jobs})

@login_required
@user_passes_test(is_manager)
def approve_job(request, pk):
    """Approve or reject a job"""
    job = get_object_or_404(JobPosting, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            job.status = 'approved'
            job.approved_by = request.user
            job.approved_at = timezone.now()
            messages.success(request, 'Job approved successfully!')
        elif action == 'reject':
            job.status = 'rejected'
            messages.warning(request, 'Job rejected.')
        
        job.save()
        return redirect('manage_jobs')
    
    return render(request, 'matchapp/approve_job.html', {'job': job})


# ==================== REVIEW SYSTEM VIEWS ====================

@login_required
def job_reviews(request, job_id):
    """View all reviews for a job"""
    job = get_object_or_404(JobPosting, pk=job_id)
    matches = Match.objects.filter(job=job, status__in=['completed', 'hired'])
    reviews = Review.objects.filter(job=job).select_related('reviewer', 'househelp')
    
    context = {
        'job': job,
        'reviews': reviews,
        'average_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
        'total_reviews': reviews.count(),
    }
    return render(request, 'matchapp/job_reviews.html', context)


@login_required
def househelp_reviews(request, househelp_id):
    """View all reviews for a househelp"""
    househelp = get_object_or_404(HouseHelpProfile, pk=househelp_id)
    reviews = Review.objects.filter(househelp=househelp).select_related('reviewer')
    
    # Update user stats
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    try:
        stats = househelp.profile.stats
        stats.average_rating = avg_rating
        stats.total_reviews = reviews.count()
        stats.save()
    except:
        pass
    
    context = {
        'househelp': househelp,
        'reviews': reviews,
        'average_rating': avg_rating,
        'total_reviews': reviews.count(),
    }
    return render(request, 'matchapp/househelp_reviews.html', context)


@login_required
def create_review(request, match_id):
    """Create a review for a completed match"""
    match = get_object_or_404(Match, pk=match_id)
    
    # Verify user is the employer
    if match.job.employer != request.user.userprofile:
        messages.error(request, 'You do not have permission to review this match.')
        return redirect('dashboard')
    
    # Check if already reviewed
    if Review.objects.filter(
        job=match.job,
        househelp=match.applicant,
        reviewer=request.user.userprofile
    ).exists():
        messages.warning(request, 'You have already reviewed this househelp for this job.')
        return redirect('match_detail', pk=match.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.househelp = match.applicant
            review.reviewer = request.user.userprofile
            review.job = match.job
            review.save()
            
            messages.success(request, 'Your review has been posted successfully!')
            return redirect('match_detail', pk=match.pk)
    else:
        form = ReviewForm()
    
    context = {'form': form, 'match': match}
    return render(request, 'matchapp/create_review.html', context)


# ==================== MESSAGING SYSTEM VIEWS ====================

@login_required
def inbox(request):
    """View user's inbox"""
    received_messages = Message.objects.filter(
        recipient=request.user.userprofile
    ).select_related('sender').order_by('-sent_at')
    
    unread_count = received_messages.filter(is_read=False).count()
    
    context = {
        'messages': received_messages,
        'unread_count': unread_count,
    }
    return render(request, 'matchapp/inbox.html', context)


@login_required
def conversation(request, user_id):
    """View conversation with a specific user"""
    other_user = get_object_or_404(UserProfile, pk=user_id)
    current_user = request.user.userprofile
    
    # Get all messages in conversation
    messages_list = Message.objects.filter(
        Q(sender=current_user, recipient=other_user) |
        Q(sender=other_user, recipient=current_user)
    ).select_related('sender', 'recipient').order_by('sent_at')
    
    # Mark received messages as read
    Message.objects.filter(
        sender=other_user,
        recipient=current_user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = current_user
            message.recipient = other_user
            message.save()
            
            return redirect('conversation', user_id=user_id)
    else:
        form = MessageForm()
    
    context = {
        'other_user': other_user,
        'messages': messages_list,
        'form': form,
    }
    return render(request, 'matchapp/conversation.html', context)


@login_required
def send_message(request, user_id):
    """Send a message to a user"""
    recipient = get_object_or_404(UserProfile, pk=user_id)
    sender = request.user.userprofile
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()
            
            messages.success(request, 'Message sent successfully!')
            return redirect('conversation', user_id=user_id)
    else:
        form = MessageForm()
    
    context = {'form': form, 'recipient': recipient}
    return render(request, 'matchapp/send_message.html', context)


# ==================== OTP VERIFICATION VIEWS ====================

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


@login_required
def setup_two_factor_auth(request):
    """Setup two-factor authentication"""
    user = request.user
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            phone = request.POST.get('phone')
            otp_code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=5)
            
            otp_obj, created = OTPVerification.objects.get_or_create(
                user=user,
                defaults={
                    'phone': phone,
                    'otp_code': otp_code,
                    'expires_at': expires_at,
                }
            )
            
            if not created:
                otp_obj.phone = phone
                otp_obj.otp_code = otp_code
                otp_obj.expires_at = expires_at
                otp_obj.attempts = 0
                otp_obj.save()
            
            # TODO: Send OTP via SMS (integrate M-Pesa or Twilio)
            messages.info(request, f'OTP sent to {phone}. OTP: {otp_code}')
            return redirect('verify_otp')
    
    try:
        otp_obj = OTPVerification.objects.get(user=user)
        initial_phone = otp_obj.phone
    except OTPVerification.DoesNotExist:
        initial_phone = ''
    
    context = {'initial_phone': initial_phone}
    return render(request, 'matchapp/setup_2fa.html', context)


@login_required
def verify_otp(request):
    """Verify OTP for two-factor authentication"""
    user = request.user
    
    try:
        otp_obj = OTPVerification.objects.get(user=user)
    except OTPVerification.DoesNotExist:
        messages.error(request, 'Please setup 2FA first.')
        return redirect('setup_two_factor_auth')
    
    if otp_obj.is_verified:
        messages.info(request, 'Your phone is already verified.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp_code']
            
            if otp_obj.is_expired():
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('setup_two_factor_auth')
            
            if not otp_obj.is_valid_attempt():
                messages.error(request, 'Too many failed attempts. Please try again later.')
                return redirect('setup_two_factor_auth')
            
            if entered_otp == otp_obj.otp_code:
                otp_obj.is_verified = True
                otp_obj.save()
                messages.success(request, 'Your phone has been verified successfully!')
                return redirect('dashboard')
            else:
                otp_obj.attempts += 1
                otp_obj.save()
                messages.error(request, f'Invalid OTP. Attempts remaining: {3 - otp_obj.attempts}')
    else:
        form = OTPVerificationForm()
    
    context = {'form': form, 'phone': otp_obj.phone}
    return render(request, 'matchapp/verify_otp.html', context)


# ==================== LOCATION-BASED FILTERING VIEWS ====================

@login_required
def location_based_jobs(request):
    """Get jobs based on user location preferences"""
    profile = request.user.userprofile
    
    try:
        location = profile.location_info
    except Location.DoesNotExist:
        messages.info(request, 'Please set your location preferences first.')
        return redirect('setup_location')
    
    # Filter jobs by location and radius
    jobs = JobPosting.objects.filter(
        is_active=True,
        status='approved',
        location__icontains=location.city
    ).order_by('-created_at')
    
    # Apply additional filters
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')
    
    if min_salary:
        jobs = jobs.filter(salary__gte=float(min_salary))
    if max_salary:
        jobs = jobs.filter(salary__lte=float(max_salary))
    
    context = {
        'jobs': jobs,
        'location': location,
        'page_title': f'Jobs in {location.city}',
    }
    return render(request, 'matchapp/location_based_jobs.html', context)


@login_required
def setup_location(request):
    """Setup user location preferences"""
    profile = request.user.userprofile
    
    try:
        location = profile.location_info
    except Location.DoesNotExist:
        location = None
    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location_obj = form.save(commit=False)
            location_obj.user = profile
            location_obj.save()
            messages.success(request, 'Location preferences updated successfully!')
            return redirect('location_based_jobs')
    else:
        form = LocationForm(instance=location)
    
    context = {'form': form}
    return render(request, 'matchapp/setup_location.html', context)


# ==================== ADMIN ANALYTICS DASHBOARD VIEWS ====================

@login_required
@user_passes_test(is_manager)
def analytics_dashboard(request):
    """Admin analytics dashboard"""
    # User statistics
    total_users = UserProfile.objects.count()
    total_employers = UserProfile.objects.filter(user_type='employer').count()
    total_househelps = UserProfile.objects.filter(user_type='househelp').count()
    
    # Job statistics
    total_jobs = JobPosting.objects.count()
    approved_jobs = JobPosting.objects.filter(status='approved').count()
    pending_jobs = JobPosting.objects.filter(status='pending').count()
    active_jobs = JobPosting.objects.filter(is_active=True, status='approved').count()
    
    # Application statistics
    total_applications = Application.objects.count()
    accepted_applications = Application.objects.filter(status='accepted').count()
    
    # Match statistics
    total_matches = Match.objects.count()
    completed_matches = Match.objects.filter(status='completed').count()
    active_matches = Match.objects.filter(status__in=['pending', 'contacted', 'interviewing', 'hired']).count()
    
    # Review statistics
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Payment statistics
    total_payments = Payment.objects.count()
    completed_payments = Payment.objects.filter(status='completed').count()
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Top rated househelps
    top_househelps = HouseHelpProfile.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:5]
    
    # Recent matches
    recent_matches = Match.objects.select_related('job', 'applicant').order_by('-created_at')[:10]
    
    # Activity by day (last 30 days)
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_jobs = JobPosting.objects.filter(created_at__gte=thirty_days_ago).count()
    recent_applications = Application.objects.filter(applied_date__gte=thirty_days_ago).count()
    recent_matches_count = Match.objects.filter(created_at__gte=thirty_days_ago).count()
    
    context = {
        # User stats
        'total_users': total_users,
        'total_employers': total_employers,
        'total_househelps': total_househelps,
        
        # Job stats
        'total_jobs': total_jobs,
        'approved_jobs': approved_jobs,
        'pending_jobs': pending_jobs,
        'active_jobs': active_jobs,
        
        # Application stats
        'total_applications': total_applications,
        'accepted_applications': accepted_applications,
        
        # Match stats
        'total_matches': total_matches,
        'completed_matches': completed_matches,
        'active_matches': active_matches,
        
        # Review stats
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        
        # Payment stats
        'total_payments': total_payments,
        'completed_payments': completed_payments,
        'total_revenue': total_revenue,
        
        # Top performers
        'top_househelps': top_househelps,
        'recent_matches': recent_matches,
        
        # Recent activity
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
        'recent_matches_count': recent_matches_count,
    }
    return render(request, 'matchapp/analytics_dashboard.html', context)


@login_required
@user_passes_test(is_manager)
def user_statistics(request):
    """Detailed user statistics"""
    users = UserProfile.objects.annotate(
        jobs_posted=Count('jobs_posted'),
        applications_received=Count('jobs_posted__applications'),
        avg_rating=Avg('reviews_given__rating')
    ).order_by('-created_at')
    
    context = {'users': users}
    return render(request, 'matchapp/user_statistics.html', context)