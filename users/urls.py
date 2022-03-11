from django.urls import path
from users.views import signup, login, activate_user, logout
from django.contrib.auth import views


urlpatterns = [
    path(route='login', view=login, name='login'),
    path(route='logout', view=logout, name='logout'),
    path(route='signup', view=signup, name='signup'),
    path(route='activate/<token>', view=activate_user, name='activate'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]