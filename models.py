from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPES = [
        ('employer', 'Employer'),
        ('househelp', 'HouseHelp'),
        ('manager', 'Manager'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='employer')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class HouseHelpProfile(models.Model):
    SKILL_LEVELS = [
        ('beginner', 'Beginner (<1 year)'),
        ('intermediate', 'Intermediate (1-3 years)'),
        ('advanced', 'Advanced (3+ years)'),
    ]
    
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='househelp_profile')
    skills = models.TextField(help_text="Separate skills with commas")
    experience = models.IntegerField(default=0, help_text="Years of experience")
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)
    is_available = models.BooleanField(default=True)
    bio = models.TextField(blank=True, help_text="Tell employers about yourself")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.get_full_name()} - {self.skill_level}"
    
    def get_skills_list(self):
        return [skill.strip() for skill in self.skills.split(',')]

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-briefcase')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Job Categories"

class JobPosting(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('filled', 'Position Filled'),
        ('expired', 'Expired'),
    ]
    
    TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ]
    
    employer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(JobCategory, related_name='jobs')
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='full_time')
    hours_per_week = models.IntegerField(default=40)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_jobs')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.employer.user.username}"
    
    def is_approved(self):
        return self.status == 'approved'
    
    def can_apply(self):
        return self.is_active and self.status == 'approved'
    
    class Meta:
        ordering = ['-created_at']

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewed', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(HouseHelpProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.applicant.profile.user.username} - {self.job.title}"
    
    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_date']

class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('interviewing', 'Interviewing'),
        ('hired', 'Hired'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
    ]
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='matches')
    applicant = models.ForeignKey(HouseHelpProfile, on_delete=models.CASCADE, related_name='matches')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    match_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    employer_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant.profile.user.username} ↔ {self.job.title}"
    
    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-match_score', '-created_at']


# ==================== NEW FEATURES ====================

class Review(models.Model):
    """Rating and review system for househelps"""
    RATING_CHOICES = [
        (1, '⭐ Poor'),
        (2, '⭐⭐ Fair'),
        (3, '⭐⭐⭐ Good'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (5, '⭐⭐⭐⭐⭐ Excellent'),
    ]
    
    househelp = models.ForeignKey(HouseHelpProfile, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_reviews')
    job = models.ForeignKey(JobPosting, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.reviewer.user.username} → {self.househelp.profile.user.username} ({self.rating}⭐)"
    
    class Meta:
        unique_together = ['househelp', 'reviewer', 'job']
        ordering = ['-created_at']


class Message(models.Model):
    """In-app messaging system"""
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    job = models.ForeignKey(JobPosting, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.sender.user.username} → {self.recipient.user.username}: {self.subject}"
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name_plural = "Messages"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class OTPVerification(models.Model):
    """Two-Factor Authentication with OTP"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.is_verified else 'Pending'}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_valid_attempt(self):
        return self.attempts < 3 and not self.is_expired()


class Payment(models.Model):
    """Payment tracking for jobs"""
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD = [
        ('mpesa', 'M-Pesa'),
        ('stripe', 'Stripe'),
        ('bank', 'Bank Transfer'),
        ('wallet', 'Wallet'),
    ]
    
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='mpesa')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment: {self.amount} KES - {self.match} ({self.status})"


class UserStats(models.Model):
    """Analytics and statistics for users"""
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='stats')
    total_jobs_posted = models.IntegerField(default=0)  # For employers
    total_jobs_completed = models.IntegerField(default=0)  # For househelps
    total_applications = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    messages_sent = models.IntegerField(default=0)
    messages_received = models.IntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stats for {self.user.user.username}"
    
    class Meta:
        verbose_name_plural = "User Stats"


class Location(models.Model):
    """Store user preferred locations"""
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='location_info')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100)
    radius_km = models.IntegerField(default=10, help_text="Search radius in kilometers")
    
    def __str__(self):
        return f"{self.user.user.username} - {self.city}"
    
    class Meta:
        verbose_name_plural = "Locations"