from django.contrib import admin
from .models import (UserProfile, HouseHelpProfile, JobCategory, JobPosting, Application, Match,
                     Review, Message, OTPVerification, Payment, UserStats, Location)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'city', 'created_at']
    list_filter = ['user_type', 'city', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(HouseHelpProfile)
class HouseHelpProfileAdmin(admin.ModelAdmin):
    list_display = ['profile', 'skill_level', 'hourly_rate', 'is_available']
    list_filter = ['skill_level', 'is_available', 'created_at']
    search_fields = ['profile__user__username', 'skills']
    readonly_fields = ['created_at']


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'status', 'job_type', 'created_at']
    list_filter = ['status', 'job_type', 'created_at']
    search_fields = ['title', 'description', 'employer__user__username']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'category', 'description', 'requirements')
        }),
        ('Employer Info', {
            'fields': ('employer',)
        }),
        ('Job Details', {
            'fields': ('location', 'salary', 'job_type', 'hours_per_week', 'is_active')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'approved_at')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_date']
    list_filter = ['status', 'applied_date']
    search_fields = ['applicant__profile__user__username', 'job__title']
    readonly_fields = ['applied_date', 'reviewed_date']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'match_score', 'created_at']
    list_filter = ['status', 'match_score', 'created_at']
    search_fields = ['applicant__profile__user__username', 'job__title']
    readonly_fields = ['created_at', 'updated_at']


# ==================== NEW MODEL ADMINS ====================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'househelp', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__user__username', 'househelp__profile__user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Review Information', {
            'fields': ('reviewer', 'househelp', 'rating', 'comment')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'sent_at']
    list_filter = ['is_read', 'sent_at']
    search_fields = ['sender__user__username', 'recipient__user__username', 'subject', 'content']
    readonly_fields = ['sent_at', 'read_at']
    fieldsets = (
        ('Message', {
            'fields': ('sender', 'recipient', 'subject', 'content', 'job')
        }),
        ('Status', {
            'fields': ('is_read', 'sent_at', 'read_at')
        }),
    )


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'is_verified', 'attempts', 'expires_at']
    list_filter = ['is_verified', 'expires_at']
    search_fields = ['user__username', 'phone']
    readonly_fields = ['expires_at']
    fieldsets = (
        ('User & Contact', {
            'fields': ('user', 'phone')
        }),
        ('OTP Details', {
            'fields': ('otp_code', 'is_verified', 'attempts', 'expires_at')
        }),
        ('Created', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['match', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['transaction_id', 'match__applicant__profile__user__username']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Match Information', {
            'fields': ('match', 'amount')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'status', 'transaction_id', 'paid_at')
        }),
        ('Created', {
            'fields': ('created_at',)
        }),
    )


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_jobs_posted', 'total_jobs_completed', 'average_rating', 'last_active']
    list_filter = ['last_active']
    search_fields = ['user__user__username']
    readonly_fields = ['last_active']
    fieldsets = (
        ('User Statistics', {
            'fields': ('user', 'total_jobs_posted', 'total_jobs_completed', 'total_applications', 'total_earnings', 'total_spent')
        }),
        ('Ratings & Reviews', {
            'fields': ('average_rating', 'total_reviews')
        }),
        ('Messages', {
            'fields': ('messages_sent', 'messages_received')
        }),
        ('Activity', {
            'fields': ('last_active',)
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'radius_km']
    list_filter = ['city']
    search_fields = ['user__user__username', 'city']
    fieldsets = (
        ('Location', {
            'fields': ('user', 'city', 'radius_km')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude')
        }),
    )
