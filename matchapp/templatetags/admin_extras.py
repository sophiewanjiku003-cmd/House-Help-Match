from django import template
from django.contrib.auth import get_user_model
from matchapp.models import UserProfile, HouseHelpProfile, JobPosting, Application, Match, JobCategory

register = template.Library()

@register.simple_tag
def admin_counts():
    User = get_user_model()
    return {
        'users': User.objects.count(),
        'profiles': UserProfile.objects.count(),
        'househelps': HouseHelpProfile.objects.count(),
        'jobs': JobPosting.objects.count(),
        'applications': Application.objects.count(),
        'matches': Match.objects.count(),
        'categories': JobCategory.objects.count(),
    }
