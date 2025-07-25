from django.urls import path
from . import views
from user.views import AdminDashbordView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('signup/', views.signup_view, name = 'signup'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('dashboard/admin/', AdminDashbordView.as_view(), name='admin_dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/participant/', views.participant_dashboard, name='participant_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
     path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
