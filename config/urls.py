"""
URL configuration for HouseHelp Match project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from matchapp.views import CustomLoginView

# Customize default admin site
admin.site.site_header = "Match-web Admin"
admin.site.site_title = "Match-web Admin Portal"
admin.site.index_title = "Welcome to Match-web Admin"

urlpatterns = [
    # Ensure explicit admin logout redirects back to admin login
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin_logout'),
    path('admin/', admin.site.urls),
    path('', include('matchapp.urls')),
    # Ensure the accounts login uses our CustomLoginView so `next=/admin/` redirects correctly
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    # Admin-specific logout that redirects back to admin login
    path('admin-signout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin_signout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
